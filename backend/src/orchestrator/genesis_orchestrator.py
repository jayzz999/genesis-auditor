"""
Genesis Orchestrator - The Complete End-to-End Workflow
Coordinates: Memory → Agent Design → Attack Execution → Analysis
"""

import os
import sys
import json
from typing import Dict, Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.genesis_agent import GenesisAgent
from memory.qdrant_memory import GenesisMemory
from orchestrator.attack_executor import AttackExecutor
from utils.report_generator import GenesisReportGenerator
from integrations.webhook_manager import get_webhook_manager


class GenesisOrchestrator:
    """
    Master orchestrator for the entire Genesis Auditor workflow
    """

    def __init__(self):
        """Initialize all components"""
        print("\n" + "=" * 60)
        print("🚀 INITIALIZING GENESIS AUDITOR")
        print("=" * 60)

        print("🧠 Gemini is initializing...")
        self.genesis_agent = GenesisAgent(use_memory=True)

        print("⚔️  Attack execution engine loading...")
        self.executor = AttackExecutor()

        print("📊 Report generator initializing...")
        self.report_generator = GenesisReportGenerator()
        self.audit_results = None

        print("🔗 Webhook manager initializing...")
        self.webhook_manager = get_webhook_manager()

        print("✅ Genesis Auditor ready")
        print("=" * 60)

    def run_complete_audit(
        self,
        domain: str,
        target_api_name: str,
        target_api_config: Optional[Dict] = None
    ) -> Dict:
        """
        Run a complete security audit

        Args:
            domain: Security domain (e.g., "HIPAA", "Financial Fraud")
            target_api_name: Name of the target API
            target_api_config: Configuration for the target API

        Returns:
            Complete audit report
        """
        print("\n" + "=" * 70)
        print(f"🎯 GENESIS AUDIT: {domain}")
        print("=" * 70)

        audit_start_time = datetime.now()

        # Trigger audit.started webhook
        self.webhook_manager.trigger_webhook("audit.started", {
            "domain": domain,
            "target": target_api_name,
            "timestamp": audit_start_time.isoformat()
        })

        # Step 1: Design the agent swarm (with memory retrieval)
        print("\n📋 PHASE 1: AGENT SWARM DESIGN")
        print("-" * 70)
        print("🧠 Gemini is architecting the swarm...")
        print("💾 Querying Qdrant for relevant attack patterns...")

        agent_plan = self.genesis_agent.design_agent_swarm(
            domain=domain,
            target_api_info=target_api_name,
            auto_retrieve_memory=True
        )

        print(f"✨ Swarm designed: {agent_plan['swarm_architecture']['total_agents']} specialized agents created")
        print(f"🎯 Strategy: {agent_plan['reasoning'][:80]}...")

        # Step 2: Execute the attacks
        print("\n📋 PHASE 2: ATTACK EXECUTION")
        print("-" * 70)
        print("⚡ Executing HTTP injection attacks on target...")
        print("🔍 Analyzing API responses for vulnerability indicators...")

        target_config = target_api_config or {
            'api_name': target_api_name,
            'base_url': 'https://api.example.com'
        }

        attack_results = self.executor.execute_agent_swarm(agent_plan, target_config)

        vulnerable_count = len([r for r in attack_results if r.get('result') == 'VULNERABLE'])
        print(f"⚠️  Found {vulnerable_count} vulnerabilities across {len(attack_results)} attack vectors")

        # Step 3: Analyze results
        print("\n📋 PHASE 3: RESULTS ANALYSIS")
        print("-" * 70)
        print("🧠 Gemini is analyzing attack results...")
        print("📊 Calculating compliance scores and risk levels...")

        analysis = self.genesis_agent.analyze_results(attack_results)
        stats = self.executor.get_summary_statistics()

        print(f"📈 Compliance Score: {stats['compliance_score']}/100")
        print(f"🚨 Risk Level: {analysis.get('risk_level', 'UNKNOWN')}")

        # Step 4: Store successful attacks in memory
        print("\n📋 PHASE 4: MEMORY UPDATE")
        print("-" * 70)
        print("💾 Storing successful attack vectors in Qdrant...")
        print("🧠 Building vector embeddings for future retrieval...")

        self._store_findings_to_memory(domain, attack_results)

        print("✅ Memory updated - system is now smarter for future audits!")

        # Compile final report
        audit_end_time = datetime.now()
        duration = (audit_end_time - audit_start_time).total_seconds()

        self.audit_results = {
            'audit_metadata': {
                'domain': domain,
                'target': target_api_name,
                'timestamp': audit_start_time.isoformat(),
                'duration_seconds': duration
            },
            'agent_plan': agent_plan,
            'attack_results': attack_results,
            'statistics': stats,
            'analysis': analysis,
            'recommendations': self._generate_recommendations(attack_results, analysis)
        }

        print("\n" + "=" * 70)
        print("✅ AUDIT COMPLETE")
        print("=" * 70)

        self._print_executive_summary()

        # Trigger audit.completed webhook
        self.webhook_manager.trigger_webhook("audit.completed", {
            "domain": domain,
            "target": target_api_name,
            "compliance_score": stats['compliance_score'],
            "risk_level": analysis.get('risk_level'),
            "vulnerabilities_found": vulnerable_count,
            "duration_seconds": duration,
            "timestamp": audit_end_time.isoformat()
        })

        # Trigger critical vulnerability webhooks if needed
        critical_vulns = [
            r for r in attack_results
            if r.get('result') == 'VULNERABLE' and r.get('severity') == 'CRITICAL'
        ]
        if critical_vulns:
            self.webhook_manager.trigger_webhook("vulnerability.critical", {
                "domain": domain,
                "target": target_api_name,
                "critical_count": len(critical_vulns),
                "vulnerabilities": [v.get('attack') for v in critical_vulns]
            })

        return self.audit_results

    def _store_findings_to_memory(self, domain: str, attack_results: list):
        """Store successful attack findings to memory"""
        if not self.genesis_agent.memory:
            print("⚠️  Memory not available - skipping storage")
            return

        successful_attacks = [r for r in attack_results if r.get('result') == 'VULNERABLE']

        if len(successful_attacks) == 0:
            print("ℹ️  No successful attacks to store")
            return

        print(f"💾 Vectorizing {len(successful_attacks)} successful attack patterns...")

        for i, attack in enumerate(successful_attacks, 1):
            try:
                print(f"   [{i}/{len(successful_attacks)}] Storing: {attack.get('attack_name', 'Unknown')[:50]}...")
                self.genesis_agent.memory.store_attack_pattern(
                    domain=domain,
                    attack_name=attack.get('attack_name', 'Unknown'),
                    attack_description=attack.get('evidence', ''),
                    attack_method=attack.get('attack_method', ''),
                    target_vulnerability=attack.get('attack_name', ''),
                    severity=attack.get('severity', 'MEDIUM'),
                    success_rate=0.85,  # Confirmed successful
                    metadata={
                        'timestamp': attack.get('timestamp'),
                        'target': attack.get('target')
                    }
                )
            except Exception as e:
                print(f"   ⚠️  Failed to store attack: {e}")

        print(f"✅ Qdrant memory updated with {len(successful_attacks)} new attack patterns")

    def _generate_recommendations(self, attack_results: list, analysis: Dict) -> list:
        """Generate prioritized recommendations"""
        recommendations = []

        # Get unique recommendations from attacks
        for result in attack_results:
            if result.get('result') == 'VULNERABLE':
                rec = {
                    'priority': result.get('severity'),
                    'vulnerability': result.get('attack_name'),
                    'recommendation': result.get('recommendation'),
                    'impact': result.get('impact')
                }
                if rec not in recommendations:
                    recommendations.append(rec)

        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        recommendations.sort(key=lambda x: severity_order.get(x['priority'], 4))

        return recommendations

    def _print_executive_summary(self):
        """Print executive summary of the audit"""
        if not self.audit_results:
            return

        stats = self.audit_results['statistics']
        analysis = self.audit_results['analysis']

        print("\n" + "=" * 70)
        print("📊 EXECUTIVE SUMMARY")
        print("=" * 70)

        print(f"\n🎯 Domain: {self.audit_results['audit_metadata']['domain']}")
        print(f"🎯 Target: {self.audit_results['audit_metadata']['target']}")
        print(f"⏱️  Duration: {self.audit_results['audit_metadata']['duration_seconds']:.1f}s")

        print(f"\n📈 Compliance Score: {stats['compliance_score']}/100")
        print(f"🚨 Risk Level: {analysis.get('risk_level', 'UNKNOWN')}")

        print(f"\n📊 Attack Statistics:")
        print(f"   Total Attacks: {stats['total_attacks']}")
        print(f"   Vulnerabilities Found: {stats['vulnerabilities_found']}")
        print(f"   Critical Issues: {stats['critical_findings']}")
        print(f"   High Issues: {stats['high_findings']}")

        print(f"\n💡 Executive Summary:")
        print(f"   {analysis.get('executive_summary', 'Analysis unavailable')}")

        print("\n" + "=" * 70)

    def export_report_json(self, filename: Optional[str] = None) -> str:
        """Export audit report as JSON"""
        if not self.audit_results:
            raise ValueError("No audit results to export")

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = self.audit_results['audit_metadata']['domain'].replace(' ', '_')
            filename = f"genesis_audit_{domain}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(self.audit_results, f, indent=2)

        print(f"📄 Report exported: {filename}")
        return filename

    def export_report_pdf(self, filename: Optional[str] = None) -> str:
        """Export audit report as professional PDF"""
        if not self.audit_results:
            raise ValueError("No audit results to export")

        return self.report_generator.generate_report(self.audit_results, filename)


def run_demo_audit():
    """Run a demonstration audit"""
    print("\n" + "=" * 70)
    print("🎬 GENESIS AUDITOR - FULL DEMO")
    print("=" * 70)

    # Initialize orchestrator
    orchestrator = GenesisOrchestrator()

    # Run audit for HIPAA compliance
    orchestrator.run_complete_audit(
        domain="HIPAA",
        target_api_name="HealthCare Management API v2.1",
        target_api_config={
            'api_name': 'HealthCare Management API v2.1',
            'base_url': 'https://api.healthcare-demo.com',
            'version': '2.1'
        }
    )

    # Export reports
    json_file = orchestrator.export_report_json()
    pdf_file = orchestrator.export_report_pdf()

    print(f"\n✅ Demo complete!")
    print(f"   JSON Report: {json_file}")
    print(f"   PDF Report: {pdf_file}")


if __name__ == "__main__":
    run_demo_audit()
