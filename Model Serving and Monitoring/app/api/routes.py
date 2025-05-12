from fastapi import APIRouter
from .routers import transform, evaluation

# Create main API router
router = APIRouter()

# Include routers
router.include_router(transform.router, prefix="/transform", tags=["transform"])
router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"]) 