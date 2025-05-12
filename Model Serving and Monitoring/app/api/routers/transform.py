from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from PIL import Image
import io
import logging
from typing import Dict
from pathlib import Path
import mlflow
from datetime import datetime

from ...model_serving import ModelServer
from ...core.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Define paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
STYLE_DIR = BASE_DIR / "data" / "styles"
STYLE_DIR.mkdir(parents=True, exist_ok=True)

# Define available styles
AVAILABLE_STYLES = {
    "starry_night": "Vincent_van_Gogh,The_Starry_Night.jpg",
    "mona_lisa": "Leonardo_da_Vinci,Mona_Lisa.jpg",
    "the_scream": "Edvard_Munch,The_Scream.jpg",
    "girl_with_pearl_earring": "Johannes_Vermeer,Girl_with_a_Pearl_Earring.jpg",
    "creation_of_adam": "Michelangelo,Creation_of_Adam.jpg",
    "le_reve": "Pablo_Picasso,Le_reve.jpg",
    "composition": "Piet_Mondriaan,Composition_in_Red,_Blue,_and_Yellow.jpg",
    "dance": "Henri_Matisse,dance.jpg",
    "odalisque": "Jean-Auguste_Dominique_Ingres,La_grande_odalisque.jpg",
    "impression_sunrise": "Claude_Monet,Impression_Sunrise.jpg"
}

async def process_image(file: UploadFile) -> Image.Image:
    """Process uploaded image"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid file type",
                    "message": "Only image files are allowed",
                    "suggestion": "Please upload a valid image file (JPEG, JPG, or PNG)",
                    "details": f"Received content type: {file.content_type}"
                }
            )
        
        # Validate file extension
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['jpg', 'jpeg', 'png']:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid file format",
                    "message": "Only JPEG, JPG, and PNG formats are supported",
                    "suggestion": "Please convert your image to JPEG, JPG, or PNG format",
                    "details": f"Received file extension: {file_ext}"
                }
            )
        
        # Read and validate image
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        return img
    except Exception as e:
        logger.error(f"Image processing failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Image processing failed",
                "message": "Failed to process the uploaded image",
                "suggestion": "Please ensure you're uploading a valid image file",
                "details": str(e)
            }
        )

@router.post("/")
async def transform_image(
    file: UploadFile = File(...),
    style: str = Form(...)
) -> Response:
    """Transform an image using the specified style"""
    try:
        # Validate style
        if style not in AVAILABLE_STYLES:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid style",
                    "message": f"Style '{style}' is not available",
                    "suggestion": f"Please choose from: {', '.join(AVAILABLE_STYLES.keys())}",
                    "details": f"Available styles: {list(AVAILABLE_STYLES.keys())}"
                }
            )

        # Process content image
        content_image = await process_image(file)
        
        # Load style image
        style_path = STYLE_DIR / AVAILABLE_STYLES[style]
        if not style_path.exists():
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Style image not found",
                    "message": f"Style image for '{style}' is missing",
                    "suggestion": "Please contact support",
                    "details": f"Missing file: {style_path}"
                }
            )
        
        style_image = Image.open(style_path)
        
        # Check for data drift
        drift_score = model_server.check_data_drift(content_image)
        if drift_score > 0.5:  # Threshold for drift
            logger.warning(f"High data drift detected: {drift_score}")
            try:
                mlflow.log_metric("data_drift_score", drift_score)
            except Exception as e:
                logger.warning(f"Failed to log drift score: {str(e)}")
        
        # Transform image
        try:
            result_image, inference_time = model_server.transform_image(content_image, style_image)
        except Exception as e:
            logger.error(f"Image transformation failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Transformation failed",
                    "message": "Failed to transform the image",
                    "suggestion": "Please try again with a different image",
                    "details": str(e)
                }
            )
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        result_image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Log metrics
        try:
            mlflow.log_metric("inference_time", inference_time)
            mlflow.log_metric("image_size", len(img_byte_arr.getvalue()))
        except Exception as e:
            logger.warning(f"Failed to log metrics: {str(e)}")
        
        # Return response with headers
        return Response(
            content=img_byte_arr.getvalue(),
            media_type="image/jpeg",
            headers={
                "X-Inference-Time": f"{inference_time:.3f}",
                "X-Drift-Score": f"{drift_score:.3f}",
                "X-Style-Used": style
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in transform endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "suggestion": "Please try again later",
                "details": str(e)
            }
        )

@router.get("/styles")
async def list_styles():
    """List available styles"""
    return {"styles": list(AVAILABLE_STYLES.keys())} 