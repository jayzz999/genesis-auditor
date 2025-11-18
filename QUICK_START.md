# 🚀 Genesis Auditor - Quick Start Guide

## Overview

Genesis Auditor is an AI-powered security auditing system that autonomously designs and executes API security tests using memory-augmented AI agents.

## Quick Start

### 1. Run a Complete Audit

```bash
python src/orchestrator/genesis_orchestrator.py
```

This runs a demo HIPAA audit and generates a complete report.

### 2. Custom Audit via Python

```python
from src.orchestrator.genesis_orchestrator import GenesisOrchestrator

# Initialize
orchestrator = GenesisOrchestrator()

# Run audit
results = orchestrator.run_complete_audit(
    domain="Financial Fraud",  # or "HIPAA", "OWASP API Security Top 10", etc.
    target_api_name="Your API Name",
    target_api_config={
        'api_name': 'Your API Name',
        'base_url': 'https://api.example.com',
        'version': '1.0'
    }
)

# Export reports (both JSON and PDF)
json_file = orchestrator.export_report_json()
pdf_file = orchestrator.export_report_pdf()
print(f"JSON Report: {json_file}")
print(f"PDF Report: {pdf_file}")
```

## Components

### 1. Attack Executor
Tests attack vectors against APIs and generates findings.

```bash
python src/orchestrator/attack_executor.py
```

### 2. Genesis Agent
Designs specialized agent swarms using AI and past attack patterns.

```bash
python src/agents/genesis_agent.py
```

### 3. Memory System
Stores and retrieves successful attack patterns.

```bash
python src/memory/qdrant_memory.py
```

### 4. PDF Report Generator
Creates professional, executive-grade PDF reports with visualizations.

```bash
python src/utils/report_generator.py
```

## Output

Each audit generates **two reports** - JSON and PDF:

### JSON Report
Contains raw data including:

- **Audit Metadata**: Domain, target, timestamp, duration
- **Statistics**: Attack counts, vulnerabilities, compliance score
- **Analysis**: Risk level, critical issues, recommendations
- **Agent Plan**: The designed swarm architecture
- **Attack Results**: Detailed findings for each attack
- **Recommendations**: Prioritized remediation steps

### PDF Report
Professional, executive-grade report with:

- **Cover Page**: Prominent compliance score, risk level, audit metadata
- **Executive Summary**: AI-generated insights and key findings table
- **Compliance Scorecard**: Radar chart (5 dimensions) + pie chart (severity distribution)
- **Detailed Findings**: Color-coded vulnerabilities with evidence and recommendations
- **Remediation Roadmap**: Prioritized action items
- **Professional Design**: Color-coded severity, tables, charts (~140KB)

## Example Output

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

## Supported Security Domains

- **HIPAA** - Healthcare data protection
- **Financial Fraud** - Banking and transaction security
- **OWASP API Security Top 10** - General API security
- **Custom Domains** - Specify any security domain

## Testing

```bash
# Test attack executor
python src/orchestrator/attack_executor.py

# Test full orchestrator
python src/orchestrator/genesis_orchestrator.py

# Verify all components
python verify_step3_success.py
```

## Key Features

✅ **AI-Powered**: Uses Gemini 2.5 Flash for intelligent agent design
✅ **Memory-Augmented**: Learns from past successful attacks
✅ **Self-Improving**: Stores findings to enhance future audits
✅ **Professional Reports**: Enterprise-grade JSON audit reports
✅ **Domain-Specific**: Specialized expertise across security domains
✅ **Compliance Scoring**: 0-100 weighted scoring system

## Architecture

```
User Input
    ↓
Genesis Orchestrator
    ↓
┌──────────────────┬──────────────────┬──────────────────┐
│  Genesis Agent   │  Attack Executor │  Memory System   │
│  (AI Design)     │  (Execution)     │  (Learning)      │
└──────────────────┴──────────────────┴──────────────────┘
    ↓
Audit Report (JSON)
```

## Requirements

- Python 3.8+
- Gemini API key (in `.env`)
- Qdrant (runs locally)
- Required packages: `qdrant-client`, `google-generativeai`, `sentence-transformers`

## Environment Setup

Create `.env` file:
```bash
GEMINI_API_KEY=your_key_here
QDRANT_URL=http://localhost:6333
```

## Generated Files

- `genesis_audit_*.json` - Audit reports
- `qdrant_data/` - Memory database
- Logs and attack results

## Support

For issues or questions, refer to:
- [STEP1_COMPLETE.md](STEP1_COMPLETE.md) - Memory system details
- [STEP2_COMPLETE.md](STEP2_COMPLETE.md) - Genesis Agent details
- [STEP3_COMPLETE.md](STEP3_COMPLETE.md) - Orchestrator details
