import requests
import config as conf

OWNER = 'campus-experts'
REPO = 'becoming-an-expert'
TOKEN = conf.api_token 

headers = {'Authorization': f'token {TOKEN}'}
issue_list_url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues?state=closed&per_page=100'
issues = []
page = 1

while True:
    r = requests.get(issue_list_url + f"&page={page}", headers=headers)
    data = r.json()
    if not data:
        break
    issues += data
    page += 1

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