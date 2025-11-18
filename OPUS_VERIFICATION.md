# Opus Integration Verification Guide

## Issue Summary

You reported: "i coudnt see any results" for Opus integration.

**Root Cause Analysis:**
- Opus integration code is correctly implemented ✅
- Code is deployed to Railway ✅
- Environment variables are configured in Railway ✅
- BUT: Need to verify if workflows are actually triggering

## Quick Verification Steps

### Step 1: Check Railway Logs for Opus Messages

1. Go to your Railway dashboard
2. Click on your `genesis-auditor` backend service
3. Go to the **Deployments** tab
4. Click on the latest deployment
5. Look for these log messages:

**Expected on startup:**
```
🎯 Opus client initializing...
✅ Opus integration enabled
```

**If you see this instead, API key is missing:**
```
🎯 Opus client initializing...
ℹ️  Opus integration disabled (set OPUS_API_KEY to enable)
```

**Expected after an audit completes:**
```
🎯 Triggering Opus workflow...
📤 Step 1: Initiating Opus job for workflow: wTriWWYYLBQC7k1a
✅ Job initiated with execution ID: abc123xyz
📤 Step 2: Executing Opus job: abc123xyz
✅ Opus job executed successfully
✅ Opus job initiated: abc123xyz
```

**If critical vulnerabilities found:**
```
🚨 Triggering Opus critical vulnerability alert...
📤 Step 1: Initiating Opus job for workflow: wTriWWYYLBQC7k1a
✅ Job initiated with execution ID: xyz789abc
📤 Step 2: Executing Opus job: xyz789abc
✅ Opus job executed successfully
✅ Opus alert job initiated: xyz789abc
```

**If Opus fails (wrong API key, network error, etc.):**
```
🎯 Triggering Opus workflow...
📤 Step 1: Initiating Opus job...
❌ Failed to initiate Opus job: [error message]
⚠️  Opus workflow trigger failed: [error message]
```

### Step 2: Verify Environment Variables in Railway

1. Go to Railway dashboard → Your project → Backend service
2. Click **Variables** tab
3. Verify these are set:

```bash
OPUS_API_KEY=your_actual_api_key_here
OPUS_WORKFLOW_ID=wTriWWYYLBQC7k1a
OPUS_BASE_URL=https://operator.opus.com  # Optional, defaults to this
```

**IMPORTANT:** If you just added/changed these, you need to:
- Click **Redeploy** in Railway
- Wait for deployment to complete
- Then run a new audit

### Step 3: Check Opus Dashboard

1. Go to https://app.opus.com (or your Opus dashboard URL)
2. Navigate to **Jobs** or **Executions** tab
3. Look for jobs with title: **"Genesis Audit - audit_completed"** or **"Genesis Audit - critical_vulnerability_alert"**
4. Check job execution status and payload data

**What you should see in Opus:**
- Job title: "Genesis Audit - audit_completed"
- Input data includes:
  - `event_type`: "audit_completed"
  - `audit_data`: compliance_score, risk_level, vulnerabilities_found, etc.

### Step 4: Run a Test Audit and Monitor

1. Go to https://genesis-auditor.vercel.app
2. Start a new audit (any domain, any API)
3. Keep Railway logs open in another tab
4. Watch for Opus-related messages as audit completes
5. Check Opus dashboard for new job execution

## Common Issues and Solutions

### Issue 1: "Opus integration disabled" in logs

**Problem:** OPUS_API_KEY not set in Railway environment variables

**Solution:**
1. Go to Railway → Variables
2. Add `OPUS_API_KEY` with your API key
3. Click **Redeploy**
4. Verify logs now show "✅ Opus integration enabled"

### Issue 2: "401 Unauthorized" or "403 Forbidden"

**Problem:** Invalid API key

**Solution:**
1. Go to Opus dashboard → Settings → API Keys
2. Generate a new API key
3. Update `OPUS_API_KEY` in Railway
4. Redeploy Railway service

### Issue 3: "404 Not Found" for workflow

**Problem:** Wrong workflow ID

**Solution:**
1. Go to Opus dashboard → Your workflow
2. Copy the correct Workflow ID
3. Update `OPUS_WORKFLOW_ID` in Railway
4. Redeploy

### Issue 4: No logs about Opus at all

**Problem:** Railway hasn't redeployed with latest code

**Solution:**
1. Railway should auto-deploy when you push to GitHub
2. If not, manually click **Redeploy** in Railway dashboard
3. Verify deployment timestamp is recent

### Issue 5: "Opus job initiated" in logs but nothing in Opus dashboard

**Problem:** Could be:
- Workflow is paused/inactive in Opus
- Network connectivity issue
- Opus API experiencing issues

**Solution:**
1. Check workflow is **Active** in Opus dashboard
2. Check Opus status page for outages
3. Try triggering workflow manually in Opus to verify it works

## Testing Locally (Optional)

If you want to test Opus integration on your local machine:

1. **Set environment variables in your terminal:**
   ```bash
   export OPUS_API_KEY=your_api_key_here
   export OPUS_WORKFLOW_ID=wTriWWYYLBQC7k1a
   ```

2. **Run the test script:**
   ```bash
   cd backend
   python test_opus.py
   ```

3. **Expected output if working:**
   ```
   ============================================================
   Testing Opus Integration
   ============================================================

   📋 Configuration:
      API Key: ✅ Set
      Workflow ID: wTriWWYYLBQC7k1a
      Base URL: https://operator.opus.com

   🔄 Initializing Opus client...
   ✅ Opus client initialized

   🧪 Testing audit completed workflow trigger...
   📤 Step 1: Initiating Opus job...
   ✅ Job initiated with execution ID: abc123
   📤 Step 2: Executing Opus job: abc123
   ✅ Opus job executed successfully
   ✅ Workflow triggered successfully!
      Job ID: abc123
      Status: initiated

   ============================================================
   ✅ Opus integration is working correctly!
   ============================================================
   ```

## What to Look For in Opus Workflow

Your Opus workflow should be configured to accept this input schema:

```json
{
  "event_type": "audit_completed",
  "audit_data": {
    "domain": "HIPAA",
    "target_api": "Healthcare API",
    "compliance_score": 85,
    "risk_level": "MEDIUM",
    "vulnerabilities_found": 3,
    "duration_seconds": 145.3,
    "critical_vulnerabilities": [],
    "timestamp": "2025-01-19T12:34:56Z"
  }
}
```

## Next Steps

1. **Check Railway logs** for Opus-related messages
2. **Verify environment variables** are set correctly
3. **Run a test audit** on production
4. **Check Opus dashboard** for triggered jobs
5. **Report back** what you see in the logs

If you see "✅ Opus integration enabled" and "✅ Opus job initiated" in Railway logs, then Opus IS working - you just need to check the Opus dashboard for the job executions.

If you see errors, share the exact error message and we can troubleshoot further.
