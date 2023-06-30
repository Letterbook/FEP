import pytest
import glob
import hashlib


def get_fep_ids():
    for fep in glob.glob("fep/*"):
        yield fep.removeprefix("fep/")


def parsefile(f):
    lines = f.readlines()

    status = 0
    frontmatter = []
    content = []

    for line in lines:
        if line == "---\n":
            status += 1
        elif status == 1:
            frontmatter.append(line.removesuffix("\n"))
        elif status >= 2:
            content.append(line.removesuffix("\n"))

    return frontmatter, content


def parse_frontmatter(frontmatter):
    split = [x.split(":", 1) for x in frontmatter]
    return {a: b.removeprefix(" ") for a, b in split}


@pytest.mark.parametrize("fep", get_fep_ids())
def test_fep(fep):
    filename = f"fep/{fep}/fep-{fep}.md"

    with open(filename) as f:
        frontmatter, content = parsefile(f)

    assert len(frontmatter) > 0
    assert len(content) > 0
    parsed_frontmatter = parse_frontmatter(frontmatter)

    assert "status" in parsed_frontmatter
    assert parsed_frontmatter["status"] in ["DRAFT", "FINAL"]
    assert parsed_frontmatter["slug"] == f'"{fep}"'
    assert "authors" in parsed_frontmatter

    assert "## Summary" in content
    assert "## Copyright" in content

    titles = [x for x in content if x.startswith("# ")]
    assert len(titles) > 0

    title = titles[0]

    begin_title = f"# FEP-{fep}: "

    assert title.startswith(begin_title)
    true_title = title.removeprefix(begin_title)

    expected_slug = hashlib.sha256(true_title.encode("utf-8")).hexdigest()[:4]

    assert expected_slug == fep
