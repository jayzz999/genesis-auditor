# Opus Job Operator API Integration Guide

## Overview

Genesis Auditor integrates directly with the **Opus Job Operator API** to trigger workflow automation when security audits complete. This provides seamless automation for compliance reporting, vulnerability alerts, and multi-system integrations.

## Architecture

```
Genesis Auditor → Opus Job Operator API → Opus Workflow Execution
     ↓
  Audit Complete
     ↓
  POST /jobs/initiate
     ↓
  Opus Workflow Runs
     ↓
  Actions (Slack, Jira, Email, etc.)
```

## Setup

### 1. Get Your Opus Credentials

1. Log into your Opus dashboard
2. Navigate to **Settings → API Keys**
3. Generate a new API key
4. Copy your **Workflow ID** from your workflow settings

### 2. Configure Environment Variables

Add these to your Railway/environment:

```bash
OPUS_API_KEY=your_opus_api_key_here
OPUS_WORKFLOW_ID=wTriWWYYLBQC7k1a  # Your workflow ID
OPUS_BASE_URL=https://api.opus.com  # Optional, uses default if not set
```

### 3. Deploy

Push changes to Railway:
```bash
git push
```

Railway will automatically redeploy with Opus integration enabled.

## How It Works

### Automatic Triggers

Genesis Auditor automatically triggers Opus workflows when:

**1. Audit Completes Successfully**
```python
# Sends to Opus Job Operator API
POST /jobs/initiate
{
  "workflow_id": "wTriWWYYLBQC7k1a",
  "input": {
    "event_type": "audit_completed",
    "audit_data": {
      "domain": "HIPAA",
      "target_api": "Healthcare API",
      "compliance_score": 78,
      "risk_level": "MEDIUM",
      "vulnerabilities_found": 5,
      "duration_seconds": 145.3,
      "critical_vulnerabilities": [],
      "timestamp": "2025-01-19T12:34:56Z"
    }
  },
  "metadata": {
    "event": "audit_completed",
    "domain": "HIPAA",
    "target": "Healthcare API"
  }
}
```

**2. Critical Vulnerabilities Found**
```python
# Separate urgent alert job
POST /jobs/initiate
{
  "workflow_id": "wTriWWYYLBQC7k1a",
  "input": {
    "event_type": "critical_vulnerability_alert",
    "alert_data": {
      "domain": "HIPAA",
      "target_api": "Healthcare API",
      "critical_count": 2,
      "vulnerabilities": [
        {
          "name": "SQL Injection",
          "description": "...",
          "severity": "CRITICAL"
        }
      ],
      "timestamp": "2025-01-19T12:34:56Z",
      "requires_immediate_action": true
    }
  },
  "metadata": {
    "event": "critical_alert",
    "priority": "P0",
    "domain": "HIPAA"
  }
}
```

### Opus Workflow Input Schema

Your Opus workflow should accept inputs matching this schema:

```json
{
  "event_type": "string",  // "audit_completed" or "critical_vulnerability_alert"
  "audit_data": {          // For audit_completed events
    "domain": "string",
    "target_api": "string",
    "compliance_score": "number",
    "risk_level": "string",
    "vulnerabilities_found": "number",
    "duration_seconds": "number",
    "critical_vulnerabilities": "array",
    "timestamp": "string"
  },
  "alert_data": {          // For critical_vulnerability_alert events
    "domain": "string",
    "target_api": "string",
    "critical_count": "number",
    "vulnerabilities": "array",
    "timestamp": "string",
    "requires_immediate_action": "boolean"
  }
}
```

## Example Opus Workflows

### 1. Compliance Reporting Workflow

**Trigger:** `audit_completed` event

**Workflow Steps:**
1. **Branch on compliance_score**
   - If < 70: Send urgent Slack alert
   - If 70-85: Send standard notification
   - If > 85: Send success message

2. **Create Jira Ticket**
   - Title: "Security Audit: {domain} - {target_api}"
   - Description: Include compliance score, vulnerabilities
   - Priority: Based on risk_level

3. **Update Google Sheet**
   - Add row with audit results
   - Track historical trends

4. **Email Report**
   - Send to compliance team
   - Attach PDF report link

### 2. Critical Vulnerability Alert Workflow

**Trigger:** `critical_vulnerability_alert` event

**Workflow Steps:**
1. **Immediate Slack Alert**
   - Channel: #security-incidents
   - Mention: @security-team
   - Priority: P0

2. **Page On-Call Engineer**
   - Use PagerDuty integration
   - Severity: High

3. **Create P0 Jira Ticket**
   - Auto-assign to security lead
   - Include vulnerability details

4. **Start Incident Response**
   - Trigger incident response workflow
   - Log to incident management system

### 3. Multi-Domain Compliance Dashboard

**Trigger:** All `audit_completed` events

**Workflow Steps:**
1. **Store in Database**
   - PostgreSQL/MongoDB
   - Track all audit history

2. **Update Grafana Dashboard**
   - Push metrics via API
   - Real-time compliance scores

3. **Generate Weekly Digest**
   - Aggregate all audits
   - Email to stakeholders every Friday

## API Reference

### OpusClient Methods

```python
from integrations.opus_client import get_opus_client

opus = get_opus_client()

# Trigger audit completed workflow
response = opus.trigger_audit_completed_workflow(
    domain="HIPAA",
    target_api_name="Healthcare API",
    compliance_score=78,
    risk_level="MEDIUM",
    vulnerabilities_found=5,
    duration_seconds=145.3,
    critical_vulnerabilities=[]
)
# Returns: {"job_id": "abc123", "status": "initiated"}

# Trigger critical alert
alert = opus.trigger_critical_vulnerability_workflow(
    domain="HIPAA",
    target_api_name="Healthcare API",
    critical_vulnerabilities=[...]
)

# Check job status
status = opus.get_job_status(job_id="abc123")
# Returns: {"job_id": "abc123", "status": "completed", "result": {...}}

# Get workflow schema
schema = opus.get_workflow_schema(workflow_id="wTriWWYYLBQC7k1a")
```

## Testing

### 1. Verify Configuration

```bash
# Check if Opus is enabled
curl http://localhost:8001/health

# Look for: "✅ Opus integration enabled" in logs
```

### 2. Run Test Audit

```bash
curl -X POST http://localhost:8001/api/audit/start \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "hipaa",
    "target_api_name": "Test API",
    "target_api_url": "https://jsonplaceholder.typicode.com"
  }'
```

### 3. Check Opus Dashboard

- Go to Opus dashboard
- Navigate to **Jobs** tab
- Look for newly initiated job
- Verify input data matches audit results

## Troubleshooting

### Opus Integration Not Working

**Check 1: API Key Configured**
```bash
echo $OPUS_API_KEY
# Should output your API key
```

**Check 2: Workflow ID Correct**
```bash
echo $OPUS_WORKFLOW_ID
# Should output: wTriWWYYLBQC7k1a or your workflow ID
```

**Check 3: Check Logs**
```bash
# Look for these messages in Railway logs:
# "✅ Opus integration enabled"
# "🎯 Triggering Opus workflow..."
# "✅ Opus job initiated: {job_id}"
```

### Job Initiation Fails

**Error:** `401 Unauthorized`
- **Fix:** Check OPUS_API_KEY is correct
- Regenerate API key in Opus dashboard if needed

**Error:** `404 Not Found`
- **Fix:** Verify OPUS_WORKFLOW_ID matches your workflow
- Check workflow is not archived/deleted

**Error:** `400 Bad Request`
- **Fix:** Check workflow input schema matches
- Verify all required fields are provided

### Workflow Not Executing

**Check 1: Workflow Status**
- Ensure workflow is **Active** (not Paused)
- Check workflow has valid configuration

**Check 2: Input Validation**
- Verify input matches workflow schema
- Check for required fields

**Check 3: Execution Logs**
- View job execution logs in Opus dashboard
- Look for errors in individual modules

## Advanced Usage

### Custom Workflow Triggers

You can trigger Opus workflows programmatically:

```python
from integrations.opus_client import get_opus_client

opus = get_opus_client()

# Custom trigger
response = opus.initiate_job(
    input_data={
        "custom_event": "manual_review_needed",
        "api_name": "My API",
        "reviewer": "john@company.com"
    },
    workflow_id="your_custom_workflow_id",
    job_metadata={
        "source": "manual",
        "priority": "high"
    }
)
```

### Multiple Workflows

Configure different workflows for different events:

```bash
# Environment variables
OPUS_WORKFLOW_ID_AUDIT=wTriWWYYLBQC7k1a
OPUS_WORKFLOW_ID_ALERT=xYz123AbC456
OPUS_WORKFLOW_ID_REPORT=mNoPqR789
```

```python
# Trigger specific workflow
opus.initiate_job(
    input_data={...},
    workflow_id=os.getenv('OPUS_WORKFLOW_ID_ALERT')
)
```

## Security Best Practices

1. **Protect API Keys**
   - Never commit API keys to git
   - Use environment variables
   - Rotate keys periodically

2. **Validate Input**
   - Genesis Auditor validates all data before sending
   - Opus workflow should also validate inputs

3. **Monitor Job Status**
   - Set up alerts for failed jobs
   - Review job logs regularly

4. **Rate Limiting**
   - Opus API has rate limits
   - Genesis Auditor handles this gracefully

## Support

- **Opus Documentation:** https://developer.opus.com
- **Genesis Issues:** https://github.com/jayzz999/genesis-auditor/issues
- **API Docs:** https://genesis-auditor-production-0ef5.up.railway.app/docs

## Next Steps

1. Set up your Opus workflow
2. Configure environment variables
3. Run a test audit
4. Monitor Opus dashboard for jobs
5. Customize workflows for your needs

Happy Automating! 🚀
