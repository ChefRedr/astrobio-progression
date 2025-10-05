import csv
import json
import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, Optional
import multiprocessing as mp
import logging
from collections import Counter

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MAX_WORKERS = 6
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.5
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_errors.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_session():
    """Create a requests session with retry logic and connection pooling."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_maxsize=10)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(HEADERS)
    return session


def get_meta(soup: BeautifulSoup, name: str) -> Optional[str]:
    """Extract metadata from meta tags."""
    tag = soup.find('meta', attrs={'name': name})
    return tag['content'].strip() if tag and tag.has_attr('content') else None


def get_text(node) -> str:
    """Extract clean text from a BeautifulSoup node."""
    return " ".join(node.stripped_strings) if node else ""


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def scrape_paper(url: str, session: requests.Session) -> Dict:
    """Scrape a paper from the given URL."""
    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        doi = get_meta(soup, 'citation_doi')
        pmid = get_meta(soup, 'citation_pmid')
        missing_fields = []
        
        authors = []
        author_tags = soup.find_all('meta', {'name': 'citation_author'})
        affiliation_tags = soup.find_all('meta', {'name': 'citation_author_institution'})
        
        for i, author_tag in enumerate(author_tags):
            author_name = author_tag.get('content', '').strip()
            if author_name:
                authors.append({
                    'name': author_name,
                    'affiliation': affiliation_tags[i]['content'].strip() 
                                   if i < len(affiliation_tags) else None
                })

        # Extract abstract paragraphs
        abstract_paragraphs = []
        abstract_section = soup.find('section', class_='abstract')
        if abstract_section:
            for p in abstract_section.find_all('p'):
                para_text = p.get_text(strip=True)
                if para_text:
                    abstract_paragraphs.append({
                        'text': para_text,
                        'word_count': count_words(para_text)
                    })

        sections = []
        total_words = 0
        main_article = soup.find('article')
        
        if main_article:
            for section in main_article.find_all('section', recursive=False):
                heading = section.find(['h2', 'h3'], class_='pmc_sec_title')
                heading_text = get_text(heading) if heading else 'Untitled Section'
                
                # Extract paragraphs individually
                paragraphs = []
                for p in section.find_all('p'):
                    para_text = p.get_text(strip=True)
                    if para_text:
                        word_count = count_words(para_text)
                        total_words += word_count
                        paragraphs.append({
                            'text': para_text,
                            'word_count': word_count
                        })
                
                if paragraphs:
                    sections.append({
                        'heading': heading_text,
                        'paragraphs': paragraphs,
                        'paragraph_count': len(paragraphs),
                        'total_word_count': sum(p['word_count'] for p in paragraphs)
                    })

        references = []
        ref_list = soup.find('section', class_='ref-list')
        if ref_list:
            for idx, ref in enumerate(ref_list.find_all('li'), 1):
                cite = ref.find('cite')
                if cite:
                    references.append({
                        'id': str(idx),
                        'text': get_text(cite)
                    })

        figures = []
        tables = []
        
        for fig in soup.find_all('figure', class_='fig'):
            caption = fig.find('figcaption')
            img = fig.find('img')
            fig_id = fig.get('id', '')
            caption_text = get_text(caption)
            
            if 'table' in fig_id.lower():
                tables.append({
                    'id': fig_id or f'table_{len(tables) + 1}',
                    'caption': caption_text
                })
            else:
                figures.append({
                    'id': fig_id or f'figure_{len(figures) + 1}',
                    'caption': caption_text,
                    'url': img.get('src') if img else None
                })

        funding_section = soup.find('section', id='funding-statement1')
        funding = get_text(funding_section)
        if funding:
            funding = funding.replace('Funding Statement', '', 1).strip()
        
        ack_section = soup.find('section', id='ack1')
        acknowledgments = get_text(ack_section)
        if acknowledgments:
            acknowledgments = acknowledgments.replace('Acknowledgments', '', 1).strip()

        if not doi:
            missing_fields.append('doi')
        if not pmid:
            missing_fields.append('pmid')
        if not abstract_paragraphs:
            missing_fields.append('abstract')
        
        return {
            'success': True,
            'paper_id': doi or f"hash_{hashlib.md5(url.encode()).hexdigest()[:16]}",
            'source_url': url,
            'scraped_at': datetime.now(timezone.utc).isoformat(),
            'missing_fields': missing_fields,
            'metadata': {
                'title': get_meta(soup, 'citation_title'),
                'authors': authors,
                'journal': get_meta(soup, 'citation_journal_title'),
                'publisher': get_meta(soup, 'citation_publisher'),
                'doi': doi,
                'pmid': pmid,
                'publication_date': get_meta(soup, 'citation_publication_date'),
                'volume': get_meta(soup, 'citation_volume'),
                'issue': get_meta(soup, 'citation_issue'),
                'pages': get_meta(soup, 'citation_firstpage')
            },
            'abstract_paragraphs': abstract_paragraphs,
            'sections': sections,
            'references': references,
            'figures': figures,
            'tables': tables,
            'funding': funding,
            'acknowledgments': acknowledgments,
            'metrics': {
                'total_word_count': total_words,
                'section_count': len(sections),
                'total_paragraph_count': sum(s['paragraph_count'] for s in sections),
                'abstract_paragraph_count': len(abstract_paragraphs),
                'reference_count': len(references),
                'figure_count': len(figures),
                'table_count': len(tables)
            }
        }
    
    except requests.HTTPError as e:
        error_detail = f"HTTP {e.response.status_code}" if e.response else str(e)
        logger.error(f"HTTP Error for {url}: {error_detail}")
        return {
            'success': False,
            'paper_id': f"error_{hashlib.sha1(url.encode()).hexdigest()[:16]}",
            'source_url': url,
            'scraped_at': datetime.now(timezone.utc).isoformat(),
            'error': error_detail,
            'error_type': 'HTTPError',
            'status_code': e.response.status_code if e.response else None
        }
    except requests.Timeout as e:
        logger.error(f"Timeout for {url}: {str(e)}")
        return {
            'success': False,
            'paper_id': f"error_{hashlib.sha1(url.encode()).hexdigest()[:16]}",
            'source_url': url,
            'scraped_at': datetime.now(timezone.utc).isoformat(),
            'error': 'Request timeout',
            'error_type': 'Timeout'
        }
    except requests.RequestException as e:
        logger.error(f"Request Error for {url}: {str(e)}")
        return {
            'success': False,
            'paper_id': f"error_{hashlib.sha1(url.encode()).hexdigest()[:16]}",
            'source_url': url,
            'scraped_at': datetime.now(timezone.utc).isoformat(),
            'error': str(e),
            'error_type': 'RequestException'
        }
    except Exception as e:
        logger.error(f"Unexpected Error for {url}: {str(e)}", exc_info=True)
        return {
            'success': False,
            'paper_id': f"error_{hashlib.sha1(url.encode()).hexdigest()[:16]}",
            'source_url': url,
            'scraped_at': datetime.now(timezone.utc).isoformat(),
            'error': str(e),
            'error_type': type(e).__name__
        }


def transform_for_llm(record: Dict) -> Dict:
    """
    Transform scraped data into an LLM-friendly format.
    Optimized for RAG (Retrieval-Augmented Generation) use cases.
    Each paragraph is stored individually for easy access.
    """
    if not record.get('success'):
        return {
            'paper_id': record.get('paper_id'),
            'source_url': record.get('source_url'),
            'scraped_at': record.get('scraped_at'),
            'status': 'error',
            'error': record.get('error', 'Unknown error'),
            'error_type': record.get('error_type', 'UnknownError'),
            'status_code': record.get('status_code')
        }
    
    meta = record.get('metadata', {})

    author_list = []
    for author in meta.get('authors', []):
        if isinstance(author, dict):
            name = author.get('name', '').strip()
            if name:
                author_list.append(name)

    # Process abstract paragraphs
    abstract_paragraphs = []
    for para in record.get('abstract_paragraphs', []):
        text = para.get('text', '').strip()
        if text:
            abstract_paragraphs.append({
                'text': text,
                'word_count': para.get('word_count', count_words(text))
            })

    # Process sections with individual paragraphs
    sections = []
    for sec in record.get('sections', []):
        heading = sec.get('heading', '').strip()
        paragraphs = []
        
        for para in sec.get('paragraphs', []):
            text = para.get('text', '').strip()
            if text:
                paragraphs.append({
                    'text': text,
                    'word_count': para.get('word_count', count_words(text))
                })
        
        if paragraphs:
            sections.append({
                'heading': heading or 'Untitled',
                'paragraphs': paragraphs,
                'paragraph_count': len(paragraphs),
                'total_word_count': sum(p['word_count'] for p in paragraphs)
            })

    references = []
    for ref in record.get('references', []):
        text = ref.get('text', '').strip()
        if text:
            references.append({
                'id': ref.get('id'),
                'citation': text
            })

    figures_tables = []
    for fig in record.get('figures', []):
        caption = fig.get('caption', '').strip()
        if caption or fig.get('url'):
            figures_tables.append({
                'type': 'figure',
                'id': fig.get('id'),
                'caption': caption,
                'url': fig.get('url')
            })
    
    for tbl in record.get('tables', []):
        caption = tbl.get('caption', '').strip()
        if caption:
            figures_tables.append({
                'type': 'table',
                'id': tbl.get('id'),
                'caption': caption
            })
    
    return {
        'paper_id': record.get('paper_id'),
        'source_url': record.get('source_url'),
        'scraped_at': record.get('scraped_at'),
        'status': 'success',
        'missing_fields': record.get('missing_fields', []),
        
        'title': meta.get('title', '').strip(),
        'authors': author_list,
        'journal': meta.get('journal'),
        'publication_date': meta.get('publication_date'),
        'doi': meta.get('doi'),
        'pmid': meta.get('pmid'),

        'abstract_paragraphs': abstract_paragraphs,
        'sections': sections,

        'references': references,
        'figures_tables': figures_tables,
        'funding': record.get('funding'),
        'acknowledgments': record.get('acknowledgments'),

        'metrics': record.get('metrics', {})
    }


def process_url(url: str) -> str:
    """Process a single URL (worker function for multiprocessing)."""
    session = create_session()
    try:
        time.sleep(RATE_LIMIT_DELAY)
        record = scrape_paper(url, session)
        llm_record = transform_for_llm(record)
        return json.dumps(llm_record, ensure_ascii=False)
    finally:
        session.close()


def analyze_failures(output_file: str = "llm_data_biopub.jsonl"):
    """Analyze the failures in the output file and print a summary."""
    error_counts = Counter()
    failed_urls = []
    status_codes = Counter()
    
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if record.get('status') == 'error':
                        error_type = record.get('error_type', 'Unknown')
                        error_counts[error_type] += 1
                        failed_urls.append({
                            'url': record.get('source_url'),
                            'error': record.get('error'),
                            'type': error_type
                        })
                        
                        if record.get('status_code'):
                            status_codes[record.get('status_code')] += 1
                except json.JSONDecodeError:
                    continue
        
        if error_counts:
            print("\n" + "="*60)
            print("FAILURE ANALYSIS")
            print("="*60)
            print(f"\nTotal failures: {sum(error_counts.values())}")
            print("\nError types:")
            for error_type, count in error_counts.most_common():
                print(f"  {error_type}: {count}")
            
            if status_codes:
                print("\nHTTP Status codes:")
                for code, count in status_codes.most_common():
                    print(f"  {code}: {count}")
            
            print("\nFailed URLs (first 10):")
            for i, fail in enumerate(failed_urls[:10], 1):
                print(f"\n{i}. {fail['url']}")
                print(f"   Type: {fail['type']}")
                print(f"   Error: {fail['error'][:100]}...")
            
            if len(failed_urls) > 10:
                print(f"\n... and {len(failed_urls) - 10} more failures")
            
            print("\n" + "="*60)
    except FileNotFoundError:
        print(f"Output file {output_file} not found")


def main():
    """Main execution function."""
    source_urls = []
    csv_row_count = 0
    empty_urls = 0
    
    try:
        with open("biopub_data.csv", "r", encoding="utf-8", newline="") as csv_in:
            reader = csv.DictReader(csv_in)
            for row in reader:
                csv_row_count += 1
                link = row.get("Link", "").strip()
                if link:
                    source_urls.append(link)
                else:
                    empty_urls += 1
                    logger.warning(f"Empty URL found in CSV row {csv_row_count}")
    except FileNotFoundError:
        print("Error: biopub_data.csv not found")
        return
    
    print(f"CSV Analysis:")
    print(f"  Total rows: {csv_row_count}")
    print(f"  Valid URLs: {len(source_urls)}")
    print(f"  Empty URLs: {empty_urls}")
    
    if not source_urls:
        print("No URLs found in CSV file")
        return
    
    print(f"\nProcessing {len(source_urls)} papers...")
    
    num_workers = min(MAX_WORKERS, max(2, mp.cpu_count() - 1))
    print(f"Using {num_workers} worker processes\n")

    successful = 0
    failed = 0
    processed_count = 0
    
    with mp.Pool(processes=num_workers) as pool, \
         open("llm_data_biopub.jsonl", "w", encoding="utf-8") as out:
        
        for result_json in pool.imap_unordered(process_url, source_urls, chunksize=2):
            out.write(result_json + "\n")
            out.flush()
            processed_count += 1
            
            try:
                result = json.loads(result_json)
                if result.get('status') == 'success':
                    successful += 1
                else:
                    failed += 1
            except:
                failed += 1
                logger.error(f"Failed to parse JSON result for record {processed_count}")
            
            if processed_count % 10 == 0:
                print(f"Processed {processed_count}/{len(source_urls)} papers (Success: {successful}, Failed: {failed})")
    
    print(f"\nComplete!")
    print(f"  URLs in CSV: {len(source_urls)}")
    print(f"  Records processed: {processed_count}")
    print(f"  Success: {successful}")
    print(f"  Failed: {failed}")
    
    if processed_count != len(source_urls):
        print(f"\n⚠️  WARNING: Processed {processed_count} but expected {len(source_urls)}")
        print(f"  Missing: {len(source_urls) - processed_count} records")
    
    print(f"\nOutput saved to llm_data_biopub.jsonl")
    print(f"Errors logged to scraper_errors.log")

    if failed > 0:
        analyze_failures()


if __name__ == "__main__":
    main()