import requests
import json
import time
import multiprocessing as mp
from functools import partial

def get_study_metadata(study_id):
    """Get metadata for a single study from NASA OSDR API."""
    url = f"https://osdr.nasa.gov/osdr/data/osd/meta/{study_id}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            study_key = f'OSD-{study_id}'
            study = data['study'][study_key]['studies'][0]
            
            return {
                'study_id': study_key,
                'title': study.get('title'),
                'description': study.get('description'),
                'submission_date': study.get('submissionDate'),
                'release_date': study.get('publicReleaseDate'),
                'factors': [f.get('factorName') for f in study.get('factors', [])],
                'protocols': [
                    {
                        'name': p.get('name'),
                        'description': p.get('description')
                    }
                    for p in study.get('protocols', [])
                ],
                'publications': [
                    {
                        'title': pub.get('title'),
                        'authors': pub.get('authorList'),
                        'doi': pub.get('doi'),
                        'doi_url': f"https://doi.org/{pub.get('doi')}" if pub.get('doi') else None,
                        'pmid': pub.get('pubMedID'),
                        'pmid_url': f"https://pubmed.ncbi.nlm.nih.gov/{pub.get('pubMedID')}/" if pub.get('pubMedID') else None
                    }
                    for pub in study.get('publications', [])
                ],
                'people': [
                    f"{p.get('firstName')} {p.get('lastName')}"
                    for p in study.get('people', [])
                ],
                'comments': {
                    c.get('name'): c.get('value')
                    for c in study.get('comments', [])
                }
            }
        else:
            return None
            
    except Exception as e:
        return None


def check_study_exists(study_id):
    """Check if a study ID exists and return it if valid."""
    url = f"https://osdr.nasa.gov/osdr/data/osd/files/{study_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return study_id
    except:
        pass
    return None


def main():
    MAX_WORKERS = 8
    
    print("Step 1: Finding all valid study IDs (using parallel requests)...\n")
    
    # Check study IDs in parallel
    with mp.Pool(processes=MAX_WORKERS) as pool:
        potential_ids = range(1, 750)
        study_ids = []
        
        for result in pool.imap_unordered(check_study_exists, potential_ids, chunksize=20):
            if result:
                study_ids.append(str(result))
                if len(study_ids) % 50 == 0:
                    print(f"Found {len(study_ids)} studies so far...")
    
    study_ids.sort(key=int)
    print(f"\nFound {len(study_ids)} total studies\n")
    
    if not study_ids:
        print("No study IDs found. Exiting.")
        return
    
    print("Step 2: Fetching metadata for all studies (using parallel requests)...\n")
    
    studies_hashtable = {}
    successful = 0
    failed = 0
    
    with mp.Pool(processes=MAX_WORKERS) as pool:
        for i, metadata in enumerate(pool.imap_unordered(get_study_metadata, study_ids, chunksize=5), 1):
            if metadata:
                studies_hashtable[metadata['study_id']] = metadata
                successful += 1
                print(f"[{i}/{len(study_ids)}] ✓ {metadata['study_id']}: {metadata['title'][:50]}...")
            else:
                failed += 1
                print(f"[{i}/{len(study_ids)}] ✗ Failed")
            
            if i % 50 == 0:
                print(f"\n--- Progress: {i}/{len(study_ids)} ({successful} success, {failed} failed) ---\n")
    
    print(f"\nComplete!")
    print(f"  Total studies found: {len(study_ids)}")
    print(f"  Successfully scraped: {successful}")
    print(f"  Failed: {failed}")
    print(f"  In hashtable: {len(studies_hashtable)}")
    
    with open('osdr_all_studies.json', 'w', encoding='utf-8') as f:
        json.dump(studies_hashtable, f, indent=2, ensure_ascii=False)
    
    print(f"\nData saved to osdr_all_studies.json")


if __name__ == "__main__":
    main()