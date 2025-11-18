"""
The Genesis Agent - The Brain of the System
This agent uses Gemini to autonomously design red-team agent swarms
"""

import os
import sys
import json
import google.generativeai as genai
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import memory system (will be used if available)
try:
    from memory.qdrant_memory import GenesisMemory
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    print("⚠️  Memory system not available")


class GenesisAgent:
    """
    The autonomous AI that designs other AI agents for security auditing
    """

    def __init__(self, api_key: Optional[str] = None, use_memory: bool = True):
        """Initialize the Genesis Agent with Gemini API and optional memory"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided")

        genai.configure(api_key=self.api_key)
        # Use stable Gemini 2.5 Flash for best performance and quota
        # Configure generation settings for better output control
        generation_config = {
            "temperature": 0.5,  # Lower temperature for more predictable JSON
            "top_p": 0.9,
            "top_k": 20,
            "max_output_tokens": 8192,  # Increased to prevent truncation mid-JSON
        }
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=generation_config
        )
        print("✅ Genesis Agent initialized with Gemini 2.5 Flash")

        # Initialize memory if enabled
        self.memory = None
        if use_memory and MEMORY_AVAILABLE:
            try:
                self.memory = GenesisMemory()
                print("✅ Memory system connected")
            except Exception as e:
                print(f"⚠️  Memory system unavailable: {e}")
                print("   Continuing without memory...")

    def design_agent_swarm(
        self,
        domain: str,
        past_attacks: Optional[List[Dict]] = None,
        target_api_info: Optional[str] = None,
        auto_retrieve_memory: bool = True
    ) -> Dict:
        """
        The core function: Design a custom agent swarm for a specific domain

        Args:
            domain: The security domain (e.g., "HIPAA Compliance", "Financial Fraud")
            past_attacks: List of past successful attacks from memory (manually provided)
            target_api_info: Information about the target API
            auto_retrieve_memory: Automatically retrieve relevant attacks from memory

        Returns:
            Dict containing the agent swarm design
        """
        print(f"\n🧠 Genesis Agent is designing swarm for: {domain}")

        # Retrieve from memory if available and not manually provided
        if past_attacks is None and self.memory and auto_retrieve_memory:
            print("🔍 Querying memory for relevant past attacks...")
            past_attacks = self.memory.retrieve_relevant_attacks(
                domain=domain,
                top_k=5,
                min_success_rate=0.65
            )
            if past_attacks:
                print(f"📚 Retrieved {len(past_attacks)} relevant attacks from memory")
            else:
                print("📚 No relevant attacks found in memory")

        # Build context from past attacks
        attack_context = ""
        if past_attacks:
            attack_context = "\n\nPAST SUCCESSFUL ATTACKS FROM MEMORY (Learn from these!):\n"
            for i, attack in enumerate(past_attacks, 1):
                attack_context += f"\n{i}. {attack.get('attack', 'N/A')}\n"
                attack_context += f"   Method: {attack.get('method', 'N/A')}\n"
                attack_context += f"   Target: {attack.get('target', 'N/A')}\n"
                attack_context += f"   Severity: {attack.get('severity', 'N/A')}\n"
                attack_context += f"   Success Rate: {attack.get('success_rate', 0):.0%}\n"

                # Include full payload/technique details
                if attack.get('payload'):
                    attack_context += f"   Payload: {attack.get('payload')}\n"
                if attack.get('technique'):
                    attack_context += f"   Technique: {attack.get('technique')}\n"
                if attack.get('success_conditions'):
                    attack_context += f"   Success Conditions: {attack.get('success_conditions')}\n"
                if attack.get('evidence'):
                    attack_context += f"   Evidence Pattern: {attack.get('evidence')}\n"

                attack_context += "\n"

        # The master prompt that showcases Gemini's intelligence
        prompt = f"""You are a GRANDMASTER SECURITY RESEARCHER and ELITE AI SECURITY ARCHITECT with deep expertise in penetration testing, vulnerability research, and adversarial system design.

YOUR MISSION: Design a highly sophisticated, multi-agent red-team swarm to audit APIs for {domain} violations. You must demonstrate ADVANCED REASONING by creating agents with distinct personas, specialized attack methodologies, and tactical coordination strategies.

{attack_context}

ADVANCED DESIGN REQUIREMENTS:

1. **Agent Personas & Specialization**: Create 3-4 specialized agents where:
   - Each agent has a UNIQUE tactical persona (e.g., "The Distractor", "The Injector", "The Escalator")
   - Each persona reflects a different attack philosophy and methodology
   - Agents should complement each other's capabilities in a coordinated assault

2. **Attack Vector Intelligence**: For each agent, design 3-4 attack vectors that:
   - Exploit REAL vulnerabilities specific to {domain}
   - Show understanding of the attack chain (reconnaissance → exploitation → impact)
   - Include technical details that demonstrate deep security knowledge
   - Consider both common and advanced/novel attack techniques

3. **Memory-Augmented Learning**: If past successful attacks are provided:
   - Analyze patterns and adapt proven techniques
   - Combine multiple past attacks into sophisticated new vectors
   - Show reasoning about WHY certain attacks work for this domain

4. **Strategic Coordination**: Design swarm coordination where:
   - Early agents gather intelligence for later agents
   - Attack sequence maximizes discovery potential
   - Agents can pivot based on discovered vulnerabilities

OUTPUT FORMAT (must be valid JSON):
{{
  "domain": "{domain}",
  "reasoning": "Your strategic thinking: WHY this swarm design is optimal for finding {domain} vulnerabilities (1-2 sentences)",
  "swarm_architecture": {{
    "total_agents": <number>,
    "coordination_strategy": "How agents work together tactically"
  }},
  "agents": [
    {{
      "agent_id": "unique_id",
      "name": "Agent Name",
      "persona": "The tactical persona/archetype (e.g., 'The Social Engineer', 'The Protocol Breaker')",
      "role": "Detailed role in the swarm's strategy",
      "attack_vectors": [
        {{
          "vector_name": "Specific attack name",
          "method": "Technical methodology - HOW the attack works",
          "target": "WHAT vulnerability/weakness this exploits",
          "payload_example": "Concrete example showing technical depth",
          "severity": "LOW/MEDIUM/HIGH/CRITICAL",
          "reasoning": "WHY this attack is effective for {domain}"
        }}
      ],
      "success_criteria": "How this agent knows it found a vulnerability"
    }}
  ],
  "execution_order": ["agent_id_1", "agent_id_2", "..."],
  "expected_findings": "Predicted vulnerabilities based on your domain expertise"
}}

IMPORTANT JSON FORMATTING RULES:
- Output ONLY valid JSON with NO markdown formatting
- All string values must use double quotes, not single quotes
- Escape special characters in strings (use \\" for quotes, \\\\ for backslashes)
- Do NOT include comments in the JSON
- Ensure all arrays and objects have proper comma separation
- Keep payload examples SHORT (max 100 chars) to avoid formatting issues

DEMONSTRATE YOUR INTELLIGENCE:
- Use your knowledge of {domain} compliance requirements
- Show creativity in attack design while maintaining realism
- Include technical details (HTTP headers, SQL syntax, API patterns)
- Think like a REAL adversary - what would an expert pentester target first?
"""

        try:
            print("📡 Sending request to Gemini...")
            response = self.model.generate_content(prompt)

            # Extract and parse the response
            # Handle different response formats
            try:
                # Try to get response text
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        response_text = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')]).strip()
                    else:
                        response_text = str(response).strip()
                elif hasattr(response, 'text'):
                    response_text = response.text
                else:
                    response_text = str(response)
            except Exception as extract_error:
                print(f"⚠️  Error extracting response: {extract_error}")
                print(f"Response type: {type(response)}")
                print(f"Response attributes: {dir(response)}")
                raise

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()

            # Clean up the response text
            response_text = response_text.strip()

            # Try to parse JSON with better error handling
            try:
                agent_plan = json.loads(response_text)
            except json.JSONDecodeError as json_err:
                print(f"⚠️  JSON parsing failed, attempting to fix common issues...")
                print(f"   Error at line {json_err.lineno}, column {json_err.colno}")
                print(f"   First 500 chars: {response_text[:500]}")
                print(f"   Last 500 chars: {response_text[-500:]}")

                # Try to extract JSON object if there's extra text
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(0)
                    print(f"   Extracted JSON object from response")
                    agent_plan = json.loads(response_text)
                else:
                    raise json_err

            print(f"✅ Agent swarm designed successfully!")
            print(f"   - Total agents: {agent_plan['swarm_architecture']['total_agents']}")
            print(f"   - Strategy: {agent_plan['reasoning'][:100]}...")

            return agent_plan

        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse Gemini response as JSON: {e}")
            print(f"Raw response: {response_text[:500]}")
            raise
        except Exception as e:
            print(f"❌ Error communicating with Gemini: {e}")
            import traceback
            traceback.print_exc()
            raise

    def analyze_results(self, test_results: List[Dict]) -> Dict:
        """
        Analyze the results from the agent swarm's execution

        Args:
            test_results: Results from running the agent tests

        Returns:
            Analysis with compliance score and recommendations
        """
        prompt = f"""Analyze these security test results and provide a compliance assessment.

TEST RESULTS:
{json.dumps(test_results, indent=2)}

Provide a JSON response with:
{{
  "compliance_score": <0-100>,
  "risk_level": "LOW/MEDIUM/HIGH/CRITICAL",
  "vulnerabilities_found": <count>,
  "critical_issues": ["list of critical findings"],
  "recommendations": ["prioritized recommendations"],
  "executive_summary": "2-3 sentence summary for executives"
}}
"""

        try:
            response = self.model.generate_content(prompt)

            # Extract response text using the same logic as design_agent_swarm
            try:
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        response_text = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')]).strip()
                    else:
                        response_text = str(response).strip()
                elif hasattr(response, 'text'):
                    response_text = response.text
                else:
                    response_text = str(response)
            except Exception as extract_error:
                print(f"⚠️  Error extracting response: {extract_error}")
                raise

            # Clean markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            return json.loads(response_text)
        except Exception as e:
            print(f"❌ Error analyzing results: {e}")
            import traceback
            traceback.print_exc()
            # Return a default analysis
            return {
                "compliance_score": 50,
                "risk_level": "MEDIUM",
                "vulnerabilities_found": len(test_results),
                "critical_issues": ["Analysis failed"],
                "recommendations": ["Manual review required"],
                "executive_summary": "Automated analysis encountered an error."
            }


def test_genesis_agent():
    """Test the Genesis Agent with memory integration"""
    print("=" * 60)
    print("🧪 TESTING GENESIS AGENT WITH MEMORY")
    print("=" * 60)

    # Initialize with memory
    agent = GenesisAgent(use_memory=True)

    # Test 1: Design a swarm WITH automatic memory retrieval
    print("\n📋 TEST 1: Design swarm for HIPAA Compliance (with memory retrieval)")
    result = agent.design_agent_swarm(
        domain="HIPAA",
        target_api_info="Healthcare API that stores patient records",
        auto_retrieve_memory=True
    )

    print("\n" + "=" * 60)
    print("📊 MEMORY-ENHANCED AGENT SWARM DESIGN:")
    print("=" * 60)
    print(json.dumps(result, indent=2))

    # Test 2: Design for a different domain
    print("\n\n📋 TEST 2: Design swarm for Financial Fraud (with memory retrieval)")
    result_financial = agent.design_agent_swarm(
        domain="Financial Fraud",
        target_api_info="Banking API for transactions and transfers",
        auto_retrieve_memory=True
    )

    print("\n" + "=" * 60)
    print("📊 FINANCIAL FRAUD SWARM DESIGN:")
    print("=" * 60)
    print(f"Domain: {result_financial.get('domain')}")
    print(f"Total Agents: {result_financial.get('swarm_architecture', {}).get('total_agents')}")
    print(f"Strategy: {result_financial.get('reasoning', '')[:200]}...")
    print(f"\nAgents:")
    for i, agent_info in enumerate(result_financial.get('agents', []), 1):
        print(f"  {i}. {agent_info.get('name')} - {agent_info.get('role', '')[:60]}...")

    # Show memory stats
    if agent.memory:
        print("\n" + "=" * 60)
        print("📊 MEMORY STATISTICS")
        print("=" * 60)
        stats = agent.memory.get_memory_stats()
        print(json.dumps(stats, indent=2))

    print("\n✅ GENESIS AGENT WITH MEMORY TEST COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    test_genesis_agent()
