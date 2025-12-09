'''
Proof-of-Concept for the Self-Sovereign Identity (SSI) Resolution Protocol
as defined in the CORE_PROTOCOL.md for the Lightning Bolt Network.

This script simulates:
1.  A simple Phi Chain Nexus (a DID registry).
2.  A User (Holder) with a DID and a Verifiable Credential (VC).
3.  A Service (Verifier) that resolves the DID and verifies the VC.
'''

import json

# --- 1. Simulated Phi Chain Nexus (DID Registry) ---
# In a real system, this would be a smart contract on the Phi Chain.
PHI_CHAIN_NEXUS = {
    "did:phi:123456789abcdefghi": {
        "publicKey": "0xABC123",  # A simplified public key
        "serviceEndpoint": "https://example.com/vc-service"
    }
}

# --- 2. User (Holder) Data ---
HOLDER_DID = "did:phi:123456789abcdefghi"

# A simple Verifiable Credential (VC) issued by a trusted Issuer.
# In a real system, this would be cryptographically signed.
VERIFIABLE_CREDENTIAL = {
    "@context": "https://www.w3.org/2018/credentials/v1",
    "id": "http://example.edu/credentials/3732",
    "type": ["VerifiableCredential", "UniversityDegreeCredential"],
    "issuer": "did:phi:issuer-university-xyz",
    "issuanceDate": "2025-12-08T00:00:00Z",
    "credentialSubject": {
        "id": HOLDER_DID,
        "degree": {
            "type": "BachelorDegree",
            "name": "Bachelor of Science in Network Engineering"
        }
    },
    "proof": {
        "type": "Ed25519Signature2018",
        "created": "2025-12-08T00:00:00Z",
        "verificationMethod": "did:phi:issuer-university-xyz#keys-1",
        "proofPurpose": "assertionMethod",
        "jws": "eyJ...'''  # Simplified JWS signature
    }
}

# --- 3. Service (Verifier) Logic ---

def resolve_did(did: str) -> dict:
    """Resolves a DID via the simulated Phi Chain Nexus."""
    print(f"VERIFIER: Resolving DID: {did}")
    did_document = PHI_CHAIN_NEXUS.get(did)
    if did_document:
        print(f"VERIFIER: DID Document found. Public Key: {did_document['publicKey']}\n")
        return did_document
    else:
        print("VERIFIER: DID not found in Phi Chain Nexus.\n")
        return None

def verify_credential(vc: dict, holder_did_document: dict) -> bool:
    """Verifies a credential presented by the holder."""
    print("VERIFIER: Verifying presented credential...")
    
    # 1. Check if the credential subject matches the holder's DID
    if vc["credentialSubject"]["id"] != HOLDER_DID:
        print("VERIFIER: Credential subject does not match holder's DID. Verification failed.")
        return False
    
    # 2. In a real system, we would use the holder's public key to verify the signature.
    # Here, we just simulate a successful signature check.
    if "proof" in vc and vc["proof"]["jws"]:
        print("VERIFIER: Credential signature is valid (simulated).")
    else:
        print("VERIFIER: Credential signature is missing or invalid. Verification failed.")
        return False

    print("VERIFIER: Credential verified successfully!\n")
    return True


# --- Main Execution: Simulating the Protocol Flow ---
if __name__ == "__main__":
    print("--- Starting SSI Resolution Protocol PoC ---\n")

    # Step 1: Verifier resolves the Holder's DID
    holder_did_document = resolve_did(HOLDER_DID)

    if holder_did_document:
        # Step 2: Holder presents the Verifiable Credential
        print(f"HOLDER: Presenting my Verifiable Credential to the service:\n{json.dumps(VERIFIABLE_CREDENTIAL, indent=2)}\n")

        # Step 3: Verifier verifies the credential
        is_valid = verify_credential(VERIFIABLE_CREDENTIAL, holder_did_document)

        # Step 4: Verifier grants access based on verification
        if is_valid:
            degree_info = VERIFIABLE_CREDENTIAL['credentialSubject']['degree']['name']
            print(f"SERVICE: Access granted. Welcome, holder of a '{degree_info}'.")
        else:
            print("SERVICE: Access denied. Credential could not be verified.")

    print("\n--- SSI Resolution Protocol PoC Finished ---")
