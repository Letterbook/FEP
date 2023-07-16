from argparse import ArgumentParser
from datetime import date, timedelta
from tools import FepFile


import json
import requests

parser = ArgumentParser("Pullrequest")
parser.add_argument("pr", help="Pull request id")
args = parser.parse_args()

with open("ISSUE_TEMPLATE/config.json") as f:
    config = json.load(f)
print(
    f"https://codeberg.org/api/v1/repos/{config['owner']}/{config['repo']}/pulls/{args.pr}"
)
response = requests.get(
    f"https://codeberg.org/api/v1/repos/{config['owner']}/{config['repo']}/pulls/{args.pr}",
    headers={"authorization": f"Bearer {config['token']}"},
)

print(response)
print(response.text)


print(json.dumps(response.json(), indent=2))
