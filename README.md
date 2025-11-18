# 🔮 Genesis Auditor

**AI-Powered Security Auditing Platform with Memory-Augmented Agent Swarms**

> An autonomous security auditing system that uses Gemini 2.5 to design specialized red-team agent swarms, execute real attacks, learn from experience via vector memory, and deliver professional reports through a beautiful Next.js interface.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5-blue.svg)](https://ai.google.dev/)
[![Qdrant](https://img.shields.io/badge/Memory-Qdrant-red.svg)](https://qdrant.tech/)
[![Deploy](https://img.shields.io/badge/Deploy-Free-green.svg)](DEPLOYMENT_GUIDE.md)

---

## 🎯 What Makes This Special

**This is a production-ready, full-stack security platform built with:**

✅ **Real AI Integration** - **Google Gemini 2.5 Flash** designs custom attack vectors with advanced reasoning for each audit
✅ **Vector Memory System** - **Qdrant** stores successful attacks for continuous learning and semantic retrieval
✅ **Real HTTP Testing** - Actually executes attacks against target APIs (not simulated!)
✅ **Professional UI** - Beautiful Next.js 14 dashboard with real-time WebSocket updates
✅ **Executive Reports** - PDF generation with charts and compliance scoring
✅ **Complete Features** - 7 pages, 11 API endpoints, 5 compliance domains
✅ **Production Deployment** - Ready to deploy on Vercel + Railway (100% free tier)

**Tech Stack:** Next.js 14 · FastAPI · **Google Gemini 2.5** · **Qdrant** · TypeScript · Python · WebSockets · ReportLab

## 🌟 Overview

Genesis Auditor is a cutting-edge security testing platform that showcases the power of **Google Gemini** and **Qdrant**:
- **AI-Powered Agent Design** - **Google Gemini 2.5 Flash** autonomously designs sophisticated attack strategies with multi-agent personas
- **Memory Augmentation** - **Qdrant** vector database stores and retrieves successful attacks via semantic search
- **Self-Improvement** - Learns from every audit to enhance future tests using vector similarity
- **Professional Reporting** - Executive-grade PDF reports with visualizations

## ✨ Key Features

### 🤖 AI-Powered Agent Swarms (Google Gemini)
- **Google Gemini 2.5** autonomously designs specialized red-team agents with unique personas
- Advanced reasoning creates attack strategies tailored to each domain (HIPAA, Financial Fraud, OWASP Top 10)
- Dynamic agent composition based on target API characteristics
- Gemini demonstrates intelligence through tactical coordination and attack chain planning

### 🧠 Memory-Augmented Learning (Qdrant)
- **Qdrant** vector database stores successful attack patterns as high-dimensional embeddings
- Semantic search retrieves relevant past attacks using vector similarity
- Continuous learning from audit history - every successful attack improves future audits
- Domain-specific knowledge accumulation with intelligent pattern matching

### ⚔️ Real Attack Execution
- Makes actual HTTP requests to target APIs
- Analyzes responses for vulnerability indicators (SQL errors, auth bypasses, etc.)
- Falls back to intelligent simulation for demo/safety
- Evidence collection and impact assessment
- Compliance scoring (0-100 scale)

### 📊 Professional PDF Reports
- Executive-grade formatting and design
- Security compliance radar charts
- Vulnerability severity pie charts
- Color-coded findings and recommendations
- AI-generated executive summaries

## 🚀 Quick Start

### Option 1: Run Locally (Full Stack)

```bash
# 1. Clone and setup
git clone <your-repo>
cd genesis-auditor
./setup.sh

# 2. Configure environment
cp .env.example .env
# Add your API keys to .env

# 3. Start both frontend and backend
./start.sh

# 4. Open browser
# Frontend: http://localhost:3000
# Backend:  http://localhost:8001/docs
```

### Option 2: Deploy to Production (100% Free!)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete instructions.

**Stack:**
- Frontend: Vercel (Free)
- Backend: Railway (Free $5/month credit)
- Database: Qdrant Cloud (Free 1GB)

### Option 3: Python API Only

```python
from src.orchestrator.genesis_orchestrator import GenesisOrchestrator

# Initialize
orchestrator = GenesisOrchestrator()

# Run audit
results = orchestrator.run_complete_audit(
    domain="HIPAA",
    target_api_name="HealthCare API v2.0"
)

# Export reports (JSON + PDF)
json_file = orchestrator.export_report_json()
pdf_file = orchestrator.export_report_pdf()
```

## 📖 Documentation

### Getting Started
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deploy for free in 10 minutes
- **[Quick Start Guide](QUICK_START.md)** - Run locally in 5 minutes
- **[Frontend README](frontend/README.md)** - Next.js app documentation

### Architecture Guides
- **[Step 1: Memory System](STEP1_COMPLETE.md)** - Vector database implementation
- **[Step 2: Genesis Agent](STEP2_COMPLETE.md)** - AI agent design system
- **[Step 3: Orchestration](STEP3_COMPLETE.md)** - End-to-end workflow
- **[Step 4: PDF Reports](STEP4_COMPLETE.md)** - Professional report generation

## 🏗️ Architecture

```
User Input → Genesis Orchestrator → Genesis Agent (AI Design)
                    ↓                      ↓
            Attack Executor ← Memory System (Qdrant)
                    ↓                      ↓
            Report Generator → PDF + JSON Reports
```

## 🎯 What Makes This Special?

Unlike traditional security tools, Genesis Auditor showcases cutting-edge AI:

1. **AI Designs AI** - **Google Gemini** demonstrates advanced reasoning by designing custom agent swarms with tactical personas
2. **Learns from History** - **Qdrant** vector memory stores successful attacks for semantic retrieval
3. **Self-Improves** - Every audit makes the next one smarter through vector similarity learning
4. **Professional Reports** - Executive-ready PDF reports with charts
5. **Real Intelligence** - Not just templates - Gemini creates unique, context-aware attack strategies

## 📊 Sample Output

```
🎯 Domain: HIPAA
🎯 Target: HealthCare Management API v2.1
⏱️  Duration: 67.3s

📈 Compliance Score: 0/100
🚨 Risk Level: CRITICAL

📊 Attack Statistics:
   Total Attacks: 15
   Vulnerabilities Found: 8
   Critical Issues: 3
   High Issues: 4
```

## 🧪 Components

1. **Memory System** - Vector database for attack patterns
2. **Genesis Agent** - AI-powered swarm designer
3. **Attack Executor** - Vulnerability testing engine
4. **Orchestrator** - Workflow coordinator
5. **Report Generator** - Professional PDF creation

## 🛠️ Tech Stack

### Backend
- **AI**: **Google Gemini 2.5 Flash** (Advanced reasoning and agent design)
- **Vector DB**: **Qdrant** (Semantic memory and attack pattern storage)
- **API**: FastAPI + WebSocket
- **Embeddings**: OpenAI / Sentence Transformers
- **PDF**: ReportLab + Matplotlib
- **Language**: Python 3.8+

### Frontend
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS
- **Components**: Shadcn UI
- **Language**: TypeScript
- **Real-time**: WebSocket for live updates

## 📈 Performance

| Metric | Value |
|--------|-------|
| Audit Duration | 40-70 seconds |
| Attacks Per Audit | 9-15 vectors |
| PDF Generation | 2-3 seconds |
| PDF Size | ~140KB with charts |

## 🎓 Supported Domains

- HIPAA Compliance
- Financial Fraud
- OWASP API Security Top 10
- Custom Security Domains

## 🧪 Testing

```bash
# Test components
python src/memory/qdrant_memory.py
python src/agents/genesis_agent.py
python src/orchestrator/genesis_orchestrator.py
python src/utils/report_generator.py

# Verify installation
python verify_step4_complete.py
```

---

**Built for hackathons and security professionals**

*Genesis Auditor - Where AI Meets Security*
