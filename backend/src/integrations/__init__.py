"""
Integration modules for external platforms
"""

from .webhook_manager import WebhookManager, get_webhook_manager
from .opus_client import OpusClient, get_opus_client

__all__ = ['WebhookManager', 'get_webhook_manager', 'OpusClient', 'get_opus_client']
