"""
API endpoints for the Vision to Vintage application.
"""
from .style_transfer import router as style_transfer_router
from .health import router as health_router

__all__ = ['style_transfer_router', 'health_router'] 