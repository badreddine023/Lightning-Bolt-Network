'''
Proof-of-Concept for the Self-Sovereign Identity (SSI) Resolution Protocol
as defined in the CORE_PROTOCOL.md for the Lightning Bolt Network.

This script simulates:
1.  A simple Phi Chain Nexus (a DID registry) using a web3-like interface.
2.  A User (Holder) with a DID and a Verifiable Credential (VC).
3.  A Service (Verifier) that resolves the DID and verifies the VC.
'''

import json
from web3 import Web3 # Using web3 for a more realistic simulation

# --- 1. Simulated Phi Chain Nexus (DID Registry) ---
# In a real system, this would be a smart contract on the Phi Chain.
# We simulate a web3 connection and a contract call.
w3 = Web3(Web3.HTTPProvider('http://simulated-phi-chain-node:8545'))

# Simulated Contract ABI and Address
DID_REGISTRY_ADDRESS = '0x1234567890123456789012345678901234567890'
DID_REGISTRY_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "did", "type": "string"}],
        "name": "resolveDID",
        "outputs": [{"name": "didDocument", "type": "string"}],
        "type": "function"
    }
]

# Simulated DID Document Storage
SIMULATED_DID_DOCUMENTS = {
    "did:phi:123456789abcdefghi": json.dumps({
        "publicKey": "0xABC123",  # A simplified public key
        "serviceEndpoint": "https://example.com/vc-service"
    }),
    "did:phi:unknown": None
}

# --- Simulated Contract Interaction ---
def simulated_contract_call(did: str) -> str:
    """Simulates a call to the resolveDID smart contract function."""
    print(f"WEB3: Calling DID Registry contract at {DID_REGISTRY_ADDRESS} to resolve {did}...")
    return SIMULATED_DID_DOCUMENTS.get(did)

# --- 2. User (Holder) Data ---
HOLDER_DID = "did:phi:123456789abcdefghi"

# A simple Verifiable Credential (VC) issued by a trusted Issuer.
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
        "jws": "eyJ..."  # Simplified JWS signature
    }
}

# --- 3. Service (Verifier) Logic ---

def resolve_did(did: str) -> dict:
    """Resolves a DID by simulating a web3 contract call."""
    print(f"VERIFIER: Resolving DID: {did}")
    
    # Simulate web3 connection check
    if not w3.is_connected():
        print("VERIFIER: Simulating connection to Phi Chain node...")
    
    # Simulate contract call
    did_document_json = simulated_contract_call(did)
    
    if did_document_json:
        did_document = json.loads(did_document_json)
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
    print("--- Starting SSI Resolution Protocol PoC (Web3 Refactor) ---\n")

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
