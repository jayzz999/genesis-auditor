"""
Webhook Manager for External Workflow Integrations
Supports Opus, Zapier, Make.com, and custom webhooks
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import hashlib
import hmac


class WebhookManager:
    """
    Manages webhook notifications for external workflow platforms
    """

    def __init__(self):
        self.webhooks: Dict[str, List[Dict]] = {
            "audit.started": [],
            "audit.completed": [],
            "audit.failed": [],
            "vulnerability.critical": [],
            "vulnerability.high": []
        }

    def register_webhook(
        self,
        event_type: str,
        webhook_url: str,
        secret: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Register a webhook for a specific event type

        Args:
            event_type: Event to trigger on (e.g., "audit.completed")
            webhook_url: URL to send POST request to
            secret: Optional secret for HMAC signature
            metadata: Additional metadata for filtering
        """
        if event_type not in self.webhooks:
            self.webhooks[event_type] = []

        webhook_config = {
            "url": webhook_url,
            "secret": secret,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }

        self.webhooks[event_type].append(webhook_config)
        print(f"✅ Registered webhook for {event_type}: {webhook_url}")

    def trigger_webhook(
        self,
        event_type: str,
        payload: Dict,
        async_mode: bool = True
    ):
        """
        Trigger all webhooks registered for an event type

        Args:
            event_type: Type of event
            payload: Data to send in webhook
            async_mode: Send webhooks asynchronously
        """
        if event_type not in self.webhooks:
            return

        webhooks_to_trigger = self.webhooks.get(event_type, [])

        if not webhooks_to_trigger:
            return

        print(f"📡 Triggering {len(webhooks_to_trigger)} webhooks for {event_type}")

        for webhook_config in webhooks_to_trigger:
            try:
                self._send_webhook(webhook_config, event_type, payload)
            except Exception as e:
                print(f"⚠️  Webhook delivery failed: {e}")

    def _send_webhook(
        self,
        webhook_config: Dict,
        event_type: str,
        payload: Dict
    ):
        """
        Send individual webhook request
        """
        url = webhook_config["url"]
        secret = webhook_config.get("secret")

        # Build webhook payload
        webhook_payload = {
            "event": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": payload,
            "source": "genesis-auditor"
        }

        # Add HMAC signature if secret provided
        headers = {"Content-Type": "application/json"}
        if secret:
            signature = self._generate_signature(webhook_payload, secret)
            headers["X-Genesis-Signature"] = signature

        # Send POST request
        response = requests.post(
            url,
            json=webhook_payload,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print(f"✅ Webhook delivered to {url}")
        else:
            print(f"⚠️  Webhook failed: {response.status_code}")

    def _generate_signature(self, payload: Dict, secret: str) -> str:
        """
        Generate HMAC-SHA256 signature for webhook verification
        """
        payload_str = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    def get_webhook_stats(self) -> Dict:
        """
        Get statistics about registered webhooks
        """
        stats = {}
        for event_type, webhooks in self.webhooks.items():
            stats[event_type] = len(webhooks)
        return stats


# Singleton instance
_webhook_manager = None

def get_webhook_manager() -> WebhookManager:
    """Get or create the webhook manager singleton"""
    global _webhook_manager
    if _webhook_manager is None:
        _webhook_manager = WebhookManager()
    return _webhook_manager
