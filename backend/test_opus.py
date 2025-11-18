#!/usr/bin/env python3
"""
Quick test script to verify Opus integration is working
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from integrations.opus_client import get_opus_client

def test_opus_integration():
    print("=" * 60)
    print("Testing Opus Integration")
    print("=" * 60)

    # Check environment variables
    api_key = os.getenv('OPUS_API_KEY')
    workflow_id = os.getenv('OPUS_WORKFLOW_ID')
    base_url = os.getenv('OPUS_BASE_URL', 'https://operator.opus.com')

    print(f"\n📋 Configuration:")
    print(f"   API Key: {'✅ Set' if api_key else '❌ Missing'}")
    print(f"   Workflow ID: {workflow_id if workflow_id else '❌ Missing'}")
    print(f"   Base URL: {base_url}")

    if not api_key:
        print("\n❌ OPUS_API_KEY not set!")
        print("   Set it with: export OPUS_API_KEY=your_key_here")
        return False

    if not workflow_id:
        print("\n⚠️  OPUS_WORKFLOW_ID not set, using default from code")

    # Get Opus client
    print("\n🔄 Initializing Opus client...")
    opus_client = get_opus_client()

    if not opus_client:
        print("❌ Failed to initialize Opus client")
        return False

    print("✅ Opus client initialized")

    # Test workflow trigger
    print("\n🧪 Testing audit completed workflow trigger...")
    try:
        response = opus_client.trigger_audit_completed_workflow(
            domain="TEST",
            target_api_name="Test API - Opus Integration Check",
            compliance_score=85,
            risk_level="LOW",
            vulnerabilities_found=2,
            duration_seconds=30.5,
            critical_vulnerabilities=[]
        )

        print(f"✅ Workflow triggered successfully!")
        print(f"   Job ID: {response.get('job_id')}")
        print(f"   Status: {response.get('status')}")
        print(f"   Response: {response.get('response')}")

        return True
    except Exception as e:
        print(f"❌ Workflow trigger failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_opus_integration()
    print("\n" + "=" * 60)
    if success:
        print("✅ Opus integration is working correctly!")
    else:
        print("❌ Opus integration has issues")
    print("=" * 60)
    sys.exit(0 if success else 1)
