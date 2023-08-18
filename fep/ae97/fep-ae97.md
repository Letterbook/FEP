---
slug: "ae97"
authors: silverpill <silverpill@firemail.cc>
status: DRAFT
dateReceived: 2023-08-14
---
# FEP-ae97: Client-side activity signing

## Summary

Existing Fediverse servers manage signing keys on behalf of their users. This proposal describes a new kind of [ActivityPub](https://www.w3.org/TR/activitypub/) client that lets users sign activities with their own keys, and a server that can distribute client-signed activities to other servers.

## History

Section [4.1 Actor objects](https://www.w3.org/TR/activitypub/#actor-objects) of ActivityPub specification mentions two endpoints, `provideClientKey` and `signClientKey`. The exact interface is [not specified](https://github.com/w3c/activitypub/issues/382), but the purpose of these endpoints is likely similar to the ones described in this proposal.

## Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC-2119](https://tools.ietf.org/html/rfc2119.html).

## Discovering endpoints

To begin communicating with the server, client MUST discover registration endpoints by sending an HTTP GET request to `/.well-known/activitypub`.

The server MUST respond with a JSON document containing URLs of these endpoints:

- `registerIdentity`: the endpoint required for registering identity.
- `verifyIdentity`: the endpoint required for verifying identity.

Example:

```json
{
  "registerIdentity": "https://server.example/register_identity",
  "verifyIdentity": "https://server.example/verify_identity"
}
```

## Creating an actor

To create an actor, the client MUST send an HTTP POST request to `registerIdentity` endpoint. The body of the request MUST be a JSON document with the following properties:

- `subject`: the identity of the user, in the form of a [Decentralized Identifier](https://www.w3.org/TR/did-core/) (DID).
- `preferredUsername`: the preferred username.

Example:

```json
{
  "subject": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
  "preferredUsername": "alice"
}
```

If request is valid, server MUST generate actor ID and return it to the client.

Example:

```json
{
  "id": "https://server.example/users/alice"
}
```

The client MUST create a [FEP-c390](https://codeberg.org/fediverse/fep/src/branch/main/fep/c390/fep-c390.md) identity proof and send it in a POST request to `verifyIdentity` endpoint.

Example:

```json
{
  "type": "VerifiableIdentityStatement",
  "subject": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
  "alsoKnownAs": "https://server.example/users/alice",
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-jcs-2022",
    "created": "2023-02-24T23:36:38Z",
    "verificationMethod": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
    "proofPurpose": "assertionMethod",
    "proofValue": "z26W7TfJYD9DrGqnem245zNbeCbTwjb8avpduzi1JPhFrwML99CpP6gGXSKSXAcQdpGFBXF4kx7VwtXKhu7VDZJ54"
  }
}
```

If identity proof is valid, the server MUST create a new actor document, and attach provided identity proof to it.

## Sending activities

The client MUST sign all activities by adding [FEP-8b32](https://codeberg.org/fediverse/fep/src/branch/main/fep/8b32/fep-8b32.md) integrity proofs to them. The `verificationMethod` property of integrity proof MUST correspond to the `subject` of one of identity proofs attached to an actor.

Client submits signed activities to actor's outbox. Contrary to what [ActivityPub](https://www.w3.org/TR/activitypub/#client-to-server-interactions) specification prescribes, the server MUST not overwrite the ID of activity. Instead of assigning a new ID, the server MUST verify that provided ID has not been used before.

The server MUST deliver activities to their indended audiences without altering them. Recipients of signed activities (including the actor's server) MUST verify integrity proofs on them. If verification method of the integrity proof doesn't match any of FEP-c390 identity proofs attached to the actor, the activity MUST be rejected.

## Compatibility

To maintain interoperability with existing software, the server MAY generate a private key for each actor to sign Server-To-Server HTTP requests.

If recipient supports FEP-8b32, and both HTTP signature and integrity proof are present, the integrity proof MUST be given precedence over HTTP signature.

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [RFC-2119] S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels](https://tools.ietf.org/html/rfc2119.html), 1997
- [Decentralized Identifier] Manu Sporny, Dave Longley, Markus Sabadell, Drummond Reed, Orie Steele, Christopher Allen, [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/), 2022
- [FEP-c390] silverpill, [FEP-c390: Identity Proofs](https://codeberg.org/fediverse/fep/src/branch/main/fep/c390/fep-c390.md), 2022
- [FEP-8b32] silverpill, [FEP-8b32: Object Integrity Proofs](https://codeberg.org/fediverse/fep/src/branch/main/fep/8b32/fep-8b32.md), 2022

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
