---
authors: Adam R. Nelson <adam@nels.onl>
status: DRAFT
dateReceived: 2023-04-29
---
# FEP-fffd: Proxy Objects

## Summary

A *proxy object* is an \[ActivityPub] object that is semantically identical to an entity on another, non-ActivityPub protocol. For example, an ActivityPub-to-Nostr bridge creates Actors and Notes that are proxies for Nostr users and notes.

This document describes a data format to identify proxy objects and to describe the non-ActivityPub entities that they are equivalent to, with the intention that multi-protocol clients will automatically merge objects with their proxies, hiding the implementation details of bridges and cross-protocol publishing from users.

## Requirements

The key words "MUST", "SHOULD", and "MAY" are to be interpreted as described in \[RFC2119].

## Rationale

Many Fediverse servers speak multiple protocols besides ActivityPub, such as Zot or Diaspora, and simultaneously publish posts across multiple protocols. Additionally, bridge servers exist to relay posts between ActivityPub and other protocols such as Nostr.

There is currently no standard way to communicate that an ActivityPub activity is a copy (or *proxy*) of a post on another protocol.

Consider this scenario:

- Alice's server speaks both ActivityPub and Diaspora protocols. She publishes a post, which is syndicated on both protocols.
- Bob's server speaks only ActivityPub. He replies to the ActivityPub version of Alice's post.
- Charlie's server speaks only Diaspora. He replies to the Diaspora version of Alice's post.
- Dee's server speaks both ActivityPub and Diaspora. She receives Alice's, Bob's, and Charlie's posts. How does Dee's server know that Bob's reply and Charlie's reply belong to the same post?

Proxy objects provide a potential solution to this problem.

## Format

FEP-fffd uses the `w3id.org/fep` namespace as defined in \[FEP-9606]. Conforming ActivityPub JSON-LD messages MUST include a context that maps the terms `proxyOf`, `protocol`, `proxied`, and `authoritative` to the same IRIs and types as in this context:

```json
{
  "@context": {
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "fep": "https://w3id.org/fep/",
    "proxyOf": {
      "@id": "fep:fffd/proxyOf",
      "@type": "@id",
      "@container": "@set"
    },
    "protocol": {
      "@id": "fep:fffd/protocol",
      "@type": "@id"
    },
    "proxied": {
      "@id": "fep:fffd/proxied",
      "@type": "xsd:string"
    },
    "authoritative": {
      "@id": "fep:fffd/authoritative",
      "@type": "xsd:boolean"
    }
  }
}
```

The property `proxyOf` may be included in any ActivityPub Object, such as an Actor or a Note. If `proxyOf` is present, its value MUST be an array of objects, and each object in this array MUST include the properties `protocol` and `proxied`, and additionally MAY include the property `authoritative`. An object with a nonempty `proxyOf` property is called a *proxy object*.

Each entry in `proxyOf` names a non-ActivityPub entity, called a *proxied object*, which should be considered semantically identical to the parent proxy object. `protocol` is an IRI that identifies the non-ActivityPub protocol being used, and `proxied` is a freeform string (usually, but not necessarily, a URL) that identifies an entity in whatever format the protocol in question uses.

If `authoritative` is present and its value is `true`, it indicates that the proxied object is the original, authoritative version of the proxy object. The `proxyOf` array MUST NOT contain more than one object with `authoritative: true`. This property SHOULD be used by bridges that relay posts made by third parties, to indicate that the bridged post is not the original. It SHOULD NOT be used by servers that publish to multiple protocols at once; in this case no one version of an object is more authoritative than another.

## Protocols

This document defines two protocol names, but more may be included in either future FEPs or future revisions of this document.

### Nostr

`protocol`: `"https://nostr.com"`

`proxied` format: A \[NIP-19] string identifying a pubkey or note.

### Diaspora

`protocol`:  `"https://joindiaspora.com/protocol"`

`proxied` format: A URI with the \[`diaspora://` URI scheme].

### Freeform Prefix IRIs

In addition to the above specified protocol IRIs, `protocol` MAY be any other IRI if `proxied` is also an IRI and `protocol` is a prefix of `proxied`.

This allows an ActivityPub object to proxy any non-federated Web content; for example, a Twitter-to-ActivityPub bridge may use a `protocol` of `"https://twitter.com"` and a `proxied` value that is a Twitter URL, to identify a Note as a proxy object for a Twitter post.

## Examples

(This section is non-normative. The JSON-LD `@context` property is omitted for brevity.)

A post relayed by a third-party Twitter-to-ActivityPub bridge:

```json
{
  "id": "http://twitter-bridge.example/status/1234",
  "type": "Note",
  "actor": "http://twitter-bridge.example/@jack",
  "content": "just setting up my twttr",
  "proxyOf": [{
    "protocol": "https://twitter.com",
    "proxied": "https://twitter.com/jack/status/20",
    "authoritative": true
  }]
}
```

A post published to ActivityPub, Diaspora, and Nostr simultaneously:

```json
{
  "id": "http://fediverse.example/status/1234",
  "type": "Note",
  "actor": "http://fediverse.example/@alice",
  "content": "Hello, world!",
  "proxyOf": [{
    "protocol": "https://joindiaspora.com/protocol",
    "proxied": "diaspora://alice@fediverse.example/post/deadbeefdeadbeefdeadbeefdeadbeef"
  }, {
    "protocol": "https://nostr.com",
    "proxied": "note1gwdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
  }]
}
```

## References

* [RFC-2119] S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels](https://tools.ietf.org/html/rfc2119.html)
* [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
* [FEP-9606] a, [FEP-9606 : Using `w3id.org/fep` as a namespace for extension terms and for FEP documents](https://codeberg.org/fediverse/fep/src/branch/main/feps/fep-9606.md), 2023
* [NIP-19] jb55, fianjaf, Semisol, [NIP-19: bech32-encoded entities](https://github.com/nostr-protocol/nips/blob/master/19.md), 2023
* [`diaspora://` URI scheme] Benjamin Neff, [diaspora* federation protocol](https://diaspora.github.io/diaspora_federation/index.html), 2017

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
