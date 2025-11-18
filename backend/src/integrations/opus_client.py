"""
Opus Job Operator API Client
Integrates Genesis Auditor with Opus workflow automation platform
"""

import os
import requests
from typing import Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class OpusClient:
    """
    Client for Opus Job Operator API
    Triggers and manages Opus workflows from Genesis Auditor
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        workflow_id: Optional[str] = None
    ):
        """
        Initialize Opus API client

        Args:
            api_key: Opus API key (or set OPUS_API_KEY env var)
            base_url: Opus API base URL (or set OPUS_BASE_URL env var)
            workflow_id: Default workflow ID (or set OPUS_WORKFLOW_ID env var)
        """
        self.api_key = api_key or os.getenv('OPUS_API_KEY')
        self.base_url = base_url or os.getenv('OPUS_BASE_URL', 'https://api.opus.com')
        self.workflow_id = workflow_id or os.getenv('OPUS_WORKFLOW_ID')

        if not self.api_key:
            print("⚠️  Warning: OPUS_API_KEY not configured")

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_workflow_schema(self, workflow_id: Optional[str] = None) -> Dict:
        """
        Get workflow schema from Opus

        Args:
            workflow_id: Workflow ID (uses default if not provided)

        Returns:
            Workflow schema including input/output definitions
        """
        wf_id = workflow_id or self.workflow_id
        if not wf_id:
            raise ValueError("workflow_id required")

        url = f"{self.base_url}/workflow/{wf_id}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to get Opus workflow schema: {e}")
            raise

    def initiate_job(
        self,
        input_data: Dict[str, Any],
        workflow_id: Optional[str] = None,
        job_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Initiate an Opus workflow job

        Args:
            input_data: Input data for the workflow (matches workflow input schema)
            workflow_id: Workflow ID (uses default if not provided)
            job_metadata: Optional metadata for job tracking

        Returns:
            Job initiation response with job_id
        """
        wf_id = workflow_id or self.workflow_id
        if not wf_id:
            raise ValueError("workflow_id required")

        url = f"{self.base_url}/jobs/initiate"

        payload = {
            "workflow_id": wf_id,
            "input": input_data,
            "metadata": job_metadata or {
                "source": "genesis-auditor",
                "timestamp": datetime.now().isoformat()
            }
        }

        try:
            print(f"📤 Initiating Opus job for workflow: {wf_id}")
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()

            result = response.json()
            job_id = result.get('job_id')
            print(f"✅ Opus job initiated: {job_id}")

            return result
        except Exception as e:
            print(f"❌ Failed to initiate Opus job: {e}")
            raise

    def get_job_status(self, job_id: str) -> Dict:
        """
        Get status of an Opus job

        Args:
            job_id: Job ID from initiate_job response

        Returns:
            Job status and results
        """
        url = f"{self.base_url}/jobs/{job_id}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to get Opus job status: {e}")
            raise

    def trigger_audit_completed_workflow(
        self,
        domain: str,
        target_api_name: str,
        compliance_score: int,
        risk_level: str,
        vulnerabilities_found: int,
        duration_seconds: float,
        critical_vulnerabilities: Optional[list] = None
    ) -> Dict:
        """
        Trigger Opus workflow when Genesis audit completes

        Args:
            domain: Security domain (HIPAA, PCI-DSS, etc.)
            target_api_name: Name of audited API
            compliance_score: Score 0-100
            risk_level: LOW/MEDIUM/HIGH/CRITICAL
            vulnerabilities_found: Total count
            duration_seconds: Audit duration
            critical_vulnerabilities: List of critical vulnerability names

        Returns:
            Opus job response
        """
        input_data = {
            "event_type": "audit_completed",
            "audit_data": {
                "domain": domain,
                "target_api": target_api_name,
                "compliance_score": compliance_score,
                "risk_level": risk_level,
                "vulnerabilities_found": vulnerabilities_found,
                "duration_seconds": duration_seconds,
                "critical_vulnerabilities": critical_vulnerabilities or [],
                "timestamp": datetime.now().isoformat()
            }
        }

        return self.initiate_job(
            input_data=input_data,
            job_metadata={
                "event": "audit_completed",
                "domain": domain,
                "target": target_api_name
            }
        )

    def trigger_critical_vulnerability_workflow(
        self,
        domain: str,
        target_api_name: str,
        critical_vulnerabilities: list
    ) -> Dict:
        """
        Trigger Opus workflow for critical vulnerabilities (immediate alert)

        Args:
            domain: Security domain
            target_api_name: API name
            critical_vulnerabilities: List of critical vulns with details

        Returns:
            Opus job response
        """
        input_data = {
            "event_type": "critical_vulnerability_alert",
            "alert_data": {
                "domain": domain,
                "target_api": target_api_name,
                "critical_count": len(critical_vulnerabilities),
                "vulnerabilities": critical_vulnerabilities,
                "timestamp": datetime.now().isoformat(),
                "severity": "CRITICAL",
                "requires_immediate_action": True
            }
        }

        return self.initiate_job(
            input_data=input_data,
            job_metadata={
                "event": "critical_alert",
                "priority": "P0",
                "domain": domain
            }
        )


# Singleton instance
_opus_client = None

def get_opus_client() -> Optional[OpusClient]:
    """Get or create Opus client singleton"""
    global _opus_client

    # Only create if API key is configured
    if os.getenv('OPUS_API_KEY'):
        if _opus_client is None:
            _opus_client = OpusClient()
        return _opus_client
    else:
        return None
