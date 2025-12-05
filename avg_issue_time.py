import requests
import config as conf
import sys
from datetime import datetime

OWNER = 'campus-experts'
REPO = 'becoming-an-expert'
TOKEN = conf.api_token

# Filter by specific usernames (set to None or empty list to disable filtering)
FILTER_USERNAMES = ["Dsniels", "redhatgamer", "Henninglar", "Darshan808", "nisalgunawardhana", "wizziez", "Nimastic", "Kile", "Frost-Lord", "tobidelly", "Spirizeon", "hichemfantar", "EncryptEx", "AlperenOvak", "mohamedaminebentayeb", "AlfredAR8", "Dav082004", "sethidhruv188", "ybedoyab", "SantyMsss", "KhuranaSanchit", "Yusadem131", "UtkarshJaiswal1406", "fit-alpha-coma", "cyu60", "DVidal1205", "Nalito", "KaalkidanSahele", "MuhammadAdilMemon", "nityaa3009", "sakshamgurbhele", "mohanamisra", "TheRyanMajd", "pmj-chosim", "Imayeer", "johandraew", "ashleymawoyo", "JocelynVelarde", "AnenIsaac"]

# Filter by issue title (set to None to disable filtering)
FILTER_TITLE = "[REQUEST] Training Changes Requested"  # Only analyze issues with this exact title

if not TOKEN:
    print("ERROR: No token found in environment variables")
    sys.exit(1)

print("Token found and loaded successfully")

# Convert usernames to lowercase for case-insensitive matching
filter_usernames_lower = [u.lower() for u in FILTER_USERNAMES] if FILTER_USERNAMES else None

if filter_usernames_lower:
    user_filter = f" by users: {', '.join(FILTER_USERNAMES)}"
else:
    user_filter = ""

if FILTER_TITLE:
    title_filter = f" with title '{FILTER_TITLE}'"
else:
    title_filter = ""

headers = {'Authorization': f'token {TOKEN}'}
issue_list_url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues?state=closed&per_page=100'
issues = []
page = 1

print(f"Fetching issues from {OWNER}/{REPO}{user_filter}{title_filter}...")
while page <= 2:
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

for issue in issues:
    if 'pull_request' not in issue:  # filter out PRs
        # Apply username filter
        if filter_usernames_lower:
            issue_author = issue.get('user', {}).get('login', '').lower()
            if issue_author not in filter_usernames_lower:
                continue
        
        # Apply title filter
        if FILTER_TITLE:
            issue_title = issue.get('title', '')
            if issue_title != FILTER_TITLE:
                continue
        
        created = datetime.strptime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        closed = datetime.strptime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
        total_days += (closed - created).total_seconds()
        count += 1

avg_seconds = total_days / count if count else 0
avg_days = avg_seconds / (60 * 60 * 24)
print(f"\nIssues analyzed: {count}")
print(f"Average open time for closed issues: {avg_days:.2f} days")