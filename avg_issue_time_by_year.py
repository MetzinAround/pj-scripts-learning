import requests
import config as conf
import sys
from datetime import datetime

# Configuration - modify these for different repos
OWNER = 'campus-experts'
REPO = 'being-an-expert'
TOKEN = conf.api_token

if not TOKEN:
    print("ERROR: No token found in environment variables")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python avg_issue_time_by_year.py <year>")
    print("Example: python avg_issue_time_by_year.py 2024")
    sys.exit(1)

try:
    target_year = int(sys.argv[1])
except ValueError:
    print(f"ERROR: '{sys.argv[1]}' is not a valid year")
    sys.exit(1)

print("Token found and loaded successfully")

headers = {'Authorization': f'token {TOKEN}'}
issue_list_url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues?state=all&per_page=100'
issues = []
page = 1

print(f"Fetching issues from {OWNER}/{REPO}...")
while True:
    print(f"Page {page}...", end=" ", flush=True)
    r = requests.get(issue_list_url + f"&page={page}", headers=headers)
    
    if r.status_code != 200:
        print(f"\nERROR: API returned {r.status_code}")
        try:
            print(f"Response: {r.json()}")
        except Exception:
            print(f"Response: {r.text}")
        sys.exit(1)
    
    data = r.json()
    if not data:
        print("\nNo more data")
        break
    print(f"({len(data)} issues)")
    issues += data
    page += 1

print(f"\nTotal issues fetched: {len(issues)}")

total_days = 0
count = 0
skipped_quick_close = 0

for issue in issues:
    if 'pull_request' not in issue:  # filter out PRs
        created = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        
        # Check if issue was created in the target year
        if created.year != target_year:
            continue
        
        # Only analyze closed issues
        if issue['closed_at'] is None:
            continue
        
        closed = datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
        days_open = (closed - created).total_seconds() / (60 * 60 * 24)
        
        # Exclude issues closed within 2 weeks (14 days)
        if days_open < 14:
            skipped_quick_close += 1
            continue
        
        total_days += (closed - created).total_seconds()
        count += 1

avg_seconds = total_days / count if count else 0
avg_days = avg_seconds / (60 * 60 * 24)

print(f"\nYear: {target_year}")
print(f"Issues analyzed: {count}")
print(f"Issues excluded (closed within 2 weeks): {skipped_quick_close}")
if count > 0:
    print(f"Average open time for closed issues: {avg_days:.2f} days")
else:
    print("No issues found for this year matching criteria")
