# Opus Workflow Integration Guide

## Overview

Genesis Auditor now supports webhook-based workflow automation, allowing you to integrate with platforms like **Opus**, **Zapier**, **Make.com**, **n8n**, and custom automation systems.

## Supported Events

Genesis Auditor triggers webhooks for the following events:

| Event Type | Triggered When | Payload Includes |
|-----------|---------------|-----------------|
| `audit.started` | Audit begins | domain, target, timestamp |
| `audit.completed` | Audit finishes successfully | compliance_score, risk_level, vulnerabilities_found, duration |
| `audit.failed` | Audit fails | error message |
| `vulnerability.critical` | Critical vulnerabilities found | critical_count, vulnerability list |
| `vulnerability.high` | High severity vulnerabilities found | high_count, vulnerability list |

## Quick Start

### 1. Register a Webhook

**API Endpoint:** `POST /api/webhooks/register`

**Request Body:**
```json
{
  "event_type": "audit.completed",
  "webhook_url": "https://your-opus-workflow.com/webhook/xyz123",
  "secret": "optional_secret_for_hmac_verification",
  "description": "Send to Opus workflow for compliance reporting"
}
```

**Example with curl:**
```bash
curl -X POST https://genesis-auditor-production-0ef5.up.railway.app/api/webhooks/register \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "audit.completed",
    "webhook_url": "https://hooks.opus.com/webhooks/abc123",
    "description": "Opus compliance workflow"
  }'
```

### 2. Receive Webhook Payload

When the event triggers, your webhook URL will receive a POST request:

```json
{
  "event": "audit.completed",
  "timestamp": "2025-01-19T12:34:56.789Z",
  "source": "genesis-auditor",
  "data": {
    "domain": "HIPAA",
    "target": "Healthcare Patient Portal API",
    "compliance_score": 78,
    "risk_level": "MEDIUM",
    "vulnerabilities_found": 5,
    "duration_seconds": 145.3
  }
}
```

### 3. Verify Webhook Signature (Optional)

If you provided a `secret`, Genesis Auditor includes an HMAC-SHA256 signature in the `X-Genesis-Signature` header:

**Python verification example:**
```python
import hmac
import hashlib
import json

def verify_webhook(request_body, signature, secret):
    payload_str = json.dumps(request_body, sort_keys=True)
    expected_sig = hmac.new(
        secret.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_sig, signature)
```

## Integration Examples

### Opus Workflow Platform

1. **Get your Opus webhook URL** from your Opus dashboard
2. **Register the webhook** using the Genesis Auditor API
3. **Configure your Opus workflow** to handle the incoming data

**Example Opus Workflow:**
```
Genesis Auditor Webhook Trigger
  ↓
Filter: compliance_score < 70
  ↓
Send Slack Alert to #security-team
  ↓
Create Jira Ticket with vulnerability details
  ↓
Send Email Report to CISO
```

### Zapier Integration

1. **Create a Zap** with a "Webhooks by Zapier" trigger
2. **Copy the webhook URL**
3. **Register it** with Genesis Auditor:
   ```bash
   curl -X POST https://genesis-auditor-production-0ef5.up.railway.app/api/webhooks/register \
     -H "Content-Type: application/json" \
     -d '{
       "event_type": "vulnerability.critical",
       "webhook_url": "https://hooks.zapier.com/hooks/catch/12345/abcdef/"
     }'
   ```
4. **Continue your Zap** with actions like:
   - Send to Slack
   - Create Google Sheet row
   - Email notification
   - Create Linear/Jira issue

### Make.com Integration

1. **Create a new scenario** with a Webhook module
2. **Copy the webhook URL**
3. **Register with Genesis Auditor**
4. **Build your automation flow**:
   - Parse webhook data
   - Route based on risk_level
   - Trigger notifications
   - Update dashboards

## Use Cases

### 1. Automated Compliance Reporting
**Trigger:** `audit.completed`
**Workflow:**
- Store results in Google Sheets
- Generate PDF report
- Email to compliance team
- Update compliance dashboard

### 2. Critical Vulnerability Alerts
**Trigger:** `vulnerability.critical`
**Workflow:**
- Immediate Slack/Teams notification
- Create P0 ticket in Jira
- Page on-call engineer
- Start incident response workflow

### 3. Scheduled Audit Pipeline
**External trigger:** Cron job or scheduler
**Flow:**
1. Trigger audit via `/api/audit/start`
2. Genesis Auditor runs audit
3. Webhook sends results to Opus
4. Opus workflow processes and distributes report

### 4. Multi-System Integration
**Trigger:** `audit.completed`
**Opus Workflow:**
- Post to Slack #security channel
- Update Notion database
- Create Linear tickets for vulnerabilities
- Send email digest to stakeholders
- Update Grafana/Datadog metrics

## API Reference

### Register Webhook
```http
POST /api/webhooks/register
Content-Type: application/json

{
  "event_type": "audit.completed",
  "webhook_url": "https://example.com/webhook",
  "secret": "optional_hmac_secret",
  "description": "Optional description"
}
```

### List Available Events
```http
GET /api/webhooks/events
```

Returns all available event types with example payloads.

### Get Webhook Statistics
```http
GET /api/webhooks/stats
```

Returns count of registered webhooks by event type.

## Security Best Practices

1. **Use HTTPS**: Always use HTTPS webhooks in production
2. **Verify Signatures**: Use the `secret` parameter and verify HMAC signatures
3. **Rate Limiting**: Implement rate limiting on your webhook endpoint
4. **Timeout Handling**: Genesis Auditor times out after 10 seconds
5. **Idempotency**: Handle duplicate webhook deliveries gracefully

## Troubleshooting

### Webhook Not Firing
- Check that you registered the correct event type
- Verify your webhook URL is accessible
- Check server logs for delivery errors

### Invalid Signature
- Ensure your secret matches exactly
- Verify you're sorting JSON keys when computing HMAC
- Check that you're using SHA256 algorithm

### Timeout Errors
- Your webhook endpoint must respond within 10 seconds
- Use async processing for long-running tasks
- Return 200 OK immediately, process in background

## Support

For issues or questions:
- Check API docs: `https://your-api-url.com/docs`
- GitHub Issues: https://github.com/jayzz999/genesis-auditor/issues
- Email: support@genesis-auditor.com

## Next Steps

1. Register your first webhook
2. Test with a simple audit
3. Build your automation workflow
4. Monitor webhook delivery success

Happy Automating! 🚀
