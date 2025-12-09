'''
Proof-of-Concept for Decentralized Physical Infrastructure Networks (DePIN) Incentive Simulation.

This script simulates a basic incentive mechanism for a DePIN storage network:
1.  A storage provider registers their service.
2.  The provider submits a "Proof of Service" (PoS).
3.  The network validates the PoS and issues a simulated token reward.
'''

import random
import json
from typing import Dict, Any

# --- 1. Simulated Network State ---
# In a real system, this would be managed by the Phi Chain smart contracts.
NETWORK_STATE = {
    "total_supply": 1000000,
    "providers": {}  # {provider_id: {"service_type": "storage", "reputation": 0, "balance": 0}}
}

# --- 2. DePIN Logic ---

def register_provider(provider_id: str, service_type: str) -> bool:
    """Registers a new infrastructure provider to the network."""
    if provider_id in NETWORK_STATE["providers"]:
        print(f"DEPIN: Provider {provider_id} already registered.")
        return False
    
    NETWORK_STATE["providers"][provider_id] = {
        "service_type": service_type,
        "reputation": 10, # Starting reputation
        "balance": 0
    }
    print(f"DEPIN: Provider {provider_id} registered for {service_type} service.")
    return True

def submit_proof_of_service(provider_id: str, work_units: int) -> bool:
    """Simulates a provider submitting proof of completed work."""
    if provider_id not in NETWORK_STATE["providers"]:
        print(f"DEPIN: Error - Provider {provider_id} not registered.")
        return False
    
    # --- Simulated Validation ---
    # In a real system, this would involve cryptographic proof verification.
    is_valid = work_units > 0 and random.random() < 0.95 # 95% chance of valid proof
    
    if is_valid:
        print(f"DEPIN: Proof of Service from {provider_id} is VALID. Work units: {work_units}")
        issue_reward(provider_id, work_units)
        return True
    else:
        print(f"DEPIN: Proof of Service from {provider_id} is INVALID. No reward issued.")
        # Penalize reputation for invalid proof
        NETWORK_STATE["providers"][provider_id]["reputation"] -= 1
        return False

def issue_reward(provider_id: str, work_units: int):
    """Calculates and issues a token reward based on work units and reputation."""
    provider = NETWORK_STATE["providers"][provider_id]
    
    # Simple reward formula: Reward = Work Units * Base Rate * (Reputation Multiplier)
    BASE_RATE = 0.5 # Tokens per work unit
    reputation_multiplier = provider["reputation"] / 10.0
    
    reward = work_units * BASE_RATE * reputation_multiplier
    
    provider["balance"] += reward
    provider["reputation"] += 0.5 # Small reputation boost for successful work
    
    print(f"DEPIN: Reward issued to {provider_id}: {reward:.2f} PHI Tokens.")
    print(f"DEPIN: New Balance: {provider['balance']:.2f}, New Reputation: {provider['reputation']:.1f}")

# --- Main Execution: Simulating the DePIN Flow ---
if __name__ == "__main__":
    print("--- Starting DePIN Incentive Simulation PoC ---\n")

    PROVIDER_A = "storage_node_001"
    
    # Step 1: Register Provider
    register_provider(PROVIDER_A, "storage")
    
    # Step 2: Submit successful Proof of Service
    print("\n--- First Service Submission (Success) ---")
    submit_proof_of_service(PROVIDER_A, 100)
    
    # Step 3: Submit a second, larger Proof of Service
    print("\n--- Second Service Submission (Success) ---")
    submit_proof_of_service(PROVIDER_A, 250)
    
    # Step 4: Simulate a failed submission (for demonstration, we force a failure)
    print("\n--- Third Service Submission (Simulated Failure) ---")
    # Temporarily override the random check to force a failure for demonstration
    random.seed(0) # Seed the random number generator to ensure the failure
    submit_proof_of_service(PROVIDER_A, 50)
    random.seed(None) # Reset seed
    
    print("\n--- DePIN Incentive Simulation PoC Finished ---")
    print("\nFinal Network State Summary:")
    print(json.dumps(NETWORK_STATE["providers"][PROVIDER_A], indent=2))
