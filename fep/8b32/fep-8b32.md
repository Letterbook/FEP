---
slug: "8b32"
authors: silverpill <silverpill@firemail.cc>
status: DRAFT
dateReceived: 2022-11-12
discussionsTo: https://codeberg.org/fediverse/fep/issues/29
---
# FEP-8b32: Object Integrity Proofs

## Summary

This proposal describes how [ActivityPub](https://www.w3.org/TR/activitypub/) servers and clients could create self-authenticating activities and objects.

HTTP signatures are often used for authentication during server-to-server interactions. However, this ties authentication to activity delivery, and limits the flexibility of the protocol.

Integrity proofs are sets of attributes that represent digital signatures and parameters required to verify them. These proofs can be added to any activity or object, allowing recipients to verify the identity of the actor and integrity of the data. That decouples authentication from the transport, and enables various protocol improvements such as activity relaying, embedded objects and client-side signing.

## History

Mastodon supports Linked Data signatures [since 2017](https://github.com/mastodon/mastodon/pull/4687), and a number of other platforms added support for them later. These signatures are similar to integrity proofs, but are based on outdated [Linked Data Signatures 1.0](https://github.com/w3c-ccg/ld-signatures/) specification, which has been superseded by other standards.

## Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC-2119](https://tools.ietf.org/html/rfc2119.html).

## Integrity proofs

The proposed authentication mechanism is based on [Data Integrity](https://w3c.github.io/vc-data-integrity/) specification.

### Proof generation

The proof MUST be created according to the *Data Integrity* specification, section [4.1 Generate Proof](https://w3c.github.io/vc-data-integrity/#generate-proof).

The process of proof generation consists of the following steps:

- **Canonicalization** is a transformation of a JSON object into the form suitable for hashing, according to some deterministic algorithm.
- **Hashing** is a process that calculates an identifier for the transformed data using a cryptographic hash function.
- **Signature generation** is a process that calculates a value that protects the integrity of the input data from modification.

The resulting proof is added to the original JSON object under the key `proof`. Objects MAY contain multiple proofs.

Example of unsigned activity:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/data-integrity/v1"
    ],
    "type": "Create",
    "actor": "https://example.com/users/alice",
    "object": {
        "type": "Note",
        "content": "Hello world"
    }
}
```

Example of activity with integrity proof:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/data-integrity/v1"
    ],
    "type": "Create",
    "actor": "https://example.com/users/alice",
    "object": {
        "type": "Note",
        "content": "Hello world"
    },
    "proof": {
        "type": "DataIntegrityProof",
        "cryptosuite": "jcs-rsa-2022",
        "created": "2022-11-12T00:00:00Z",
        "verificationMethod": "https://example.com/users/alice#main-key",
        "proofPurpose": "assertionMethod",
        "proofValue": "<proof-value>"
    }
}
```

The list of attributes used in integrity proof is defined in *Data Integrity* specification, section [2.1 Proofs](https://w3c.github.io/vc-data-integrity/#proofs). The proof type SHOULD be `DataIntegrityProof`, as specified in section [3.1 DataIntegrityProof](https://w3c.github.io/vc-data-integrity/#dataintegrityproof). The value of `verificationMethod` attribute SHOULD be an URL of actor's public key or a [DID](https://www.w3.org/TR/did-core/) associated with an actor.

### Proof verification

The recipient of activity SHOULD perform proof verification if it contains integrity proofs. Verification process MUST follow the *Data Integrity* specification, section [4.2 Verify Proof](https://w3c.github.io/vc-data-integrity/#verify-proof). It starts with the removal of a `proof` value from the JSON object. Then the object is canonicalized, hashed and signature verification is performed according to the parameters specified in the proof.

If both HTTP signature and integrity proof are used, the integrity proof MUST be given precedence over HTTP signature. The HTTP signature MAY be dismissed.

### Algorithms

Implementers SHOULD pursue broad interoperability when choosing algorithms for integrity proofs.

[jcs-eddsa-2022](https://w3c.github.io/vc-di-eddsa/#jcs-eddsa-2022) cryptosuite is RECOMMENDED:

- Canonicalization: [JCS](https://www.rfc-editor.org/rfc/rfc8785)
- Hashing: SHA-256
- Signatures: EdDSA

Support for **RSASSA-PKCS1-v1_5** signature algorithm is OPTIONAL but could be desirable for interoperability with legacy systems.

### Backwards compatibility

Integrity proofs and Linked Data signatures can be used together, as they rely on different properties (`proof` and `signature`, respectively).

## Implementations

- [Mitra](https://codeberg.org/silverpill/mitra/src/tag/v1.13.0/FEDERATION.md#object-integrity-proofs)
- Vervis
  ([generation](https://codeberg.org/ForgeFed/Vervis/commit/e8e587af26944d3ea8d91f5c47cc3058cf261387),
  [verification](https://codeberg.org/ForgeFed/Vervis/commit/621275e25762a1c1e5860d07a6ff87b147deed4f))

## References

- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [RFC-2119] S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels](https://tools.ietf.org/html/rfc2119.html), 1997
- [Data Integrity] Dave Longley, Manu Sporny, [Verifiable Credential Data Integrity 1.0](https://w3c.github.io/vc-data-integrity/), 2022
- [DID] Manu Sporny, Dave Longley, Markus Sabadell, Drummond Reed, Orie Steele, Christopher Allen, [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/), 2022
- [jcs-eddsa-2022] Dave Longley, Manu Sporny, [EdDSA Cryptosuite v2022](https://w3c.github.io/vc-di-eddsa/), 2023
- [JCS] A. Rundgren, B. Jordan, S. Erdtman, [JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785), 2020

## Copyright

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

To the extent possible under law, the authors of this Fediverse Enhancement Proposal have waived all copyright and related or neighboring rights to this work.
