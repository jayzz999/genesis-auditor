"""
Genesis Auditor - FastAPI Backend
Provides REST API and WebSocket endpoints for the React frontend
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import asyncio
import json
import sys
import os
from datetime import datetime
import uuid

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.orchestrator.genesis_orchestrator import GenesisOrchestrator
from src.memory.qdrant_memory import GenesisMemory

app = FastAPI(
    title="Genesis Auditor API",
    description="AI-Powered Security Auditing Platform",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://genesis-auditor.vercel.app",  # Production domain
        "https://genesis-auditor-bggj5hgzr-jayanth-muthinas-projects.vercel.app",
        "https://genesis-auditor-68vtpxy5j-jayanth-muthinas-projects.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active audits
active_audits: Dict[str, dict] = {}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, audit_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[audit_id] = websocket

    def disconnect(self, audit_id: str):
        if audit_id in self.active_connections:
            del self.active_connections[audit_id]

    async def send_update(self, audit_id: str, message: dict):
        if audit_id in self.active_connections:
            try:
                await self.active_connections[audit_id].send_json(message)
            except:
                self.disconnect(audit_id)

manager = ConnectionManager()

# Pydantic models
class AuditRequest(BaseModel):
    domain: str
    target_api_name: str
    target_api_url: Optional[str] = None
    description: Optional[str] = None

class AuditResponse(BaseModel):
    audit_id: str
    status: str
    message: str

class DomainInfo(BaseModel):
    id: str
    name: str
    icon: str
    description: str

# Routes
@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "Genesis Auditor API",
        "version": "1.0.0"
    }

@app.get("/api/domains", response_model=List[DomainInfo])
async def get_available_domains():
    """Get list of available security domains"""
    return [
        {
            "id": "hipaa",
            "name": "HIPAA Compliance",
            "icon": "🏥",
            "description": "Healthcare data protection and privacy"
        },
        {
            "id": "financial",
            "name": "Financial Fraud",
            "icon": "💰",
            "description": "Payment security and fraud prevention"
        },
        {
            "id": "gdpr",
            "name": "GDPR Compliance",
            "icon": "🇪🇺",
            "description": "EU data protection regulations"
        },
        {
            "id": "pci",
            "name": "PCI-DSS",
            "icon": "💳",
            "description": "Payment card industry security"
        },
        {
            "id": "api",
            "name": "API Security",
            "icon": "🔌",
            "description": "General API security testing"
        }
    ]

@app.post("/api/audit/start", response_model=AuditResponse)
async def start_audit(request: AuditRequest):
    """Start a new security audit"""
    try:
        # Generate unique audit ID
        audit_id = str(uuid.uuid4())[:8]

        print(f"\n{'='*70}")
        print(f"🚀 Starting audit: {audit_id}")
        print(f"   Domain: {request.domain}")
        print(f"   Target: {request.target_api_name}")
        print(f"{'='*70}\n")

        # Store audit metadata
        active_audits[audit_id] = {
            "id": audit_id,
            "domain": request.domain,
            "target": request.target_api_name,
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "results": None
        }

        # Run audit asynchronously in background
        # Use asyncio.create_task with proper reference to keep task alive
        task = asyncio.create_task(run_audit_async(audit_id, request))
        # Store task reference to prevent garbage collection
        active_audits[audit_id]["task"] = task

        print(f"✅ Background task created for audit {audit_id}")

        return {
            "audit_id": audit_id,
            "status": "started",
            "message": f"Audit {audit_id} initiated successfully"
        }

    except Exception as e:
        print(f"❌ Error starting audit: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_audit_async(audit_id: str, request: AuditRequest):
    """Run audit asynchronously with real-time updates"""
    print(f"\n{'='*70}")
    print(f"🎬 AUDIT ASYNC TASK STARTED for {audit_id}")
    print(f"{'='*70}\n")

    try:
        # Send memory query update
        await manager.send_update(audit_id, {
            "type": "phase_update",
            "phase": "memory_query",
            "message": "Querying memory for relevant past attacks..."
        })
        print(f"📤 Sent memory_query update for {audit_id}")

        await asyncio.sleep(1)  # Simulate processing

        # Send agent design update
        await manager.send_update(audit_id, {
            "type": "phase_update",
            "phase": "agent_design",
            "message": "Designing specialized agent swarm..."
        })

        await asyncio.sleep(1)

        # Initialize orchestrator with error handling
        try:
            print(f"🔧 Initializing orchestrator...")
            orchestrator = GenesisOrchestrator()
            print(f"✅ Orchestrator initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize orchestrator: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            await manager.send_update(audit_id, {
                "type": "audit_error",
                "error": error_msg
            })
            active_audits[audit_id]["status"] = "failed"
            active_audits[audit_id]["error"] = error_msg
            return

        # Send execution update
        await manager.send_update(audit_id, {
            "type": "phase_update",
            "phase": "execution",
            "message": "Deploying agents and executing attacks..."
        })

        # Map frontend domain IDs to actual domain names
        domain_map = {
            "hipaa": "HIPAA",
            "financial": "Financial Fraud",
            "gdpr": "GDPR Compliance",
            "pci": "PCI-DSS",
            "api": "API Security"
        }

        domain_name = domain_map.get(request.domain.lower(), request.domain)

        # Validate target URL if provided
        if request.target_api_url:
            if not (request.target_api_url.startswith("http://") or
                    request.target_api_url.startswith("https://")):
                error_msg = "Invalid target API URL. Must start with http:// or https://"
                await manager.send_update(audit_id, {
                    "type": "audit_error",
                    "error": error_msg
                })
                active_audits[audit_id]["status"] = "failed"
                active_audits[audit_id]["error"] = error_msg
                return

        # Run the actual audit with error handling
        try:
            print(f"🚀 Running audit: domain={domain_name}, target={request.target_api_name}")
            results = orchestrator.run_complete_audit(
                domain=domain_name,
                target_api_name=request.target_api_name,
                target_api_config={
                    'api_name': request.target_api_name,
                    'base_url': request.target_api_url or 'https://api.example.com'
                }
            )
            print(f"✅ Audit execution completed successfully")
            print(f"📊 Results: {results['statistics']}")
        except Exception as e:
            error_msg = f"Audit execution failed: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
            await manager.send_update(audit_id, {
                "type": "audit_error",
                "error": error_msg
            })
            active_audits[audit_id]["status"] = "failed"
            active_audits[audit_id]["error"] = error_msg
            return

        # Generate PDF report
        try:
            pdf_path = orchestrator.export_report_pdf(filename=f"genesis_audit_{audit_id}.pdf")
            print(f"📄 PDF report generated: {pdf_path}")
            results["report_files"] = {"pdf": pdf_path}
        except Exception as e:
            print(f"⚠️  Failed to generate PDF: {e}")
            # Continue even if PDF generation fails
            results["report_files"] = {}

        # Send completion update
        await manager.send_update(audit_id, {
            "type": "audit_complete",
            "compliance_score": results['statistics']['compliance_score'],
            "vulnerabilities_found": results['statistics']['vulnerabilities_found'],
            "critical_findings": results['statistics']['critical_findings']
        })

        # Update audit status
        active_audits[audit_id].update({
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "results": results
        })

        print(f"✅ Audit {audit_id} completed successfully")

    except Exception as e:
        print(f"❌ Unexpected error during audit {audit_id}: {e}")
        import traceback
        traceback.print_exc()

        # Send error update
        await manager.send_update(audit_id, {
            "type": "audit_error",
            "error": f"Unexpected error: {str(e)}"
        })

        active_audits[audit_id]["status"] = "failed"
        active_audits[audit_id]["error"] = str(e)

@app.get("/api/audit/{audit_id}")
async def get_audit_status(audit_id: str):
    """Get the status and results of an audit"""
    if audit_id not in active_audits:
        raise HTTPException(status_code=404, detail="Audit not found")

    audit = active_audits[audit_id]

    # If completed, include full results
    if audit["status"] == "completed" and audit.get("results"):
        return {
            "audit_id": audit_id,
            "status": audit["status"],
            "domain": audit["domain"],
            "target": audit["target"],
            "started_at": audit["started_at"],
            "completed_at": audit.get("completed_at"),
            "statistics": audit["results"]["statistics"],
            "analysis": audit["results"]["analysis"],
            "vulnerabilities": [
                v for v in audit["results"]["attack_results"]
                if v.get("result") == "VULNERABLE"
            ][:10]  # Return top 10 vulnerabilities
        }

    # Otherwise just return status
    return {
        "audit_id": audit_id,
        "status": audit["status"],
        "domain": audit["domain"],
        "target": audit["target"],
        "started_at": audit["started_at"]
    }

@app.get("/api/audits/recent")
async def get_recent_audits(limit: int = 10):
    """Get recent audit history"""
    audits = sorted(
        active_audits.values(),
        key=lambda x: x.get("started_at", ""),
        reverse=True
    )[:limit]

    return {
        "audits": [
            {
                "audit_id": audit["id"],
                "domain": audit["domain"],
                "target": audit["target"],
                "status": audit["status"],
                "started_at": audit["started_at"],
                "compliance_score": audit["results"]["statistics"]["compliance_score"]
                    if audit.get("results") else None
            }
            for audit in audits
        ]
    }

@app.websocket("/ws/audit/{audit_id}")
async def websocket_endpoint(websocket: WebSocket, audit_id: str):
    """WebSocket endpoint for real-time audit updates"""
    await manager.connect(audit_id, websocket)
    print(f"🔌 WebSocket connected for audit: {audit_id}")

    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(audit_id)
        print(f"🔌 WebSocket disconnected for audit: {audit_id}")

@app.get("/api/memory/stats")
async def get_memory_stats():
    """Get memory system statistics"""
    try:
        memory = GenesisMemory()
        stats = memory.get_memory_stats()

        return {
            "total_patterns": stats["total_patterns"],
            "collection_name": stats["collection_name"],
            "status": "operational"
        }
    except Exception as e:
        return {
            "total_patterns": 0,
            "status": "unavailable",
            "error": str(e)
        }

@app.get("/api/memory/patterns/{domain}")
async def get_memory_patterns(domain: str, limit: int = 10):
    """Get stored attack patterns for a domain"""
    try:
        memory = GenesisMemory()

        # Map frontend domain IDs
        domain_map = {
            "hipaa": "HIPAA",
            "financial": "Financial Fraud",
            "gdpr": "GDPR Compliance",
            "pci": "PCI-DSS",
            "api": "API Security"
        }

        domain_name = domain_map.get(domain.lower(), domain)

        patterns = memory.retrieve_relevant_attacks(
            domain=domain_name,
            top_k=limit
        )

        return {
            "domain": domain_name,
            "patterns": patterns
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audit/{audit_id}/download-pdf")
async def download_pdf(audit_id: str):
    """Download the PDF report for a completed audit"""
    if audit_id not in active_audits:
        raise HTTPException(status_code=404, detail="Audit not found")

    audit = active_audits[audit_id]

    if audit["status"] != "completed":
        raise HTTPException(status_code=400, detail="Audit not yet completed")

    # Get the PDF file path from results
    pdf_path = audit["results"].get("report_files", {}).get("pdf")

    if not pdf_path or not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF report not found")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"genesis_audit_{audit_id}.pdf"
    )

if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*70)
    print("🚀 Starting Genesis Auditor API Server")
    print("="*70)
    print("📍 API: http://localhost:8001")
    print("📚 Docs: http://localhost:8001/docs")
    print("🔌 WebSocket: ws://localhost:8001/ws/audit/{audit_id}")
    print("="*70 + "\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
