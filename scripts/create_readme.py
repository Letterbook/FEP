from tools import FepFile, get_fep_ids

fep_files = [FepFile(fep) for fep in get_fep_ids()]
fep_files = reversed(fep_files)
fep_files = sorted(fep_files, key=lambda x: x.parsed_frontmatter["dateReceived"])

result = []


def build_url_link(url):
    url_number = url.split("/")[-1]
    return f"[#{url_number}]({url})"


for fep in fep_files:
    link = f"[FEP-{fep.fep}: {fep.title}](./{fep.filename})"
    parsed = fep.parsed_frontmatter

    if "discussionsTo" in parsed:
        url = parsed["discussionsTo"]
        urls = url.split(", ")
        discussions = " ".join(build_url_link(url) for url in urls)
    else:
        discussions = ""

    if "dateFinalized" in parsed:
        date_final = parsed["dateFinalized"]
    else:
        date_final = "-"
    result.append(
        f"""| {link} | `{parsed["status"]}` | {discussions} | {parsed["dateReceived"]} | {date_final} |\n"""
    )


# | [FEP-a4ed: The Fediverse Enhancement Proposal Process](./fep/a4ed/fep-a4ed.md)          | `FINAL` | [#10](https://git.activitypub.dev/ActivityPubDev/Fediverse-Enhancement-Proposals/issues/10) | 2020-10-16     | 2020-01-18


with open("README.md", "w") as f1:
    with open("scripts/frontmatter.md") as f:
        f1.write(f.read().removesuffix("\n"))

    f1.writelines(result)

    with open("scripts/backmatter.md") as f:
        f1.write(f.read())
