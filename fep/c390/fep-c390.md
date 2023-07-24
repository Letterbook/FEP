---
slug: "c390"
authors: silverpill <silverpill@firemail.cc>
status: DRAFT
dateReceived: 2022-11-23
relatedFeps: FEP-8b32
discussionsTo: https://codeberg.org/fediverse/fep/issues/34
---
# FEP-c390: Identity Proofs

## Summary

This proposal describes a mechanism of creating verifiable links between [Decentralized Identifiers](https://www.w3.org/TR/did-core/) and [ActivityPub](https://www.w3.org/TR/activitypub/) actor profiles.

Potential applications include: identity verification, end-to-end encryption and account migrations.

## History

- Mastodon implemented [identity proofs](https://github.com/mastodon/mastodon/pull/10414) in 2019. Keybase platform was used as an identity provider, but the integration was later [removed](https://github.com/mastodon/mastodon/pull/17045).
- [Keyoxide](https://keyoxide.org/) can create off-protocol identity proofs for Fediverse profiles [using OpenPGP](https://docs.keyoxide.org/service-providers/activitypub/).

## Identity proofs

Identity proof is a JSON document that represents a verifiable bi-directional link between a [Decentralized Identifier](https://www.w3.org/TR/did-core/) and an ActivityPub actor.

It MUST contain the following properties:

- `type` (REQUIRED): the `type` property MUST contain the string `VerifiableIdentityStatement`.
- `subject` (REQUIRED): the decentralized identifier (DID) that represents a cryptographic key belonging to an actor.
- `alsoKnownAs` (REQUIRED): the value of this property MUST match the actor ID.
- `proof` (REQUIRED): the data integrity proof, as defined by [Data Integrity](https://w3c.github.io/vc-data-integrity/) specification.

The document MAY contain additional properties.

Identity proofs SHOULD be attached to an actor object, under the `attachment` property.

### Proof generation

The identity proof document MUST contain a data integrity proof, which includes a cryptographic proof and parameters required to verify it. It MUST be created according to the *Data Integrity* specification, section [4.1 Add Proof](https://w3c.github.io/vc-data-integrity/#add-proof). The value of `verificationMethod` property of the data integrity proof MUST match the value of `subject` property of the identity proof document.

The resulting data integrity proof MUST be added to identity proof document under the `proof` key.

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://www.w3.org/ns/did/v1",
        "https://w3id.org/security/data-integrity/v1",
        {
            "fep": "https://w3id.org/fep#",
            "VerifiableIdentityStatement": "fep:VerifiableIdentityStatement",
            "subject": "fep:subject"
        }
    ],
    "type": "Person",
    "id": "https://server.example/users/alice",
    "inbox": "https://server.example/users/alice/inbox",
    "outbox": "https://server.example/users/alice/outbox",
    "attachment": [
        {
            "type": "VerifiableIdentityStatement",
            "subject": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
            "alsoKnownAs": "https://server.example/users/alice",
            "proof": {
                "type": "DataIntegrityProof",
                "cryptosuite": "jcs-eddsa-2022",
                "created": "2023-02-24T23:36:38Z",
                "verificationMethod": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
                "proofPurpose": "assertionMethod",
                "proofValue": "zYqr4eFzrnUWiBDaa7SmBhfaSBiv6BFRsDRGkmaCJpXArPBspFWNM6NXu77R7JakdzbUdjZihBa28LuWscZxSfRk"
            }
        }
    ]
}
```

### Proof verification

The consuming implementations MUST check the authenticity of identity proof document by verifying its data integrity proof. If the proof can not be verified, or if the value of `verificationMethod` property of the data integrity proof doesn't match the value of `subject` property of the identity proof, or if the value of `alsoKnownAs` property of the identity proof doesn't match the actor ID, the identity proof MUST be discarded.

Verification process MUST follow the *Data Integrity* specification, section [4.2 Verify Proof](https://w3c.github.io/vc-data-integrity/#verify-proof).

### Linking identities

The consuming implementations SHOULD treat identities denoted by `subject` and `alsoKnownAs` properties of identity proof as belonging to the same entity.

If two actors have identity proofs with the same `subject` property, they SHOULD be treated as different identities of the same entity.

## Test vectors

See [fep-c390.feature](./fep-c390.feature)

## Implementations

- [Mitra](https://codeberg.org/silverpill/mitra/src/commit/eb18e475efb71e461cd33c800c86cfe94144f5a3/FEDERATION.md#identity-proofs)

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [Decentralized Identifiers] Manu Sporny, Dave Longley, Markus Sabadell, Drummond Reed, Orie Steele, Christopher Allen, [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/), 2022
- [Data Integrity] Dave Longley, Manu Sporny, [Verifiable Credential Data Integrity 1.0](https://w3c.github.io/vc-data-integrity/), 2022

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
