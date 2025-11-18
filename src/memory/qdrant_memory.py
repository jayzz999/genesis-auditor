"""
Qdrant Memory System - The Genesis Agent's Persistent Memory
Stores and retrieves successful attack patterns across audits
"""

import os
import json
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    PayloadSchemaType
)
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import hashlib

# Load environment variables
load_dotenv()


class GenesisMemory:
    """
    Vector-based memory system for storing and retrieving attack patterns
    """

    def __init__(
        self,
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None,
        collection_name: str = "attack_patterns"
    ):
        """Initialize the memory system"""
        self.qdrant_url = qdrant_url or os.getenv('QDRANT_URL')
        self.qdrant_api_key = qdrant_api_key or os.getenv('QDRANT_API_KEY')
        self.collection_name = collection_name

        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("Qdrant URL and API key required")

        # Initialize Qdrant client
        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key
        )

        # Initialize embedding model
        print("📥 Loading embedding model...")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded")

        # Ensure collection exists
        self._ensure_collection()
        print(f"✅ Genesis Memory initialized with Qdrant")

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            print(f"🔨 Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,  # all-MiniLM-L6-v2 embedding size
                    distance=Distance.COSINE
                )
            )

            # Create index for domain field to enable filtering
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="domain",
                field_schema=PayloadSchemaType.KEYWORD
            )

            print(f"✅ Collection created: {self.collection_name}")
        else:
            print(f"✅ Collection already exists: {self.collection_name}")

    def store_attack_pattern(
        self,
        domain: str,
        attack_name: str,
        attack_description: str,
        attack_method: str,
        target_vulnerability: str,
        severity: str,
        success_rate: float,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Store a successful attack pattern in memory

        Args:
            domain: Security domain (e.g., "HIPAA", "Financial Fraud")
            attack_name: Name of the attack
            attack_description: Full description
            attack_method: Technical method used
            target_vulnerability: What it exploits
            severity: LOW/MEDIUM/HIGH/CRITICAL
            success_rate: 0.0 to 1.0
            metadata: Additional metadata

        Returns:
            ID of the stored pattern
        """
        # Create searchable text (what we embed)
        searchable_text = f"{domain} {attack_name} {attack_description} {attack_method} {target_vulnerability}"

        # Generate embedding
        vector = self.encoder.encode(searchable_text).tolist()

        # Create unique ID
        pattern_id = hashlib.md5(searchable_text.encode()).hexdigest()

        # Prepare payload
        payload = {
            "domain": domain,
            "attack_name": attack_name,
            "attack_description": attack_description,
            "attack_method": attack_method,
            "target_vulnerability": target_vulnerability,
            "severity": severity,
            "success_rate": success_rate,
            "searchable_text": searchable_text
        }

        # Add optional metadata
        if metadata:
            payload.update(metadata)

        # Store in Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(
                id=pattern_id,
                vector=vector,
                payload=payload
            )]
        )

        print(f"💾 Stored attack pattern: {attack_name} (ID: {pattern_id[:8]}...)")
        return pattern_id

    def retrieve_relevant_attacks(
        self,
        domain: str,
        query: Optional[str] = None,
        top_k: int = 5,
        min_success_rate: float = 0.0
    ) -> List[Dict]:
        """
        Retrieve relevant attack patterns from memory

        Args:
            domain: Security domain to search within
            query: Optional specific query (if None, uses domain)
            top_k: Number of results to return
            min_success_rate: Minimum success rate threshold

        Returns:
            List of relevant attack patterns
        """
        # Build search query
        search_query = query or f"{domain} vulnerabilities attacks exploits"

        print(f"🔍 Searching memory for: {search_query}")

        # Generate query embedding
        query_vector = self.encoder.encode(search_query).tolist()

        # Build filter for domain
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="domain",
                    match=MatchValue(value=domain)
                )
            ]
        )

        # Search Qdrant
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=search_filter,
            limit=top_k * 2  # Get extra results to filter
        )

        # Filter by success rate and format
        relevant_attacks = []
        for hit in results:
            if hit.payload.get('success_rate', 0) >= min_success_rate:
                relevant_attacks.append({
                    'attack': hit.payload.get('attack_name'),
                    'description': hit.payload.get('attack_description'),
                    'method': hit.payload.get('attack_method'),
                    'target': hit.payload.get('target_vulnerability'),
                    'severity': hit.payload.get('severity'),
                    'success_rate': hit.payload.get('success_rate'),
                    'relevance_score': hit.score
                })

                if len(relevant_attacks) >= top_k:
                    break

        print(f"📊 Found {len(relevant_attacks)} relevant attacks")
        return relevant_attacks

    def get_memory_stats(self) -> Dict:
        """Get statistics about stored memories"""
        collection_info = self.client.get_collection(self.collection_name)

        return {
            "total_patterns": collection_info.points_count,
            "collection_name": self.collection_name,
            "vector_size": 384
        }

    def clear_all_memories(self):
        """⚠️ WARNING: Deletes all stored attack patterns"""
        print("⚠️  Clearing all memories...")
        self.client.delete_collection(self.collection_name)
        self._ensure_collection()
        print("✅ All memories cleared")


def seed_initial_attack_patterns(memory: GenesisMemory):
    """
    Pre-seed the memory with realistic attack patterns
    This is our "head start" for the demo
    """
    print("\n" + "=" * 60)
    print("🌱 SEEDING INITIAL ATTACK PATTERNS")
    print("=" * 60)

    seed_patterns = [
        # HIPAA Compliance attacks
        {
            "domain": "HIPAA",
            "attack_name": "Unauthenticated PHI Access",
            "attack_description": "Direct access to patient health information endpoints without authentication",
            "attack_method": "Send GET requests to /api/patients/{id} without Authorization header",
            "target_vulnerability": "Missing authentication on PHI endpoints",
            "severity": "CRITICAL",
            "success_rate": 0.92
        },
        {
            "domain": "HIPAA",
            "attack_name": "SQL Injection on Patient Search",
            "attack_description": "SQL injection in patient search query parameter",
            "attack_method": "Inject SQL payload in search parameter: ?name='; DROP TABLE patients--",
            "target_vulnerability": "Unsanitized SQL queries in patient search",
            "severity": "CRITICAL",
            "success_rate": 0.87
        },
        {
            "domain": "HIPAA",
            "attack_name": "IDOR on Patient Records",
            "attack_description": "Insecure Direct Object Reference allows access to other patients' records",
            "attack_method": "Enumerate patient IDs and access records: /api/patients/1, /api/patients/2, etc.",
            "target_vulnerability": "No authorization check on patient ID parameter",
            "severity": "HIGH",
            "success_rate": 0.78
        },
        {
            "domain": "HIPAA",
            "attack_name": "Audit Log Manipulation",
            "attack_description": "Ability to delete or modify HIPAA audit logs",
            "attack_method": "POST to /api/audit/delete with log IDs to remove access traces",
            "target_vulnerability": "Insufficient access controls on audit log endpoints",
            "severity": "HIGH",
            "success_rate": 0.65
        },

        # Financial Fraud attacks
        {
            "domain": "Financial Fraud",
            "attack_name": "Transaction Amount Manipulation",
            "attack_description": "Manipulate transaction amounts through parameter tampering",
            "attack_method": "Intercept POST to /api/transfer and modify amount field before submission",
            "target_vulnerability": "Client-side validation only, no server-side verification",
            "severity": "CRITICAL",
            "success_rate": 0.83
        },
        {
            "domain": "Financial Fraud",
            "attack_name": "Race Condition in Balance Check",
            "attack_description": "Exploit race condition to withdraw more than account balance",
            "attack_method": "Send multiple simultaneous withdrawal requests before balance update",
            "target_vulnerability": "Non-atomic balance check and deduction",
            "severity": "CRITICAL",
            "success_rate": 0.71
        },
        {
            "domain": "Financial Fraud",
            "attack_name": "JWT Token Privilege Escalation",
            "attack_description": "Modify JWT claims to escalate from user to admin privileges",
            "attack_method": "Decode JWT, change 'role': 'admin', re-encode with weak secret",
            "target_vulnerability": "Weak JWT secret or no signature verification",
            "severity": "HIGH",
            "success_rate": 0.69
        },

        # API Security attacks
        {
            "domain": "API Security",
            "attack_name": "Rate Limit Bypass",
            "attack_description": "Bypass rate limiting through header manipulation",
            "attack_method": "Rotate X-Forwarded-For headers to circumvent IP-based rate limits",
            "target_vulnerability": "Rate limiting based only on client IP",
            "severity": "MEDIUM",
            "success_rate": 0.81
        },
        {
            "domain": "API Security",
            "attack_name": "GraphQL Query Depth Attack",
            "attack_description": "DoS attack through deeply nested GraphQL queries",
            "attack_method": "Send query with 50+ levels of nesting to exhaust server resources",
            "target_vulnerability": "No query depth or complexity limits",
            "severity": "HIGH",
            "success_rate": 0.76
        },
        {
            "domain": "API Security",
            "attack_name": "Mass Assignment Vulnerability",
            "attack_description": "Modify restricted fields through mass assignment",
            "attack_method": "Include 'isAdmin': true in POST /api/users registration payload",
            "target_vulnerability": "No whitelist of allowed fields in object creation",
            "severity": "HIGH",
            "success_rate": 0.74
        }
    ]

    for pattern in seed_patterns:
        memory.store_attack_pattern(**pattern)

    print(f"\n✅ Seeded {len(seed_patterns)} attack patterns")
    print("=" * 60)


def test_genesis_memory():
    """Test the memory system"""
    print("=" * 60)
    print("🧪 TESTING GENESIS MEMORY SYSTEM")
    print("=" * 60)

    # Initialize memory
    memory = GenesisMemory()

    # Clear any existing data for clean test
    memory.clear_all_memories()

    # Seed initial patterns
    seed_initial_attack_patterns(memory)

    # Test retrieval
    print("\n" + "=" * 60)
    print("🔍 TEST: Retrieve HIPAA-related attacks")
    print("=" * 60)

    hipaa_attacks = memory.retrieve_relevant_attacks(
        domain="HIPAA",
        top_k=3,
        min_success_rate=0.7
    )

    print("\n📊 Retrieved Attacks:")
    for i, attack in enumerate(hipaa_attacks, 1):
        print(f"\n{i}. {attack['attack']}")
        print(f"   Severity: {attack['severity']}")
        print(f"   Success Rate: {attack['success_rate']:.0%}")
        print(f"   Relevance: {attack['relevance_score']:.3f}")
        print(f"   Method: {attack['method'][:80]}...")

    # Test with specific query
    print("\n" + "=" * 60)
    print("🔍 TEST: Search for 'patient data access' vulnerabilities")
    print("=" * 60)

    specific_attacks = memory.retrieve_relevant_attacks(
        domain="HIPAA",
        query="patient data unauthorized access",
        top_k=2
    )

    print("\n📊 Retrieved Attacks:")
    for i, attack in enumerate(specific_attacks, 1):
        print(f"\n{i}. {attack['attack']}")
        print(f"   Target: {attack['target']}")
        print(f"   Relevance: {attack['relevance_score']:.3f}")

    # Get stats
    print("\n" + "=" * 60)
    print("📊 MEMORY STATISTICS")
    print("=" * 60)
    stats = memory.get_memory_stats()
    print(json.dumps(stats, indent=2))

    print("\n✅ GENESIS MEMORY TEST COMPLETE!")
    print("=" * 60)

    return memory


if __name__ == "__main__":
    test_genesis_memory()
