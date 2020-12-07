# Fediverse Enhancement Proposals

This is the Git repository containing Fediverse Enhancment Proposals (FEPs).

A Fediverse Enhancement Proposal (FEP) is a document that provides information to the Fediverse community. The goal of a FEP is to improve interoperability and well-being of diverse services, applications and communities that form the Fediverse.

# Submitting a FEP

Do you have an idea, opinion or information that you want to share with the wider Fediverse community? You may do so with a Fediverse Enhancement Proposal (FEP).

To create and submit a FEP:

1. Think of a title for the FEP you want to submit.
2. Compute the identifier of the FEP by computing the hash of the title. This can be done with following Unix command:
```
$ echo -n "The title of my proposal" | sha256sum | cut -c-4
b3f0
```
4. Clone this repository.
3. Copy the FEP template ([fep-0000-template.md](./fep-0000-template.md)) to the [feps/](feps/) folder and change the filename to `fep-abcd.md` where `abcd` is the identifier computed in step 2.
4. Write down your idea in the newly created file.
5. Submit a Pull Request to this repository containing your proposal (other submission methods may be listed in [`SUBMISSION_METHODS`](./SUBMISSION_METHODS)).
6. Within 7 days you will receive feedback from the editors who may request changes or clarifications. If your proposal is accepted it will be added to the repository with the status `DRAFT`.
7. You (as author) are now responsible for initiating community discussion and collecting feedback. While the proposal is in status `DRAFT` you may submit changes to the proposal via Pull Requests.
8. After at least 60 days of being added to the repository with status `DRAFT` you may request the proposal to be finalized. You must now request final comments from the community. If there are no significant community objections your proposal will reach status `FINAL` after 14 days. Once the proposal has reached status `FINAL` it may no longer be updated.

For more information see [FEP-a4ed: The Fediverse Enhancement Proposal Process](./feps/fep-a4ed.md).

# Editors

Editors are listed in the [EDITORS](EDITORS) file.

# Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication 

To the extent possible under law, the authors of this document have waived all copyright and related or neighboring rights to this work.
