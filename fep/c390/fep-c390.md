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

This proposal describes a mechanism of linking cryptographic keys to [ActivityPub](https://www.w3.org/TR/activitypub/) actor profiles.

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

The identity proof document MUST contain a data integrity proof, which includes a cryptographic proof and parameters required to verify it. It MUST be created according to the *Data Integrity* specification, section [4.1 Generate Proof](https://w3c.github.io/vc-data-integrity/#generate-proof). The value of `verificationMethod` property of the data integrity proof MUST match the value of `id` property of the identity proof document.

The resulting data integrity proof MUST be added to identity proof document under the `proof` key.

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://www.w3.org/ns/did/v1",
        "https://w3id.org/security/data-integrity/v1",
        {
            "fep": "https://w3id.org/fep#"
            "VerifiableIdentityStatement": "fep:VerifiableIdentityStatement",
            "subject": "fep:subject"
        }
    ],
    "type": "Person",
    "id": "https://example.com/users/alice",
    "inbox": "https://example.com/users/alice/inbox",
    "attachment": [
        {
            "type": "VerifiableIdentityStatement",
            "subject": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
            "alsoKnownAs": "https://example.com/users/alice",
            "proof": {
                "type": "JcsEd25519Signature2022",
                "created": "2022-11-12T00:00:00Z",
                "verificationMethod": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
                "proofPurpose": "assertionMethod",
                "proofValue": "<proof-value>"
            }
        }
    ]
}
```

### Proof verification

The receiving server MUST check the authenticity of identity proof document by verifying its data integrity proof. If the server can't verify the proof, or if the value of `verificationMethod` property of the data integrity proof doesn't match the value of `subject` property of the identity proof, or if the value of `alsoKnownAs` property of the identity proof doesn't match the actor ID, the identity proof MUST be discarded.

Verification process MUST follow the *Data Integrity* specification, section [4.2 Verify Proof](https://w3c.github.io/vc-data-integrity/#verify-proof).

The receiving server SHOULD treat identities denoted by `subject` and `alsoKnownAs` properties of identity proof as belonging to the same entity.

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [Decentralized Identifier] Manu Sporny, Dave Longley, Markus Sabadell, Drummond Reed, Orie Steele, Christopher Allen, [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/), 2022
- [Data Integrity] Dave Longley, Manu Sporny, [Verifiable Credential Data Integrity 1.0](https://w3c.github.io/vc-data-integrity/), 2022

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
