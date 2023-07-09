Feature: FEP-8b32: Object Integrity Proofs

    @fep-8b32
    Scenario: Signing document
        Given document
            """
            {
                "@context": [
                    "https://www.w3.org/ns/activitystreams",
                    "https://w3id.org/security/data-integrity/v1"
                ],
                "type": "Create",
                "actor": "https://server.example/users/alice",
                "object": {
                    "type": "Note",
                    "content": "Hello world"
                }
            }
            """
        And Ed25519 Private Key "z3u2en7t5LR2WtQH5PfFqMqwVHBeXouLzo6haApm8XHqvjxq"
        And current time "2023-02-24T23:36:38Z"
        When Signing the document for key "https://server.example/users/alice#ed25519-key"
        Then The signed document is
            """
            {
                "@context": [
                    "https://www.w3.org/ns/activitystreams",
                    "https://w3id.org/security/data-integrity/v1"
                ],
                "type": "Create",
                "actor": "https://server.example/users/alice",
                "object": {
                    "type": "Note",
                    "content": "Hello world"
                },
                "proof": {
                    "type": "DataIntegrityProof",
                    "cryptosuite": "jcs-eddsa-2022",
                    "verificationMethod": "https://server.example/users/alice#ed25519-key",
                    "proofPurpose": "assertionMethod",
                    "proofValue": "z2nnHsFrkVJcmfprDuquc5bjjSZSUoFXbYZkyZFyptXVhwUwEBnhYftu9Jh25b9oZAn4WcPNY6mjhv2g3EuVc7fjC",
                    "created": "2023-02-24T23:36:38Z"
                }
            }
            """

    @fep-8b32
    Scenario: Verifying a signature
        Given The signed document is
            """
            {
                "@context": [
                    "https://www.w3.org/ns/activitystreams",
                    "https://w3id.org/security/data-integrity/v1"
                ],
                "type": "Create",
                "actor": "https://server.example/users/alice",
                "object": {
                    "type": "Note",
                    "content": "Hello world"
                },
                "proof": {
                    "type": "DataIntegrityProof",
                    "cryptosuite": "jcs-eddsa-2022",
                    "verificationMethod": "https://server.example/users/alice#ed25519-key",
                    "proofPurpose": "assertionMethod",
                    "proofValue": "z2nnHsFrkVJcmfprDuquc5bjjSZSUoFXbYZkyZFyptXVhwUwEBnhYftu9Jh25b9oZAn4WcPNY6mjhv2g3EuVc7fjC",
                    "created": "2023-02-24T23:36:38Z"
                }
            }
            """
        And The actor
            """
            {
                "@context": [
                    "https://www.w3.org/ns/activitystreams",
                    "https://w3id.org/security/data-integrity/v1",
                    "https://w3id.org/security/multikey/v1"
                ],
                "type": "Person",
                "id": "https://server.example/users/alice",
                "inbox": "https://server.example/users/alice/inbox",
                "outbox": "https://server.example/users/alice/outbox",
                "authentication": [
                    {
                        "id": "https://server.example/users/alice#ed25519-key",
                        "type": "Multikey",
                        "controller": "https://server.example/users/alice",
                        "publicKeyMultibase": "z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2"
                    }
                ]
            }
            """
        When verifying the document
        Then the document is valid
