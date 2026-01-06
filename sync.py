import pandas as pd
import json
from datetime import datetime

def load_fixes_from_audit_report():
    print("Loading fixes from audit report...")
    
    df = pd.read_csv("outputs/audit_report.csv")
    
    df_fixable = df[df['fix_suggestion'] != '[Needs manual review]']
    
    print(f"Found {len(df_fixable)} fixable problems\n")
    
    return df_fixable

def preview_changes(fixes_df):
    print("="*60)
    print("PREVIEW OF CHANGES (DRY RUN)")
    print("="*60 + "\n")
    
    print(f"Total changes to make: {len(fixes_df)}\n")
    
    print("First 10 changes:\n")
    for i, row in fixes_df.head(10).iterrows():
        print(f"{i+1}. Record: {row['record_id']}")
        print(f"   Field: {row['field']}")
        print(f"   Current: {row['current_value']}")
        print(f"   Will change to: {row['fix_suggestion']}")
        print()
    
    if len(fixes_df) > 10:
        print(f"... and {len(fixes_df) - 10} more changes\n")

def apply_fixes(fixes_df, dry_run=True):
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - Not making actual changes\n")
        preview_changes(fixes_df)
        return
    
    print("\n🔧 APPLYING FIXES...\n")
    
    df_original = pd.read_csv("data/raw_collections.csv")
    df_updated = df_original.copy()
    
    changes_log = []
    
    for _, fix in fixes_df.iterrows():
        record_id = fix['record_id']
        field = fix['field']
        new_value = fix['fix_suggestion']
        
        mask = df_updated['identifier'] == record_id
        
        if mask.any():
            old_value = df_updated.loc[mask, field].values[0]
            df_updated.loc[mask, field] = new_value
            
            changes_log.append({
                'timestamp': datetime.now().isoformat(),
                'record_id': record_id,
                'field': field,
                'old_value': str(old_value),
                'new_value': str(new_value),
                'status': 'SUCCESS'
            })
            
            print(f"✓ Updated {record_id} - {field}")
    
    df_updated.to_csv("outputs/cleaned_collections.csv", index=False)
    
    with open("outputs/update_log.json", "w") as f:
        json.dump(changes_log, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ UPDATE COMPLETE")
    print(f"{'='*60}")
    print(f"Changes made: {len(changes_log)}")
    print(f"Updated data saved to: outputs/cleaned_collections.csv")
    print(f"Change log saved to: outputs/update_log.json")

if __name__ == "__main__":
    print("🔄 Bulk Update Tool\n")
    
    fixes = load_fixes_from_audit_report()
    
    apply_fixes(fixes, dry_run=True)
    
    print("\n" + "="*60)
    print("This was a DRY RUN - no changes were made")
    print("="*60)

