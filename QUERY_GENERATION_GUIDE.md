# Boolean Query Generation Guide

Complete guide for generating and using Boolean search queries with `dice_complete.py`.

## Overview

`dice_complete.py` now reads the Boolean search query from `Dice_string.txt` instead of hardcoding it. This allows you to:
- ✅ Generate queries from job descriptions using ChatGPT
- ✅ Manually edit and customize queries
- ✅ Use different queries for different searches

## File Structure

```
Data_Resume_Harvesting_Script/
├── job_description.txt          # Input: Job requirements
├── dice_api.py                  # Generates Boolean query using ChatGPT
├── Dice_string.txt             # Output: Generated Boolean query
├── dice_complete.py            # Main script (reads Dice_string.txt)
└── generate_dice_query.sh      # Helper script to generate query
```

## Method 1: Using ChatGPT (Automatic)

### Prerequisites
1. OpenAI API key
2. Create `.env` file:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

### Steps
1. **Edit job description**:
   ```bash
   nano job_description.txt
   # Add your job requirements
   ```

2. **Generate query**:
   ```bash
   python dice_api.py
   # or
   ./generate_dice_query.sh
   ```

3. **Run scraper**:
   ```bash
   python dice_complete.py --debug --pages 3
   ```

### Example Output
```
Generating Dice query using ChatGPT API...
✓ Dice query generated successfully!
✓ Output saved to: Dice_string.txt

Generated Query:
(Appian OR "Appian Developer" ...) AND (SAIL OR "Appian UI" ...) AND ...

API Usage:
  Model: gpt-3.5-turbo
  Tokens used: 234
```

## Method 2: Manual Editing

### Steps
1. **Edit query directly**:
   ```bash
   nano Dice_string.txt
   ```

2. **Format guidelines**:
   ```
   (Term1 OR "Term Variation" OR "Term Synonym") AND
   (Term2 OR "Term2 Variation") AND
   (Term3 OR Term4 OR Term5)
   ```

3. **Run scraper**:
   ```bash
   python dice_complete.py --debug --pages 3
   ```

### Query Format Tips
- ✅ Use `OR` within skill groups
- ✅ Use `AND` between skill groups
- ✅ Use quotes for multi-word terms: `"Appian Developer"`
- ✅ Include synonyms: `(AWS OR "Amazon Web Services" OR "Cloud Integration")`
- ✅ Keep it comprehensive but focused

## Method 3: Use Default Query

If `Dice_string.txt` doesn't exist, `dice_complete.py` will:
1. Look for `job_description.txt` and try to generate query
2. If that fails, use the default Appian Developer query

## How dice_complete.py Loads the Query

```python
def load_boolean_query():
    # Priority 1: Read from Dice_string.txt
    if Dice_string.txt exists:
        return query_from_file

    # Priority 2: Generate from job_description.txt
    if job_description.txt exists:
        return generate_with_chatgpt()

    # Priority 3: Use default
    return default_appian_query

BOOLEAN = load_boolean_query()  # Loaded once at startup
```

## Sample job_description.txt

```
An Appian Architect designs, builds, and maintains business process
automation solutions using the Appian low-code platform.

Key Skills & Qualifications:
• Appian Platform: Strong proficiency in Appian UI and RPA
• Low-Code Development: Experience with low-code principles
• Business Process Management (BPM): Understanding of BPM concepts
• Software Development: Java/J2EE, JavaScript, or C#
• Cloud: Mandatory AWS and AWS services
```

## Sample Dice_string.txt Output

```
(Appian OR "Appian Developer" OR "Appian Engineer" OR "Appian Architect") AND
(SAIL OR "Appian UI" OR "Appian RPA" OR "Appian Integration") AND
("Business Process Management" OR BPM OR "process automation") AND
(Java OR J2EE OR "JavaScript" OR C# OR ".NET") AND
("low-code" OR "low code" OR "low-code development") AND
(workflow OR "process modeling" OR "workflow automation") AND
(integration OR API OR "third-party systems" OR "REST API") AND
(SQL OR "data modeling" OR "data management" OR "database") AND
(AWS OR "Amazon Web Services" OR "Cloud Integration" OR "AWS services")
```

## Verification

Check which query is being used:
```bash
# View current query
cat Dice_string.txt

# Test loading
python -c "
with open('Dice_string.txt', 'r') as f:
    query = f.read().strip()
    print(f'Query length: {len(query)} chars')
    print(f'Preview: {query[:100]}...')
"

# Run with debug to see query being used
python dice_complete.py --debug --pages 1
# Look for: "✅ Loaded Boolean query from Dice_string.txt"
```

## Troubleshooting

### Query not loading
```bash
# Check if file exists
ls -la Dice_string.txt

# Check file contents
cat Dice_string.txt

# Check file is not empty
[ -s Dice_string.txt ] && echo "File has content" || echo "File is empty"
```

### Generate new query
```bash
# Using API
python dice_api.py

# Or manually create
echo '(Appian OR "Appian Developer") AND (SAIL OR "Appian UI")' > Dice_string.txt
```

### API key issues
```bash
# Check .env file
cat .env

# Verify API key format
# Should be: OPENAI_API_KEY=sk-...
```

## Best Practices

1. **Keep queries focused** - Don't include too many terms
2. **Test queries** - Run with `--debug` to verify results
3. **Version control** - Save different queries for different searches
4. **Iterate** - Refine query based on search results

## Example Workflow

```bash
# 1. Update job description
nano job_description.txt

# 2. Generate query (if you have API key)
python dice_api.py

# 3. Review and edit query
nano Dice_string.txt

# 4. Run scraper
python dice_complete.py --debug --pages 3

# 5. Check results
ls -la dice_candidates_*.xlsx

# 6. Open Excel and filter candidates
open dice_candidates_*.xlsx
```

## Advanced: Multiple Queries

Save different queries for different roles:

```bash
# Backend developer
cp Dice_string.txt queries/backend_developer.txt

# Frontend developer
cp queries/frontend_developer.txt Dice_string.txt

# Run scraper
python dice_complete.py --pages 5
```

## Summary

| Method | Pros | Cons |
|--------|------|------|
| ChatGPT API | Automatic, comprehensive | Requires API key, costs money |
| Manual Edit | Full control, free | Time-consuming, requires expertise |
| Default | Always works | Generic, may not fit specific needs |

✅ **Recommended**: Use ChatGPT to generate, then manually refine the query!
