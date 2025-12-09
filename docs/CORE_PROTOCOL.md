# Core Protocol Definition: The Unified Information Fabric

This document outlines the high-level interaction protocol for the Lightning Bolt Network, focusing on how the three core pillars—Self-Sovereign Identity (SSI), Content-Based Addressing (CBA), and Decentralized Physical Infrastructure Networks (DePIN)—are unified by the Phi Chain Nexus.

## 1. The Phi Chain Nexus (DLT Layer)

The Phi Chain acts as the immutable, low-trust coordination layer. All critical metadata, such as DID documents, DePIN reward claims, and content metadata, is anchored here.

| Function | Pillar | Mechanism |
| :--- | :--- | :--- |
| **Identity Anchor** | SSI | Stores the public keys and service endpoints for all Decentralized Identifiers (DIDs). |
| **Incentive Engine** | DePIN | Smart contracts verify resource contribution proofs (e.g., proof-of-coverage, proof-of-storage) and distribute Phi Chain tokens as rewards. |
| **Content Registry** | CBA | Optional: Registers Content Identifiers (CIDs) with associated metadata (e.g., payment terms, access control policies). |

## 2. Identity Resolution Protocol (SSI)

When a user (Holder) needs to prove an attribute to a service (Verifier):

1.  **Resolution:** The Verifier resolves the Holder's DID via the Phi Chain Nexus to retrieve the public key and service endpoints.
2.  **Presentation:** The Holder uses their private key to create a Verifiable Presentation (VP) containing a Verifiable Credential (VC) issued by a trusted Issuer.
3.  **Verification:** The Verifier verifies the VP's signature using the public key retrieved from the Phi Chain.
4.  **Access:** Access is granted based on the verified claim, without the Verifier needing to store the user's personal data.

## 3. Content Retrieval Protocol (CBA + DePIN)

When a user requests content via a Content Identifier (CID):

1.  **Request:** The user requests the CID from the network.
2.  **Routing:** The network (e.g., an IPFS-like layer) routes the request to nodes that have advertised they store the content.
3.  **Storage Proof:** The storage node (a DePIN participant) provides a cryptographic proof-of-storage (PoS) to the Phi Chain, confirming the content's integrity and availability.
4.  **Transfer & Reward:** The content is transferred. The Phi Chain's Incentive Engine rewards the storage node based on the successful transfer and the verified PoS.

This protocol ensures that the network is **Self-Sovereign** (Identity), **Content-Addressed** (Data), and **Resilient** (Infrastructure).
