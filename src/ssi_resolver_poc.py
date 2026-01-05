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
import ipfshttpclient
from typing import Dict, Any

# --- 1. Simulated Phi Chain Nexus (DID Registry) ---

# --- IPFS Client Logic (Integrated from CBA PoC) ---

def store_content_on_ipfs(content: Dict[str, Any]) -> str:
    """Simulates storing content on IPFS and returns the CID."""
    print("IPFS: Attempting to connect to local IPFS node...")
    try:
        # Simulate the IPFS add operation
        content_str = json.dumps(content, indent=2)
        
        # Simulate hashing and CID generation
        cid = f"QmSimulatedCID{hash(content_str)}"
        
        print(f"IPFS: Content successfully added. Generated CID: {cid}")
        return cid
        
    except Exception as e:
        print(f"IPFS: Error connecting or adding content (simulated): {e}")
        return ""

def retrieve_content_from_ipfs(cid: str) -> Dict[str, Any] | None:
    """Simulates retrieving content from IPFS using the CID."""
    print(f"\nIPFS: Attempting to retrieve content with CID: {cid}")
    try:
        # Simulate the IPFS get operation
        if "QmSimulatedCID" in cid:
            # In a real system, this would retrieve the content from IPFS
            # For this PoC, we will simulate the retrieval of the original VC
            print("IPFS: Content successfully retrieved.")
            return ORIGINAL_VERIFIABLE_CREDENTIAL
        else:
            print("IPFS: Invalid CID. Content not found.")
            return None
            
    except Exception as e:
        print(f"IPFS: Error connecting or retrieving content (simulated): {e}")
        return None

# --- End IPFS Client Logic ---

# In a real system, this would be a smart contract on the Phi Chain.
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
# This is the full VC content, which will be stored on IPFS.
ORIGINAL_VERIFIABLE_CREDENTIAL = {
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

# The presented VC will only contain a reference (CID) to the full VC on IPFS.
VERIFIABLE_CREDENTIAL_REFERENCE = {
    "type": "VerifiableCredentialReference",
    "cid": "" # This will be populated at runtime
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

def verify_credential(vc_reference: dict, holder_did_document: dict) -> bool:
    """Verifies a credential presented by the holder, retrieving the full VC from IPFS."""
    print("VERIFIER: Verifying presented credential reference...")
    
    if vc_reference.get("type") != "VerifiableCredentialReference" or "cid" not in vc_reference:
        print("VERIFIER: Invalid credential reference format.")
        return False

    # Step 1: Retrieve the full VC from IPFS using the CID
    full_vc = retrieve_content_from_ipfs(vc_reference["cid"])
    
    if not full_vc:
        print("VERIFIER: Failed to retrieve full VC from IPFS. Verification failed.")
        return False

    # Step 2: Check if the credential subject matches the holder's DID
    if full_vc["credentialSubject"]["id"] != HOLDER_DID:
        print("VERIFIER: Credential subject does not match holder's DID. Verification failed.")
        return False
    
    # Step 3: In a real system, we would use the holder's public key to verify the signature.
    # Here, we just simulate a successful signature check.
    if "proof" in full_vc and full_vc["proof"]["jws"]:
        print("VERIFIER: Credential signature is valid (simulated).")
    else:
        print("VERIFIER: Credential signature is missing or invalid. Verification failed.")
        return False

    print("VERIFIER: Credential verified successfully!\n")
    return True
if __name__ == "__main__":
    print("--- Starting SSI Resolution Protocol PoC (Web3 Refactor & Refined) ---\n")

    # --- Setup: Store VC on IPFS and create reference ---
    print("--- Setup: Storing full VC on IPFS (CBA) ---")
    vc_cid = store_content_on_ipfs(ORIGINAL_VERIFIABLE_CREDENTIAL)
    VERIFIABLE_CREDENTIAL_REFERENCE["cid"] = vc_cid
    print("-" * 50)

    # --- Test Case 1: Valid DID Resolution and Verification (with CBA) ---
    print("--- Test Case 1: Valid DID Resolution and Verification (with CBA) ---")
    holder_did_document = resolve_did(HOLDER_DID)

    if holder_did_document:
        # Step 2: Holder presents the Verifiable Credential Reference
        print(f"HOLDER: Presenting my Verifiable Credential Reference to the service:\n{json.dumps(VERIFIABLE_CREDENTIAL_REFERENCE, indent=2)}\n")

        # Step 3: Verifier verifies the credential (which now retrieves from IPFS)
        is_valid = verify_credential(VERIFIABLE_CREDENTIAL_REFERENCE, holder_did_document)

        # Step 4: Verifier grants access based on verification
        if is_valid:
            # We need to retrieve the degree info from the original VC for the final message
            degree_info = ORIGINAL_VERIFIABLE_CREDENTIAL['credentialSubject']['degree']['name']
            print(f"SERVICE: Access granted. Welcome, holder of a '{degree_info}'.")
        else:
            print("SERVICE: Access denied. Credential could not be verified.")
    print("-" * 50)

    # --- Test Case 2: Non-Existent DID Resolution (Error Handling) ---
    print("--- Test Case 2: Non-Existent DID Resolution (Error Handling) ---")
    NON_EXISTENT_DID = "did:phi:nonexistent12345"
    non_existent_did_document = resolve_did(NON_EXISTENT_DID)

    if not non_existent_did_document:
        print(f"VERIFIER: Successfully handled non-existent DID: {NON_EXISTENT_DID}")
    print("-" * 50)

    print("\n--- SSI Resolution Protocol PoC Finished ---")
