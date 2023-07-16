# tools for fep editors

Please follow the steps in configuration before following "Merge a FEP".

## Merge a FEP

Merge the Pull Request in [https://codeberg.org/fediverse/fep/pulls](https://codeberg.org/fediverse/fep/pulls)
and note the slug.

```bash
python scripts/create_issue.py $SLUG
```

creates the tracking issue and updates the fep with the information.
This script prints the issue url, you will need it later to add the
link to the SocialHub discussion. Then run

```bash
python scripts/create_readme.py
```

to update the table in `README.md`. You are now ready to commit the
changes to the FEP (added discussionsTo to frontmatter) and README.md,
added the new FEP.

Run

```bash
python scripts/create_topic.py $SLUG
```

and following the instructions to create a topic on SocialHub to discuss
the FEP.

Finally, add the link to the SocialHub issue to the tracking issue, created above.

## Configuration

Add a file `config.json` to the directory `scripts` with content

```json
{
  "repo": "fep",
  "owner": "fediverse",
  "token": "CODEBERG_API_TOKEN"
}
```

The API token can be obtained by visiting [https://codeberg.org/user/settings/applications](https://codeberg.org/user/settings/applications) and generating one with scope "public_repo".

## Setup for running pytest

Ensure dependencies (use a virtualenv)

```bash
pip install pytest
```

Check validity

```bash
pytest
```
