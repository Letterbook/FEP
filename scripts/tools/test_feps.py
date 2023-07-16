import pytest
import hashlib

from scripts.tools import get_fep_ids, FepFile


@pytest.mark.parametrize("fep", get_fep_ids())
def test_fep(fep):
    fep_file = FepFile(fep)

    content = fep_file.content
    parsed_frontmatter = fep_file.parsed_frontmatter

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
