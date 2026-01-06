import pandas as pd
import requests
from time import sleep

def lookup_creator_in_library_of_congress(name):
    try:
        url = "https://id.loc.gov/authorities/names/suggest2"
        params = {'q': name, 'count': 3}
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('hits'):
            best_match = data['hits'][0]
            return {
                'authority_uri': best_match.get('uri', ''),
                'official_name': best_match.get('suggestLabel', ''),
                'confidence': 'HIGH' if len(data['hits']) == 1 else 'MEDIUM'
            }
        
        return None
    
    except Exception as e:
        print(f"  Warning: Could not look up '{name[:40]}'")
        return None

def lookup_subject_in_library_of_congress(subject):
    try:
        url = "https://id.loc.gov/authorities/subjects/suggest2"
        params = {'q': subject, 'count': 3}
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('hits'):
            best_match = data['hits'][0]
            return {
                'authority_uri': best_match.get('uri', ''),
                'official_term': best_match.get('suggestLabel', ''),
                'confidence': 'HIGH' if len(data['hits']) == 1 else 'MEDIUM'
            }
        
        return None
    
    except Exception as e:
        print(f"  Warning: Could not look up '{subject[:40]}'")
        return None

def reconcile_all_creators():
    print("\n" + "="*60)
    print("MATCHING CREATOR NAMES")
    print("="*60 + "\n")
    
    df = pd.read_csv("data/raw_collections.csv")
    
    creators = df[df['creator'].notna()]['creator'].unique()
    creators = [str(c).strip() for c in creators if len(str(c).strip()) > 2]
    
    print(f"Found {len(creators)} unique creators")
    print("Checking first 30 (this takes ~15 seconds)...\n")
    
    results = []
    
    for i, creator in enumerate(creators[:30], 1):
        print(f"[{i}/30] {creator[:60]}...")
        
        match = lookup_creator_in_library_of_congress(creator)
        
        if match:
            results.append({
                'original_name': creator,
                'official_name': match['official_name'],
                'authority_uri': match['authority_uri'],
                'confidence': match['confidence']
            })
        else:
            results.append({
                'original_name': creator,
                'official_name': '',
                'authority_uri': '',
                'confidence': 'NO_MATCH'
            })
        
        sleep(0.5)
    
    df_results = pd.DataFrame(results)
    df_results.to_csv("outputs/reconciled_creators.csv", index=False)
    
    matched = len([r for r in results if r['confidence'] != 'NO_MATCH'])
    print(f"\n✅ Done!")
    print(f"   Matched: {matched}/30")
    print(f"   Saved to: outputs/reconciled_creators.csv")

def reconcile_all_subjects():
    print("\n" + "="*60)
    print("MATCHING SUBJECT TERMS")
    print("="*60 + "\n")
    
    df = pd.read_csv("data/raw_collections.csv")
    
    all_subjects = set()
    for subj in df[df['subject'].notna()]['subject']:
        subj_str = str(subj)
        parts = [s.strip() for s in subj_str.replace(';', ',').split(',')]
        all_subjects.update([p for p in parts if len(p) > 2])
    
    subjects_list = list(all_subjects)[:20]
    
    print(f"Found {len(all_subjects)} unique subjects")
    print(f"Checking first 20 (this takes ~10 seconds)...\n")
    
    results = []
    
    for i, subject in enumerate(subjects_list, 1):
        print(f"[{i}/20] {subject[:60]}...")
        
        match = lookup_subject_in_library_of_congress(subject)
        
        if match:
            results.append({
                'original_subject': subject,
                'official_term': match['official_term'],
                'authority_uri': match['authority_uri'],
                'confidence': match['confidence']
            })
        else:
            results.append({
                'original_subject': subject,
                'official_term': '',
                'authority_uri': '',
                'confidence': 'NO_MATCH'
            })
        
        sleep(0.5)
    
    df_results = pd.DataFrame(results)
    df_results.to_csv("outputs/reconciled_subjects.csv", index=False)
    
    matched = len([r for r in results if r['confidence'] != 'NO_MATCH'])
    print(f"\n✅ Done!")
    print(f"   Matched: {matched}/20")
    print(f"   Saved to: outputs/reconciled_subjects.csv")

if __name__ == "__main__":
    print("🔗 Authority Reconciliation Tool")
    print("Matching names and subjects to Library of Congress\n")
    
    reconcile_all_creators()
    reconcile_all_subjects()
    
    print("\n" + "="*60)
    print("ALL DONE!")
    print("="*60)
