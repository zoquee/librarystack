import pandas as pd
import re
from datetime import datetime

def check_record_quality(record, record_number):
    problems = []
    record_id = record.get('identifier', f'row_{record_number}')
    
    required_fields = ['identifier', 'title', 'creator', 'date']
    for field in required_fields:
        value = record.get(field)
        if pd.isna(value) or str(value).strip() == '':
            problems.append({
                'record_id': record_id,
                'field': field,
                'problem': 'Missing required field',
                'severity': 'CRITICAL',
                'current_value': '',
                'fix_suggestion': '[Needs manual review]'
            })
    
    date_value = record.get('date')
    if not pd.isna(date_value):
        date_str = str(date_value).strip()
        
        if '-00-' in date_str or '-00' in date_str:
            problems.append({
                'record_id': record_id,
                'field': 'date',
                'problem': 'Invalid date (has 00)',
                'severity': 'HIGH',
                'current_value': date_str,
                'fix_suggestion': '[Needs manual review]'
            })
        
        if '/' in date_str:
            problems.append({
                'record_id': record_id,
                'field': 'date',
                'problem': 'Wrong date format (use YYYY-MM-DD)',
                'severity': 'HIGH',
                'current_value': date_str,
                'fix_suggestion': date_str.replace('/', '-')
            })
    
    lang_value = record.get('language')
    if not pd.isna(lang_value):
        lang_str = str(lang_value).strip().lower()
        
        if lang_str in ['en', 'english']:
            problems.append({
                'record_id': record_id,
                'field': 'language',
                'problem': 'Non-standard language code',
                'severity': 'MEDIUM',
                'current_value': lang_str,
                'fix_suggestion': 'eng'
            })
    
    creator_value = record.get('creator')
    if not pd.isna(creator_value):
        creator_str = str(creator_value).strip()
        
        if re.search(r'\b(dr\.?|prof\.?)\s', creator_str, re.IGNORECASE):
            fixed = re.sub(r'\b(dr\.?|prof\.?)\s', '', creator_str, flags=re.IGNORECASE)
            problems.append({
                'record_id': record_id,
                'field': 'creator',
                'problem': 'Contains title prefix (Dr., Prof.)',
                'severity': 'MEDIUM',
                'current_value': creator_str,
                'fix_suggestion': fixed.strip()
            })
        
        if creator_str.islower() or creator_str.isupper():
            problems.append({
                'record_id': record_id,
                'field': 'creator',
                'problem': 'Inconsistent capitalization',
                'severity': 'MEDIUM',
                'current_value': creator_str,
                'fix_suggestion': creator_str.title()
            })
    
    return problems

def validate_all_records():
    print("Loading data...")
    df = pd.read_csv("data/raw_collections.csv")
    print(f"Loaded {len(df)} records\n")
    
    print("Checking quality...")
    all_problems = []
    
    for index, record in df.iterrows():
        problems = check_record_quality(record, index)
        all_problems.extend(problems)
        
        if (index + 1) % 100 == 0:
            print(f"  Checked {index + 1}/{len(df)} records...")
    
    print(f"\nDone checking!\n")
    
    if len(all_problems) == 0:
        print("✅ NO PROBLEMS FOUND! Dataset is clean.")
        return
    
    df_problems = pd.DataFrame(all_problems)
    df_problems.to_csv("outputs/audit_report.csv", index=False)
    
    print(f"{'='*60}")
    print(f"AUDIT REPORT")
    print(f"{'='*60}")
    print(f"Total problems found: {len(all_problems)}")
    print(f"Saved to: outputs/audit_report.csv\n")
    
    print("Problems by severity:")
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = len([p for p in all_problems if p['severity'] == severity])
        if count > 0:
            print(f"  {severity:10s}: {count:4d}")
    
    print("\nProblems by field:")
    field_counts = {}
    for problem in all_problems:
        field = problem['field']
        field_counts[field] = field_counts.get(field, 0) + 1
    
    for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {field:15s}: {count:4d}")

if __name__ == "__main__":
    validate_all_records()
