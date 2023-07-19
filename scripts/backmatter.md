
## Submitting a FEP

Do you have an idea, opinion or information that you want to share with the wider Fediverse community? You may do so with a Fediverse Enhancement Proposal (FEP).

To create and submit a FEP:

1. Fork this repository, and then clone it to your local machine. Check the Codeberg [Cheat sheet](https://docs.codeberg.org/collaborating/pull-requests-and-git-flow/#cheat-sheet) on how to prepare your Pull Request.
2. Think of a title for the FEP you want to submit.
3. Compute the identifier of the FEP by computing the hash of the title. This can be done with following Unix command:
```
$ echo -n "The title of my proposal" | sha256sum | cut -c-4
b3f0
```
4. Create a subdirectory of [`fep/`](./fep/) using the identifier you just computed.
5. Copy the FEP template ([fep-xxxx-template.md](./fep-xxxx-template.md)) to this subdirectory and change the filename appropriately.
6. Use the identifer as the "slug" when filling out the frontmatter. 
    
    - For example, if your computed identifier was `abcd`, then your file would be located at `fep/abcd/fep-abcd.md` and your frontmatter would include `slug: "abcd"`.

7. Write down your idea in the newly created file and commit it to a new branch in your repository (ex. fep-xxxx).
8. Create a Pull Request to complete Step 1 of [FEP-a4ed: The Fediverse Enhancement Proposal Process](./feps/fep-a4ed.md). Further process is described in FEP-a4ed.

## Editors

The list of FEP's is facilitated by Editors who are listed in the [EDITORS.md](EDITORS.md) file. Editors are neutral custodians of the FEP process, who merge PR's, create tracking issues, and start discussion threads for each FEP in the [SocialHub](https://socialhub.activitypub.rocks) developer community forum.

## Contributing

Do you have ideas to improve the FEP Process? Post your suggestions to the issue tracker, or on the SocialHub forum. The SocialHub developer community is a "DoOcracy" which means: “pick up any task you want, and then steer it to completion”. Your contributions are most welcome, so delve in and find out how you can help.

## License

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication 

To the extent possible under law, the authors of this document have waived all copyright and related or neighboring rights to this work.
