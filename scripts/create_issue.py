from argparse import ArgumentParser
from datetime import date, timedelta
from tools import FepFile

import json
from urllib.request import Request, urlopen

parser = ArgumentParser("Create tracking issue for FEP")
parser.add_argument("fep", help="slug of the FEP")
args = parser.parse_args()

fep_file = FepFile(args.fep)

if "discussionsTo" in fep_file.parsed_frontmatter:
    print("File already has discussionsTo")
    exit(1)

title = f"[TRACKING] FEP-{args.fep}: {fep_file.title}"

date_received = date.fromisoformat(fep_file.parsed_frontmatter["dateReceived"])

date1 = date_received.isoformat()
date2 = (date_received + timedelta(days=365)).isoformat()

body = f"""
The [proposal](https://codeberg.org/fediverse/fep/src/branch/main/{fep_file.filename}) has been received. Thank you!

This issue tracks discussions and updates to the proposal during the `DRAFT` period.

Please post links to relevant discussions as comment to this issue.

`dateReceived`: {date1}

If no further actions are taken, the proposal may be set by editors to `WITHDRAWN` on {date2} (in 1 year).
"""

with open("scripts/config.json") as f:
    config = json.load(f)

request = Request(
    f"https://codeberg.org/api/v1/repos/{config['owner']}/{config['repo']}/issues"
)
request.add_header("Content-Type", "application/json; charset=utf-8")
request_body = json.dumps({"title": title, "body": body}).encode("utf-8")
request.add_header("authorization", f"Bearer {config['token']}")
request.add_header("Content-Length", len(request_body))
request.data = request_body
response = urlopen(request)


issue_url = json.loads(response.read())["html_url"]

fep_file.frontmatter.append(f"discussionsTo: {issue_url}")
fep_file.write()

print(f"Issue url: {issue_url}")
