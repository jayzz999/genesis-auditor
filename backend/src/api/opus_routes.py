"""
Opus Monitoring API Routes
Provides endpoints for Opus workflow monitoring UI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import os

from integrations.opus_client import get_opus_client

router = APIRouter(prefix="/api/opus", tags=["opus"])

# In-memory job store (in production, use database)
job_executions: List[Dict] = []


class TriggerJobRequest(BaseModel):
    domain: str
    eventType: str


@router.get("/jobs")
async def get_jobs():
    """Get all Opus job executions"""
    return {"jobs": job_executions}


@router.post("/trigger")
async def trigger_job(request: TriggerJobRequest):
    """Manually trigger an Opus workflow job"""
    opus_client = get_opus_client()

    if not opus_client:
        raise HTTPException(
            status_code=503,
            detail="Opus integration not configured. Please set OPUS_API_KEY environment variable."
        )

    try:
        # Create mock audit data for manual trigger
        audit_data = {
            "domain": request.domain,
            "target_api": f"{request.domain} API",
            "compliance_score": 75,  # Mock data
            "risk_level": "MEDIUM",
            "vulnerabilities_found": 5,
            "duration_seconds": 120.5,
            "critical_vulnerabilities": [],
            "timestamp": datetime.utcnow().isoformat()
        }

        # Trigger the workflow
        if request.eventType == "audit_completed":
            response = opus_client.trigger_audit_completed_workflow(
                domain=request.domain,
                target_api_name=f"{request.domain} API",
                compliance_score=75,
                risk_level="MEDIUM",
                vulnerabilities_found=5,
                duration_seconds=120.5,
                critical_vulnerabilities=[]
            )
        else:
            # Critical vulnerability alert
            response = opus_client.trigger_critical_vulnerability_workflow(
                domain=request.domain,
                target_api_name=f"{request.domain} API",
                critical_vulnerabilities=[
                    {
                        "name": "SQL Injection",
                        "description": "Critical SQL injection vulnerability",
                        "severity": "CRITICAL"
                    }
                ]
            )

        job_id = response.get("job_id")

        # Store job execution for monitoring
        job_execution = {
            "id": job_id,
            "title": f"Genesis Audit - {request.eventType} - {request.domain}",
            "status": "running",
            "startedAt": datetime.utcnow().isoformat(),
            "auditData": {
                "domain": request.domain,
                "criticalCount": 1 if request.eventType == "critical_vulnerability_alert" else 0,
                "highCount": 2,
                "riskScore": 75
            }
        }

        job_executions.insert(0, job_execution)  # Add to beginning

        # Keep only last 50 jobs
        if len(job_executions) > 50:
            job_executions.pop()

        return {
            "success": True,
            "jobExecutionId": job_id,
            "status": "initiated",
            "message": f"Opus workflow triggered successfully for {request.domain}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger Opus workflow: {str(e)}"
        )


@router.get("/stats")
async def get_stats():
    """Get Opus integration statistics"""
    total_jobs = len(job_executions)
    succeeded = sum(1 for j in job_executions if j.get("status") == "succeeded")
    failed = sum(1 for j in job_executions if j.get("status") == "failed")
    running = sum(1 for j in job_executions if j.get("status") == "running")

    return {
        "total_jobs": total_jobs,
        "succeeded": succeeded,
        "failed": failed,
        "running": running,
        "success_rate": round((succeeded / total_jobs * 100) if total_jobs > 0 else 0, 2)
    }


@router.post("/jobs/{job_id}/complete")
async def mark_job_complete(job_id: str, success: bool = True):
    """Mark a job as completed (for testing/simulation)"""
    for job in job_executions:
        if job["id"] == job_id:
            job["status"] = "succeeded" if success else "failed"
            job["completedAt"] = datetime.utcnow().isoformat()
            job["duration"] = 45.2  # Mock duration
            return {"success": True, "job": job}

    raise HTTPException(status_code=404, detail="Job not found")
