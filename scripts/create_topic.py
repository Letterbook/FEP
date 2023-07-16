from argparse import ArgumentParser
from tools import FepFile

parser = ArgumentParser("Create topic for FEP")
parser.add_argument("fep", help="slug of the FEP")
args = parser.parse_args()

fep_file = FepFile(args.fep)

fep_file.write()

url = f"https://codeberg.org/fediverse/fep/src/branch/main/fep/{args.fep}/fep-{args.fep}.md"


body = f"""
Hello!

This is a discussion thread for the proposed [FEP-{args.fep}: {fep_file.title}]({url}).
Please use this thread to discuss the proposed FEP and any potential problems
or improvements that can be addressed.

__Summary__

{fep_file.summary}
"""

print("Create a new topic on https://socialhub.activitypub.rocks/c/standards/fep/54")
print("with title")
print(f"       FEP-{args.fep}: {fep_file.title}")
print("and tags")
print(f"       fep, fep-{args.fep}, draft")
print("and body")
print(body)
print("")
discussionsTo = fep_file.parsed_frontmatter["discussionsTo"]
print(f"After creating the issue add a link to the tracking issue {discussionsTo}")
