---
authors: Helge Krueger <helge.krueger@gmail.com>
status: DRAFT
dateReceived:  2023-02-13
---
# FEP-2e40: The FEP Vocabulary Extension Process

## Summary

Current usage of ActivityPub relies on the ActivityStreams namespace [AS-NS]
combined with custom extensions [Mastodon NS]. As far as I can tell, no
best practices exist or a formal process to add new namespaces.

This FEP will

- Create a FEP Vocabulary based on identified best practices
- Define a process to add new entries to this FEP Vocabulary without a risk of Term collision
- Define a process to elevate Terms to be common
- Define a process to create specialized Vocabularies
- Using [FEP-61CE] as an example how this process can be used.

## Background and Terminology

The JSON-LD context is introduced in [3.1 The Context](https://www.w3.org/TR/json-ld/#the-context) of [JSON-LD]. The context of an object is specified by its `@context` property.

One can think of the context as defining certain strings to be equivalent. For example `Note`, `as:Note`, and `https://www.w3.org/ns/activitystreams#Note` all represent the same thing. More details can be found in [3.2. IRIs](https://www.w3.org/TR/json-ld/#iris). Following [JSON-LD], we will refer to all three strings mentioned above as a __Term__.

The second useful aspect of this is that one can define the used terms through the provided URL: [https://www.w3.org/ns/activitystreams#Note](https://www.w3.org/ns/activitystreams#Note). Clicking on it will let you easily find the definiton of the [Note Type](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note).

We will refer to the combination of Context and easily accessible documentations for the terms a __Vocabulary__.

## Requirements

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this specification are to be interpreted as described in [RFC-2119].

## The FEP Vocabulary

This FEP creates the file `/namespace/fep.json` with content

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "fep": "https://w3id.org/fep#"
    }
  ]
}
```

A description of this context is contained in `/namespace/fep.md`. The goal of inclusion of the ActivityStreams context is to increase the chances of most objects having the simple form

```json
{
  "@context": "https://w3id.org/fep",
  ...
}
```

which is as close as one can get to pure JSON with JSON-LD. These two files fill form the __FEP Vocabulary__. Through a pull-request to [W3-ID], these two files will be made available at `https://w3id.org/fep`.

## Process to add a new Term to the FEP Vocabulary

The authors of FEP-xxxx following [FEP-a3ed] MAY include a section or sections titled "Create FEP Term: $TERM". The $TERM MUST follow points 2-5 of [3. The Registration Process](https://www.w3.org/TR/did-spec-registries/#the-registration-process) in [DID-Reg].

__FIXME__: Include the rules here.

Furthermore, the author MAY perform the following action

1. Add a new term of the form `fep-xxxx/$TERM` to `/namespace/fep.json`.
2. Add a description for this term to `/namespace/fep.md`.

The changes to the two files MUST be described in the FEP, and they may only add new content or change content added by the FEP.
An example is provided in the next section. While these actions are optional at the DRAFT stage of a FEP, they MUST be performed before a FEP can reach its FINAL stage. We will refer to a term introduced by this process as a __FEP term__.

Instead of having many sections with similar names, the author of a FEP MAY combine them.

__FIXME__: Check the following actually is valid JSON-LD:

__FIXME__: Document requirements on new documentation vs reusing existing documentation.

Instead of defining a new Term, the author of a  FEP MAY decide to include terms from another namespace as a FEP Term. For example, we decide to introduce `conversation` as follows

```json
 "fep:fep-xxxx/conversation": {
    "@id": "http://ostatus.org#conversation",
    "@type": "@id"
 },
 "fep-xxxx/conversation": "fep:fep-xxxx/conversation"
```

This has the advantage that terms, which are currently used but not properly documented, can be given a proper definition. Furthermore, this will help keep the `@context` block small.

__FIXME__: Find volunteer to do this. An incomplete list of terms to include `as:Public`, `as:senstive`, `ostatus:conversation`.

## Example "Create FEP term: serverSentEvents"

In [FEP-61ce], I plan to introduce the term `serverSentEvents`. As this will most likely be the first FEP using the herein defined procces, this will lead to `/namespace/fep.json` being changed to

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "fep": "https://www.w3id.org/fep#",
      "fep-61ce/serverSentEvents": {
        "@id": "fep:fep-61ce/serverSentEvents",
        "@type": "@id"
      }
    }
  ]
}
```

with usage information

> The term `serverSentEvents` is to be as part of the `endpoints` of an [ActivityPub] Actor. It specifies an endpoint, where the Client can receive push notifications using the Server Side Events protocol of activities being added to collections on the server. By default the inbox collection of the Actor is used. By specifying the `X-ActivityPub-Collection` header a different collection can be specified to retrieve push notifications from.
>
> Example usage:
>
> ```json
> {
>  "@context": ["https://www.w3id.org/fep",
>      {"serverSentEvents": "fep-61ce/serverSentEvents"}
>   ],
>  "type": "Person",
>  "id": "https://example.com/client_actor",
>  "inbox": "https://example.com/client_actor/inbox",
>  "outbox": "https://example.com/client_actor/outbox",
>  "preferredUsername": "actor",
>  "endpoints": {
>    "proxyUrl": "https://example.com/client_actor/proxyUrl",
>    "serverSentEvents": "https://example.com/client_actor/serverSentEvents"
>  }
> }
> ```
>

## Promotion to common terms

While the above example is already nice looking, it still has the uglyness of needing to define `serverSentEvents` as `fep-61ce/serverSentEvents`. We will call the process of adding the line

```json
"serverSentEvents": "fep-61ce/serverSentEvents"
```

to `/namespace/fep.json` a __promotion to common term__.

In order to be elligible for promotion, a term MUST NOT conflict with any term currently in the vocabulary. For example, if the term `visualization` was already introduced in a previous FEP, it is not acceptable to introduce `visualisation` and expect promotion of this term.

Any term elligible for promotion CAN be promoted to a common term by the author of the FEP after the FEP has been declared FINAL. If an author does not seek to promotion of a term, it SHOULD be noted in the section introducing this term.

## Secondary FEP Vocabularies

We have now introduced a process for the common or primary vocabulary with context in `/namespace/fep.json` and documentation in `/namespace/fep.md`. We will now introduce _secondary vocabularies_. These are meant to be an option to introduce many domain specific terms without having to add them to the primary vocabulary.

An author of a FEP MAY include a section titled "Introducing Secondary FEP Vocubalary fep-DOMAIN". Here DOMAIN is a short name representing the domain. Then files `/namespace/fep-domain.json` and `/namespace/fep-domain.md` can be created. These should only differ from the primary files in the list of promoted terms.

__FIXME__: Find a technical solution to avoid duplication in the markdown.

## Example: The barber vocabulary

The barber community in the FediVerse has decided that, they need a marker if people shave themself. So they have introduce FEP-ba1b and defined the term `shavesHimself`. It was decided not to promote this term to the primary vocabulary. Instead the barber community has decided to introduce FEP-ba2b, in which they introduce the secondary FEP vocabulary `fep-barber`. The context of this vocabulary then takes the form:

```json
{
  "@context": [
    "https://www.w3id.org/fep",
    {
      "shavesHimself": "fep-ba1b/shavesHimself"
    }
  ]
}
```

By including the primary FEP vocabulary, it is ensured that changes to the primary vocabulary carry over to the secondary `fep-barber` vocabulary. Furthermore, by the promotion of `shavesHimself` taking place after the inclusion of the primary vocabulary, it is ensure that the primary vocabulary cannot override it.

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [AS-NS] Amy Guy [ActivityStreams 2.0 Terms](https://www.w3.org/ns/activitystreams), 2018
- [AS-Git] M. Sporny  [Add alsoKnownAs property to AS vocabulary #511](https://github.com/w3c/activitystreams/issues/511), 2020
- [DID Reg] Orie Steele, Manu Sporny [DID Specification Registries](https://www.w3.org/TR/did-spec-registries), 2023
- [FEP-a4ed] pukkamustard [FEP-a4ed: The Fediverse Enhancement Proposal Process](https://codeberg.org/fediverse/fep/src/branch/main/feps/fep-a4ed.md)
- [FEP-61ce] Helge Krueger [FEP-61CE: Server Sent Events for Actor], in preparation
- [JSON-LD] Gregg Kellogg,
    Pierre-Antoine Champin,
    Dave Longley
[JSON-LD](https://www.w3.org/TR/json-ld/), 2020
- [Mastodon NS] Eugen Rochko et al [JSON-LD Namespacing](https://docs.joinmastodon.org/spec/activitypub/#namespaces)
- [RFC-2119] S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels](https://tools.ietf.org/html/rfc2119.html)
- [W3-ID] Contibutors [Permanent Identifiers for the Web](https://github.com/perma-id/w3id.org)

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
