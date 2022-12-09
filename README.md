# Fediverse Enhancement Proposals

This is the Git repository containing Fediverse Enhancment Proposals (FEPs).

A Fediverse Enhancement Proposal (FEP) is a document that provides information to the Fediverse community. The goal of a FEP is to improve interoperability and well-being of diverse services, applications and communities that form the Fediverse.

# FEPs

<!-- TODO: This table is not CommonMark (as specified by FEP-a4ed) and requires maintenance. It should be replaced by a dynamically created table. -->

| Title                                                                               | Status  | Tracking issue                                                                              | `dateReceived` | `dateFinalized` (or `dateWithdrawn`) |
| ---                                                                                 | ---     | -----                                                                                       | -------        | ------                               |
| [FEP-a4ed: The Fediverse Enhancement Proposal Process](./feps/fep-a4ed.md)          | `FINAL` | [#10](https://git.activitypub.dev/ActivityPubDev/Fediverse-Enhancement-Proposals/issues/10) | 2020-10-16     | 2020-01-18                           |
| [FEP-8fcf: Followers collection synchronization across servers](./feps/fep-8fcf.md) | `FINAL` | [#6](https://codeberg.org/fediverse/fep/issues/6) [#11](https://git.activitypub.dev/ActivityPubDev/Fediverse-Enhancement-Proposals/issues/11) | 2020-10-24     | 2022-02-07                                    |
| [FEP-f1d5: NodeInfo in Fediverse Software](./feps/fep-f1d5.md)                      | `DRAFT` | [#12](https://git.activitypub.dev/ActivityPubDev/Fediverse-Enhancement-Proposals/issues/12) | 2020-12-13     | -                                    |
| [FEP-400e: Publicly-appendable ActivityPub collections](./feps/fep-400e.md)         | `FINAL` | [#5](https://codeberg.org/fediverse/fep/issues/5)                                       | 2021-02-16     | 2020-02-04                           |
| [FEP-8c3f: Web Monetization](./feps/fep-8c3f.md) | `DRAFT` | [#3](https://codeberg.org/fediverse/fep/issues/3) | 2022-01-18     | -                                    |
| [FEP-2100: Unbound Group and Organization](./feps/fep-2100.md) | `DRAFT` | [#36](https://codeberg.org/fediverse/fep/issues/36) | 2022-03-31 | - |
| [FEP-e232: Object Links](./feps/fep-e232.md) | `DRAFT` | [#14](https://codeberg.org/fediverse/fep/issues/14) | 2022-08-01 | - |
| [FEP-5624: Per-object reply control policies](./feps/fep-5624.md) | `DRAFT` | [#18](https://codeberg.org/fediverse/fep/issues/18) | 2022-08-23 | - |
| [FEP-1b12: Group federation](./feps/fep-1b12.md) | `DRAFT` | [#22](https://codeberg.org/fediverse/fep/issues/22) | 2022-11-12 | - |
| [FEP-8b32: Object Integrity Proofs](./feps/fep-8b32.md) | `DRAFT` | [#29](https://codeberg.org/fediverse/fep/issues/29) | 2022-11-12 | - |
| [FEP-c390: Identity Proofs](./feps/fep-c390.md) | `DRAFT` | [#34](https://codeberg.org/fediverse/fep/issues/34) | 2022-11-23 | - |
| [FEP-cb76: Content Addressed Vocabulary](./feps/fep-cb76.md) | `DRAFT` | [#41](https://codeberg.org/fediverse/fep/issues/41) | 2022-11-29 | - |
| [FEP-fb2a: Actor metadata](./feps/fep-fb2a.md) | `DRAFT` | [#45](https://codeberg.org/fediverse/fep/issues/45) | 2022-12-09 | - |


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
5. Submit a Pull Request to this repository containing your proposal (other submission methods may be listed in [`SUBMISSION.md`](./SUBMISSION.md)).
6. Within 7 days you will receive feedback from the editors who may request changes or clarifications. If your proposal is accepted it will be added to the repository with the status `DRAFT`. The editors will also create a tracking issue for your proposal.
7. You (as author) are now responsible for initiating community discussion and collecting feedback (post links to the discussions to the tracking issue). While the proposal is in status `DRAFT` you may submit changes to the proposal via Pull Requests (reference the tracking issue from the Pull Request).
8. After at least 60 days of being added to the repository with status `DRAFT` you may request the proposal to be finalized. You must now request final comments from the community. If there are no significant community objections your proposal will reach status `FINAL` after 14 days. Once the proposal has reached status `FINAL` it may no longer be updated.

For more information see [FEP-a4ed: The Fediverse Enhancement Proposal Process](./feps/fep-a4ed.md).

# Editors

Editors are listed in the [EDITORS.md](EDITORS.md) file.

# Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication 

To the extent possible under law, the authors of this document have waived all copyright and related or neighboring rights to this work.
