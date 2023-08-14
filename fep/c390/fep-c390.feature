Feature: FEP-c390: Identity Proofs

    @fep-c390
    Scenario: Creating the identity proof
        Given the decentralized identifier "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2"
        And private Key "z3u2en7t5LR2WtQH5PfFqMqwVHBeXouLzo6haApm8XHqvjxq"
        And actor ID "https://server.example/users/alice"
        And current time "2023-02-24T23:36:38Z"
        When creating the identity proof for the actor
        Then the identity claim is
            """
             {
                "type": "VerifiableIdentityStatement",
                "subject": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
                "alsoKnownAs": "https://server.example/users/alice"
            }
            """
        And the identity proof is
            """
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
            """

    @fep-c390
    Scenario: Verifying the identity proof
        Given the actor
            """
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
                            "cryptosuite": "eddsa-jcs-2022",
                            "created": "2023-02-24T23:36:38Z",
                            "verificationMethod": "did:key:z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2",
                            "proofPurpose": "assertionMethod",
                            "proofValue": "z26W7TfJYD9DrGqnem245zNbeCbTwjb8avpduzi1JPhFrwML99CpP6gGXSKSXAcQdpGFBXF4kx7VwtXKhu7VDZJ54"
                        }
                    }
                ]
            }
            """
        When verifying the attached identity proof
        Then the identity proof is valid
