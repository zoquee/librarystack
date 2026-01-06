# LibraryStack — Metadata QA & Sync Tool

Digital collection metadata validation and bulk update engine with authority reconciliation.

## What It Does

1. **Extracts** metadata from Internet Archive (500 records)
2. **Validates** against library metadata standards
3. **Reconciles** names/subjects against Library of Congress authorities
4. **Updates** records with fixes (dry-run supported)
5. **Tracks** all changes with audit trails

## Quick Start

### Setup
```bash
cd ~/librarystack
source venv/bin/activate

# Step 1: Get data
python extract.py

# Step 2: Check quality
python validate.py

# Step 3: Match to authorities (takes ~30 seconds)
python reconcile.py

# Step 4: Preview fixes
python sync.py

What Gets Validated
Required fields: identifier, title, creator, date

Date format: ISO 8601 (YYYY-MM-DD)

Language codes: ISO 639-2 (3-letter codes like 'eng')

Creator names: Capitalization, title prefixes (Dr., Prof.)

Subject terms: Delimiter consistency

Authority Reconciliation
Creator names → Library of Congress Name Authority File (LCNAF)

Subject terms → Library of Congress Subject Headings (LCSH)

Uses real LC Suggest APIs to match against official controlled vocabularies
