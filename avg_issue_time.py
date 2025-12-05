import requests
import config as conf
import sys

OWNER = 'campus-experts'
REPO = 'becoming-an-expert'
TOKEN = conf.api_token

if not TOKEN:
    print("ERROR: No token found in environment variables")
    sys.exit(1)

print(f"Token found: {TOKEN[:8]}...")
headers = {'Authorization': f'token {TOKEN}'}
issue_list_url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues?state=closed&per_page=100'
issues = []
page = 1

print(f"Fetching issues from {OWNER}/{REPO}...")
while page <= 4:
    print(f"Page {page}...", end=" ", flush=True)
    r = requests.get(issue_list_url + f"&page={page}", headers=headers)
    
    if r.status_code != 200:
        print(f"\nERROR: API returned {r.status_code}")
        print(f"Response: {r.json()}")
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
from datetime import datetime

for issue in issues:
    if 'pull_request' not in issue:  # filter out PRs
        created = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        closed = datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
        total_days += (closed - created).total_seconds()
        count += 1

avg_seconds = total_days / count if count else 0
avg_days = avg_seconds / (60 * 60 * 24)
print(f"Average open time for closed issues: {avg_days:.2f} days")