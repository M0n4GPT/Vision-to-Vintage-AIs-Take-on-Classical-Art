from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import io
import logging
import time
import shutil
from typing import Dict, List
from pydantic import BaseModel, Field
from datetime import datetime
import json
from app.minio_client import MinioClient
from fastapi.responses import Response
from app.model_serving import ModelServer

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/style", tags=["style"])

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

class Evaluation(BaseModel):
    model_config = {
        'protected_namespaces': (),
        'json_schema_extra': {
            'example': {
                'style_accuracy': 8,
                'content_preservation': 7,
                'overall_quality': 8,
                'comment': 'Great style transfer!'
            }
        }
    }
    style_accuracy: int = Field(ge=0, le=10)
    content_preservation: int = Field(ge=0, le=10)
    overall_quality: int = Field(ge=0, le=10)
    comment: str = None

def load_img(path_to_img):
    """Load and preprocess image"""
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

def tensor_to_image(tensor):
    """Convert tensor to image"""
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)

@router.post("/transform")
async def transform_image(
    content_image: UploadFile = File(...),
    style_name: str = Form(...)
):
    """Transform content image with specified style"""
    try:
        # Log the incoming request
        logger.info(f"Received transform request with style: {style_name}")
        
        # Validate style name
        if not style_name:
            logger.warning("Empty style name provided")
            raise HTTPException(
                status_code=400,
                detail="Style name is required"
            )
            
        if style_name not in AVAILABLE_STYLES:
            available_styles = list(AVAILABLE_STYLES.keys())
            logger.warning(f"Invalid style name provided: {style_name}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid style name",
                    "available_styles": available_styles,
                    "message": f"Please choose from one of the following styles: {', '.join(available_styles)}"
                }
            )

        # Validate content image
        if not content_image.content_type.startswith('image/'):
            logger.warning(f"Invalid file type provided: {content_image.content_type}")
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image file."
            )

        # Process the content image
        content_bytes = await content_image.read()
        content_img = Image.open(io.BytesIO(content_bytes))
        
        # Load style image
        style_path = Path("data/styles") / AVAILABLE_STYLES[style_name]
        if not style_path.exists():
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Style image not found",
                    "message": f"Style image for '{style_name}' not found.",
                    "suggestion": "Please contact support."
                }
            )
        style_img = Image.open(style_path)
        
        # Get model server instance
        model_path = Path("models/style_transfer_model.pt")
        if not model_path.exists():
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Model not found",
                    "message": "Style transfer model not found.",
                    "suggestion": "Please ensure the model is properly installed."
                }
            )
        
        model_server = ModelServer(str(model_path))
        
        # Apply style transfer
        result_img, inference_time = await model_server.transform_image(content_img, style_img)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        result_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Create response with headers
        response = Response(content=img_byte_arr, media_type="image/png")
        response.headers["X-Inference-Time"] = f"{inference_time:.3f}"
        
        return response
        
    except Exception as e:
        logger.error(f"Error during style transfer: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Style transfer failed",
                "message": "Failed to process the image.",
                "details": str(e)
            }
        )

@router.get("/list")
async def list_styles():
    """List all available styles"""
    return {
        "styles": list(AVAILABLE_STYLES.keys()),
        "count": len(AVAILABLE_STYLES)
    }

@router.post("/evaluate")
async def evaluate_result(evaluation: Evaluation, image_id: str = Form(...)):
    """Submit evaluation for a style transfer result"""
    try:
        # Save evaluation to file
        evaluation_data = evaluation.dict()
        evaluation_data["timestamp"] = datetime.now().isoformat()
        evaluation_data["image_id"] = image_id
        # Save to metrics directory
        metrics_dir = Path("data/metrics")
        metrics_dir.mkdir(parents=True, exist_ok=True)
        evaluation_file = metrics_dir / f"evaluation_{int(time.time())}.json"
        with open(evaluation_file, "w") as f:
            json.dump(evaluation_data, f)

        # If style_accuracy is low, upload image to MinIO for retraining
        if evaluation.style_accuracy <= 3:
            minio_client = MinioClient()
            image_path = Path("data/production") / f"{image_id}.jpg"
            if image_path.exists():
                minio_client.upload_file(str(image_path), object_name=f"production/feedback/{image_id}.jpg")
                logger.info(f"Uploaded low-score image {image_id}.jpg to MinIO for feedback loop.")
            else:
                logger.warning(f"Image for feedback not found: {image_path}")

        return {"message": "Evaluation saved successfully"}
    except Exception as e:
        logger.error(f"Error saving evaluation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to save evaluation"
        ) 