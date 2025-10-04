import requests
import csv
import json
from bs4 import BeautifulSoup
import time
from datetime import datetime, timezone
import hashlib

headers = {'User-Agent': 'Mozilla/5.0'}

def get_meta(soup, name):
    tag = soup.find('meta', {'name': name})
    return tag['content'] if tag else None

def get_text(elem):
    return elem.get_text(strip=True) if elem else None

def count_words(text):
    return len(text.split()) if text else 0

def scrape_paper(url):
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 429:
        time.sleep(int(response.headers.get('Retry-After', 60)))
        return scrape_paper(url)
    
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    doi = get_meta(soup, 'citation_doi')
    pmid = get_meta(soup, 'citation_pmid')
    missing_fields = []
    
    authors = []
    author_tags = soup.find_all('meta', {'name': 'citation_author'})
    affiliation_tags = soup.find_all('meta', {'name': 'citation_author_institution'})
    for i, author_tag in enumerate(author_tags):
        authors.append({
            'name': author_tag['content'],
            'affiliation': affiliation_tags[i]['content'] if i < len(affiliation_tags) else None,
            'is_corresponding': False
        })
    
    abstract_section = soup.find('section', class_='abstract')
    abstract_text = get_text(abstract_section)
    if abstract_text:
        abstract_text = abstract_text.replace('Abstract', '', 1).strip()
    
    sections = []
    total_words = 0
    main_article = soup.find('article')
    if main_article:
        for section in main_article.find_all('section', recursive=False):
            heading = section.find(['h2', 'h3'], class_='pmc_sec_title')
            text = ' '.join([p.get_text(strip=True) for p in section.find_all('p')])
            if text:
                word_count = count_words(text)
                total_words += word_count
                sections.append({
                    'heading': get_text(heading),
                    'level': 2 if heading and heading.name == 'h2' else 3,
                    'text': text,
                    'word_count': word_count
                })
    
    references = []
    ref_list = soup.find('section', class_='ref-list')
    if ref_list:
        for idx, ref in enumerate(ref_list.find_all('li'), 1):
            cite = ref.find('cite')
            if cite:
                references.append({
                    'id': str(idx),
                    'text': get_text(cite),
                    'doi': None,
                    'pmid': None
                })
    
    figures = []
    tables = []
    for fig in soup.find_all('figure', class_='fig'):
        caption = fig.find('figcaption')
        img = fig.find('img')
        fig_id = fig.get('id', '')
        
        if 'table' in fig_id.lower():
            tables.append({
                'id': fig_id,
                'label': fig_id,
                'caption': get_text(caption)
            })
        else:
            figures.append({
                'id': fig_id,
                'label': fig_id,
                'caption': get_text(caption),
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
    if not abstract_text:
        missing_fields.append('abstract')
    
    return {
        'paper_id': doi if doi else hashlib.md5(url.encode()).hexdigest(),
        'source_url': url,
        'scraped_at': datetime.now(timezone.utc).isoformat(),
        'scrape_status': {
            'success': True,
            'partial_failure': len(missing_fields) > 0,
            'missing_fields': missing_fields
        },
        'metadata': {
            'title': get_meta(soup, 'citation_title'),
            'authors': authors,
            'journal': {
                'name': get_meta(soup, 'citation_journal_title'),
                'publisher': get_meta(soup, 'citation_publisher'),
                'issn': get_meta(soup, 'citation_issn')
            },
            'identifiers': {
                'doi': doi,
                'pmid': pmid,
                'pmcid': None
            },
            'publication': {
                'date': get_meta(soup, 'citation_publication_date'),
                'volume': get_meta(soup, 'citation_volume'),
                'issue': get_meta(soup, 'citation_issue'),
                'pages': get_meta(soup, 'citation_firstpage')
            },
            'keywords': [],
            'mesh_terms': []
        },
        'abstract': {
            'text': abstract_text,
            'structured': {}
        },
        'sections': sections,
        'references': references,
        'figures': figures,
        'tables': tables,
        'supplementary': {
            'funding': funding,
            'acknowledgments': acknowledgments,
            'conflicts_of_interest': None,
            'data_availability': None
        },
        'metrics': {
            'total_word_count': total_words,
            'section_count': len(sections),
            'reference_count': len(references),
            'figure_count': len(figures),
            'table_count': len(tables)
        }
    }

with open('SB_publication_PMC.csv', newline='') as csvfile:
    total_rows = sum(1 for row in csvfile) - 1
    csvfile.seek(0)
    
    with open('papers.jsonl', 'w', encoding='utf-8') as outfile:
        reader = csv.reader(csvfile)
        next(reader)
        
        processed = 0
        successful = 0
        failed = 0
        
        for row in reader:
            if len(row) <= 1 or not row[1].startswith('http'):
                continue
                
            url = row[1].strip()
            processed += 1
            
            try:
                paper = scrape_paper(url)
                outfile.write(json.dumps(paper, ensure_ascii=False) + '\n')
                successful += 1
                print(f"[{processed}/{total_rows}] SUCCESS: {paper['metadata']['title'][:60]}")
                time.sleep(1)
            except Exception as e:
                failed += 1
                print(f"[{processed}/{total_rows}] FAILED: {url} - {str(e)[:60]}")
                outfile.write(json.dumps({
                    'paper_id': hashlib.md5(url.encode()).hexdigest(),
                    'source_url': url,
                    'scraped_at': datetime.now(timezone.utc).isoformat(),
                    'scrape_status': {
                        'success': False,
                        'partial_failure': False,
                        'missing_fields': ['all'],
                        'error': str(e)
                    }
                }, ensure_ascii=False) + '\n')

print(f"\nComplete: {successful} successful, {failed} failed out of {processed} total")