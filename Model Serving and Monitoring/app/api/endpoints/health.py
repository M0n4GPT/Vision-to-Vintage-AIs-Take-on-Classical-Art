from fastapi import APIRouter
import logging
import socket
from contextlib import closing
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

def find_free_port(start_port: int = 8000, max_port: int = 8999) -> int:
    """Find a free port in the given range"""
    for port in range(start_port, max_port + 1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"Could not find a free port between {start_port} and {max_port}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if model is loaded
        # This is a placeholder - replace with actual model check
        model_status = "healthy"
        
        # Check if services are running
        # This is a placeholder - replace with actual service checks
        services_status = "healthy"
        
        return {
            "status": "healthy",
            "model": model_status,
            "services": services_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        } 