"""
Style transfer endpoint for transforming images.
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import logging

from app.core.image_processing.processor import ImageProcessor
from app.core.models.model_optimization import ModelOptimizer

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/transform")
async def transform_image(
    content_image: UploadFile = File(...),
    style_name: str = "van_gogh"
):
    """
    Transform an image using the specified style.
    
    Args:
        content_image: The image to transform
        style_name: The style to apply (e.g., "van_gogh", "monet", "picasso")
    
    Returns:
        JSONResponse: The transformed image or error message
    """
    try:
        processor = ImageProcessor()
        model = ModelOptimizer("models/style_transfer_model.pt")
        
        # Process and transform image
        result = await processor.process_image(content_image, style_name, model)
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in transform_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 