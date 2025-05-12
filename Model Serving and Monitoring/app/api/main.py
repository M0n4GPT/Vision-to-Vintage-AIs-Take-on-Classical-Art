from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from prometheus_client import Counter, Histogram, generate_latest
import uvicorn
import os
from pathlib import Path
import shutil
from typing import Optional
from PIL import Image
import io
import time
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.monitoring.drift_detection import DriftDetector
from app.core.monitoring.drift_dashboard import DriftDashboard
import sys
import json
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import logging
from app.core.models.model_optimization import ModelOptimizer

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Vision-to-Vintage API",
    description="API for AI-powered classical art style transfer with monitoring",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize metrics
request_counter = Counter("style_transfer_requests_total", "Total number of style transfer requests")
latency_histogram = Histogram("style_transfer_latency_seconds", "Style transfer request latency")

# Define paths
BASE_DIR = Path(__file__).parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "style_transfer_model.pt"
STYLE_DIR = BASE_DIR / "serving" / "style"
REFERENCE_DATA_PATH = BASE_DIR / "data" / "reference"
METRICS_PATH = BASE_DIR / "data" / "metrics" / "drift_metrics.json"

# Create necessary directories
REFERENCE_DATA_PATH.mkdir(parents=True, exist_ok=True)
METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

# Initialize drift detector and dashboard
drift_detector = DriftDetector(reference_data_path=str(REFERENCE_DATA_PATH))
drift_dashboard = DriftDashboard(app=app, metrics_path=str(METRICS_PATH))

# Load model
try:
    model_optimizer = ModelOptimizer(model_path="")  # No local model path needed for TF Hub
    model = model_optimizer.load_model()
    logger.info("Model loaded successfully from TensorFlow Hub")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise HTTPException(status_code=500, detail="Failed to load model from TensorFlow Hub")

def load_img(path, max_dim=512):
    """Load an image from disk, resize so longest side <= max_dim, normalize [0,1], batch it."""
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    return img[tf.newaxis, :]

def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = tf.cast(tensor, tf.uint8)[0].numpy()
    return Image.fromarray(tensor)

# Initialize Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Vision-to-Vintage API",
        "endpoints": {
            "/transform": "Transform an image with a style",
            "/drift-dashboard": "View drift monitoring dashboard",
            "/metrics": "View Prometheus metrics",
            "/health": "Health check endpoint"
        }
    }

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(
            status_code=200,
            content={"message": "File uploaded successfully", "filename": file.filename}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.post("/style-transfer")
async def style_transfer(
    content_image: UploadFile = File(...),
    style_image: UploadFile = File(...)
):
    if model_optimizer is None:
        raise HTTPException(status_code=500, detail="Model not initialized. Please run setup.sh")
        
    request_counter.inc()
    start_time = time.time()
    
    try:
        # Read and validate images
        content_img = Image.open(io.BytesIO(await content_image.read()))
        style_img = Image.open(io.BytesIO(await style_image.read()))
        
        # Apply style transfer
        with latency_histogram.time():
            result_img = model_optimizer.predict(content_img, style_img)
        
        # Save result
        result_path = UPLOAD_DIR / f"result_{int(time.time())}.jpg"
        result_img.save(result_path)
        
        # Calculate metrics
        latency = time.time() - start_time
        metrics = model_optimizer.benchmark_performance()
        
        # Update drift metrics
        drift_metrics = drift_detector.detect_drift(content_img, style_img)
        drift_dashboard.update_metrics(drift_metrics)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Style transfer completed successfully",
                "result_path": str(result_path),
                "metrics": metrics,
                "latency": latency,
                "drift_metrics": drift_metrics
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during style transfer: {str(e)}")

@app.get("/metrics")
async def get_metrics():
    """Endpoint for Prometheus metrics."""
    return generate_latest()

@app.get("/drift-dashboard")
async def get_drift_dashboard():
    """Endpoint for drift monitoring dashboard."""
    return HTMLResponse(content=drift_dashboard.get_dashboard())

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/transform")
async def transform_image(
    content_image: UploadFile = File(...),
    style_name: str = "starry_night"
):
    """
    Transform an image using the specified style.
    
    Args:
        content_image: The image to transform
        style_name: Name of the style to apply
        
    Returns:
        Transformed image as bytes and drift metrics
    """
    request_counter.inc()
    start_time = time.time()
    
    try:
        # Save content image temporarily
        content_path = STYLE_DIR / "temp_content.jpg"
        content_bytes = await content_image.read()
        with open(content_path, "wb") as f:
            f.write(content_bytes)
            
        # Load style image
        style_path = STYLE_DIR / f"{style_name}.jpg"
        if not style_path.exists():
            raise HTTPException(status_code=404, detail=f"Style {style_name} not found")
            
        # Load images
        content_tensor = load_img(str(content_path))
        style_tensor = load_img(str(style_path))
        
        # Detect drift
        drift_metrics = drift_detector.detect_drift(
            current_content=content_tensor.numpy(),
            current_style=style_tensor.numpy()
        )
        
        # Save metrics
        with open(METRICS_PATH, 'w') as f:
            json.dump(drift_metrics, f)
        
        # Transform image
        with latency_histogram.time():
            output_tensor = model(tf.constant(content_tensor), tf.constant(style_tensor))[0]
        
        # Convert output to image
        output_image = tensor_to_image(output_tensor)
        
        # Save output to bytes
        output_bytes = io.BytesIO()
        output_image.save(output_bytes, format="JPEG")
        
        # Clean up temp file
        os.remove(content_path)
        
        # Calculate latency
        latency = time.time() - start_time
        
        return JSONResponse(
            content={
                "image": output_bytes.getvalue().hex(),
                "metrics": {
                    "drift": drift_metrics,
                    "latency": latency
                }
            },
            media_type="application/json"
        )
        
    except Exception as e:
        logger.error(f"Error transforming image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 