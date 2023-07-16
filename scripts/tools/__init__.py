import glob


def get_fep_ids():
    for fep in glob.glob("fep/*"):
        yield fep.removeprefix("fep/")


class FepFile:
    def __init__(self, fep):
        self.fep = fep
        with open(self.filename) as f:
            self.frontmatter, self.content = FepFile.parsefile(f)

    @property
    def filename(self):
        return f"fep/{self.fep}/fep-{self.fep}.md"

    @property
    def summary(self):
        result = []
        is_summary = False
        for x in self.content:
            if is_summary:
                if x.startswith("##"):
                    return "\n".join(result)
                result.append(x)
            elif x == "## Summary":
                is_summary = True

    def write(self):
        with open(self.filename, "w") as f:
            f.write("---\n")
            for x in self.frontmatter:
                f.write(x + "\n")
            f.write("---\n")
            for x in self.content:
                f.write(x + "\n")

    @property
    def parsed_frontmatter(self):
        split = [x.split(":", 1) for x in self.frontmatter]
        return {a: b.strip() for a, b in split}

    @property
    def title(self):
        titles = [x for x in self.content if x.startswith("# ")]
        assert len(titles) > 0

        title = titles[0]

        begin_title = f"# FEP-{self.fep}: "

        assert title.startswith(begin_title)
        true_title = title.removeprefix(begin_title)

        return true_title

    @staticmethod
    def parsefile(f):
        lines = f.readlines()

        status = 0
        frontmatter = []
        content = []

        for line in lines:
            if line == "---\n" and status <= 2:
                status += 1
            elif status == 1:
                frontmatter.append(line.removesuffix("\n"))
            elif status >= 2:
                content.append(line.removesuffix("\n"))

        return frontmatter, content
