from fastapi import FastAPI, UploadFile, File, HTTPException, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import io
import logging
import json
from typing import List, Optional
from pydantic import BaseModel, conint
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Vision-to-Vintage API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths
BASE_DIR = Path(__file__).parent.parent
STYLE_DIR = BASE_DIR / "data" / "styles"
STYLE_DIR.mkdir(parents=True, exist_ok=True)
METRICS_DIR = BASE_DIR / "data" / "metrics"
METRICS_DIR.mkdir(parents=True, exist_ok=True)

# Load TensorFlow Hub model
try:
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    logger.info("Model loaded successfully from TensorFlow Hub")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise HTTPException(status_code=500, detail="Failed to load model")

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

# Pydantic models for evaluation
class Evaluation(BaseModel):
    style_accuracy: conint(ge=0, le=10)
    content_preservation: conint(ge=0, le=10)
    overall_quality: conint(ge=0, le=10)
    comment: Optional[str] = None

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

@app.post("/transform")
async def transform_image(
    content_image: UploadFile = File(...),
    style_name: str = Form(...)
):
    """Transform content image with specified style"""
    try:
        # Validate style name
        if style_name not in AVAILABLE_STYLES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid style name. Available styles: {list(AVAILABLE_STYLES.keys())}"
            )

        # Save uploaded image temporarily
        content_path = STYLE_DIR / "temp_content.jpg"
        with open(content_path, "wb") as buffer:
            content = await content_image.read()
            buffer.write(content)
        
        # Load and process images
        content_image = load_img(str(content_path))
        style_path = Path(__file__).parent.parent.parent / "ModelTraining" / "vision-to-vintage-app" / "style" / AVAILABLE_STYLES[style_name]
        style_image = load_img(str(style_path))
        
        # Generate stylized image
        stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]
        
        # Convert to PIL Image
        result_image = tensor_to_image(stylized_image)
        
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        result_image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Clean up temp file
        content_path.unlink()
        
        # Return image directly
        return Response(content=img_byte_arr, media_type="image/jpeg")
        
    except Exception as e:
        logger.error(f"Error transforming image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/styles")
async def list_styles():
    """List available style images"""
    try:
        return {"styles": list(AVAILABLE_STYLES.keys())}
    except Exception as e:
        logger.error(f"Error listing styles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate")
async def evaluate_result(evaluation: Evaluation):
    """Save evaluation metrics"""
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = METRICS_DIR / f"evaluation_{timestamp}.json"
        
        # Save evaluation
        with open(filename, "w") as f:
            json.dump(evaluation.dict(), f)
        
        return {"message": "Evaluation saved successfully"}
    except Exception as e:
        logger.error(f"Error saving evaluation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/evaluations")
async def get_evaluations():
    """Get all evaluations"""
    try:
        evaluations = []
        for file in METRICS_DIR.glob("*.json"):
            with open(file, "r") as f:
                evaluations.append(json.load(f))
        return {"evaluations": evaluations}
    except Exception as e:
        logger.error(f"Error getting evaluations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 