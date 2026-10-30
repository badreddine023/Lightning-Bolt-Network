"""Self-Sovereign Identity resolution protocol proof of concept.

The PoC models the Lightning Bolt Network flow:

1. Resolve a ``did:phi`` identifier through the Phi Chain Nexus registry.
2. Resolve a content-addressed Verifiable Credential reference.
3. Verify that the credential belongs to the resolved holder and has a proof.
4. Exercise both successful and rejected paths.

The registry and IPFS/CBA layer are deterministic in-memory simulations. No
network node or third-party Python package is required to run this example.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

JsonObject = dict[str, Any]

HOLDER_DID = "did:phi:123456789abcdefghi"
NON_EXISTENT_DID = "did:phi:nonexistent12345"
DID_REGISTRY_ADDRESS = "phi:nexus:did-registry-v1"

DID_DOCUMENTS: dict[str, JsonObject] = {
    HOLDER_DID: {
        "id": HOLDER_DID,
        "publicKey": "did:phi:123456789abcdefghi#keys-1",
        "serviceEndpoint": "https://example.com/vc-service",
    }
}

ORIGINAL_VERIFIABLE_CREDENTIAL: JsonObject = {
    "@context": "https://www.w3.org/2018/credentials/v1",
    "id": "https://example.edu/credentials/3732",
    "type": ["VerifiableCredential", "UniversityDegreeCredential"],
    "issuer": "did:phi:issuer-university-xyz",
    "issuanceDate": "2025-12-08T00:00:00Z",
    "credentialSubject": {
        "id": HOLDER_DID,
        "degree": {
            "type": "BachelorDegree",
            "name": "Bachelor of Science in Network Engineering",
        },
    },
    "proof": {
        "type": "Ed25519Signature2018",
        "created": "2025-12-08T00:00:00Z",
        "verificationMethod": "did:phi:issuer-university-xyz#keys-1",
        "proofPurpose": "assertionMethod",
        "jws": "simulated-jws-signature",
    },
}

# Simulated content-addressed storage. The CID is derived from canonical bytes.
CONTENT_STORE: dict[str, JsonObject] = {}


def canonical_json(value: JsonObject) -> str:
    """Serialize JSON deterministically for hashing and comparison."""

    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def store_content_on_ipfs(content: JsonObject) -> str:
    """Store content in simulated IPFS and return a deterministic CID."""

    payload = canonical_json(content).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    cid = f"bafybeisimulated{digest[:32]}"
    CONTENT_STORE[cid] = deepcopy(content)
    print(f"IPFS: Content stored. Generated CID: {cid}")
    return cid


def retrieve_content_from_ipfs(cid: str) -> JsonObject | None:
    """Retrieve content by CID, returning a copy to model an external fetch."""

    print(f"IPFS: Resolving content CID: {cid}")
    content = CONTENT_STORE.get(cid)
    if content is None:
        print("IPFS: Content not found.")
        return None
    print("IPFS: Content successfully retrieved.")
    return deepcopy(content)


def simulated_contract_call(did: str) -> JsonObject | None:
    """Simulate a Phi Chain Nexus DID-registry contract call."""

    print(f"WEB3: Querying {DID_REGISTRY_ADDRESS} for {did}...")
    document = DID_DOCUMENTS.get(did)
    return deepcopy(document) if document else None


def resolve_did(did: str) -> JsonObject | None:
    """Resolve a DID through the simulated Phi Chain Nexus."""

    print(f"VERIFIER: Resolving DID: {did}")
    did_document = simulated_contract_call(did)
    if did_document is None:
        print("VERIFIER: DID not found in Phi Chain Nexus.\n")
        return None
    print(f"VERIFIER: DID Document found. Public key: {did_document['publicKey']}\n")
    return did_document


def verify_credential(vc_reference: JsonObject, holder_did_document: JsonObject) -> bool:
    """Verify a content-addressed credential against the resolved holder DID."""

    print("VERIFIER: Verifying presented credential reference...")
    if vc_reference.get("type") != "VerifiableCredentialReference":
        print("VERIFIER: Invalid credential reference format.")
        return False

    cid = vc_reference.get("cid")
    if not isinstance(cid, str) or not cid:
        print("VERIFIER: Credential reference has no CID.")
        return False

    full_vc = retrieve_content_from_ipfs(cid)
    if full_vc is None:
        print("VERIFIER: Credential retrieval failed. Verification rejected.\n")
        return False

    subject = full_vc.get("credentialSubject", {})
    resolved_holder = holder_did_document.get("id")
    if subject.get("id") != resolved_holder:
        print("VERIFIER: Credential subject does not match holder DID. Verification rejected.\n")
        return False

    proof = full_vc.get("proof", {})
    if not proof.get("jws"):
        print("VERIFIER: Credential proof is missing or invalid. Verification rejected.\n")
        return False

    print("VERIFIER: Credential proof is valid (simulated).")
    print("VERIFIER: Credential verified successfully!\n")
    return True


def main() -> None:
    """Run the success and rejection cases and fail loudly if expectations break."""

    print("--- Starting SSI Resolution Protocol PoC ---\n")
    print("--- Setup: Store full VC on IPFS (CBA) ---")
    vc_cid = store_content_on_ipfs(ORIGINAL_VERIFIABLE_CREDENTIAL)
    vc_reference = {"type": "VerifiableCredentialReference", "cid": vc_cid}
    print(f"HOLDER: Presenting reference: {json.dumps(vc_reference, indent=2)}\n")
    print("-" * 60)

    print("--- Test Case 1: Valid DID resolution and credential verification ---")
    holder_document = resolve_did(HOLDER_DID)
    assert holder_document is not None, "valid holder DID must resolve"
    assert verify_credential(vc_reference, holder_document), "valid credential must verify"
    degree_name = ORIGINAL_VERIFIABLE_CREDENTIAL["credentialSubject"]["degree"]["name"]
    print(f"SERVICE: Access granted. Welcome, holder of a '{degree_name}'.")
    print("RESULT: PASS - valid SSI/CBA flow accepted.")
    print("-" * 60)

    print("--- Test Case 2: Non-existent DID resolution ---")
    missing_document = resolve_did(NON_EXISTENT_DID)
    assert missing_document is None, "unknown DID must not resolve"
    print(f"RESULT: PASS - unknown DID rejected: {NON_EXISTENT_DID}")
    print("-" * 60)

    print("--- Test Case 3: Invalid content reference ---")
    assert not verify_credential(
        {"type": "VerifiableCredentialReference", "cid": "bafybeimissing"},
        DID_DOCUMENTS[HOLDER_DID],
    ), "missing CID content must be rejected"
    print("RESULT: PASS - missing content rejected.")
    print("-" * 60)
    print("\n--- SSI Resolution Protocol PoC Finished: ALL TESTS PASSED ---")


if __name__ == "__main__":
    main()
