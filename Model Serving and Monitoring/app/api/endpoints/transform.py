from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io
import base64
import logging
from typing import List
from ...model_serving import ModelServer
from ...schemas.transform import TransformResponse
from ...main import model_server

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/transform", response_model=TransformResponse)
async def transform_image(
    file: UploadFile = File(...),
    style: str = None
):
    """Transform content image using style image"""
    try:
        # Read and validate image
        content_img = Image.open(file.file)
        
        # Get style image from predefined styles
        style_img = model_server.get_style_image(style)
        if style_img is None:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid style: {style}"
            )
        
        # Validate image sizes
        if content_img.size[0] > 1024 or content_img.size[1] > 1024:
            content_img = content_img.resize((1024, 1024), Image.Resampling.LANCZOS)
        if style_img.size[0] > 1024 or style_img.size[1] > 1024:
            style_img = style_img.resize((1024, 1024), Image.Resampling.LANCZOS)
        
        # Transform image
        result_img, inference_time = model_server.transform_image(content_img, style_img)
        
        # Convert result to bytes
        img_byte_arr = io.BytesIO()
        result_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return TransformResponse(
            transformed_image=base64.b64encode(img_byte_arr.getvalue()).decode(),
            inference_time=inference_time
        )
    except Exception as e:
        logger.error(f"Transform endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Transform failed",
                "message": str(e),
                "suggestion": "Please try again with a different image or style"
            }
        )