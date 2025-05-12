"""
Style Transfer API
Main FastAPI application for the style transfer service.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Query, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_client import generate_latest
import io
import base64
import logging
import os
import time
import json
import uuid
from typing import Optional, List, Dict, Any
from PIL import Image
from pathlib import Path
import shutil
from sqlalchemy.orm import Session
from schemas.evaluation import Evaluation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure static styles directory exists *before* mounting
APP_ROOT = Path(__file__).parent # /app
STATIC_STYLES_DIR_ABS = APP_ROOT / "static" / "styles"
STATIC_STYLES_DIR_ABS.mkdir(parents=True, exist_ok=True)
logger.info(f"Ensured static styles directory exists at: {STATIC_STYLES_DIR_ABS}")

# Initialize FastAPI app
app = FastAPI(title="Style Transfer API", description="API for applying artistic styles to images")

# Mount static files directory for style images
# The path for StaticFiles should be relative to where the Python script is run or an absolute path.
# Since the app runs from /app, "app/static/styles" becomes "static/styles" if CWD is /app.
# Using the absolute path STATIC_STYLES_DIR_ABS is safer.
app.mount("/static/styles", StaticFiles(directory=str(STATIC_STYLES_DIR_ABS)), name="static_styles")

# Set up templates
# templates_dir_abs = APP_ROOT / "templates"
# templates = Jinja2Templates(directory=str(templates_dir_abs))
templates = Jinja2Templates(directory="templates") # Assuming templates is in /app/templates

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import MinIO client for feedback storage
from minio_client import get_minio_client

# Import model and monitoring modules
from model_management.model_serving import get_model_instance, StyleTransferModel
from monitoring.monitoring import get_metrics_manager, MetricsManager

# Initialize model instance and metrics manager (singleton)
model_instance = StyleTransferModel.get_instance()
metrics_manager = get_metrics_manager()
logger.info(f"Metrics manager initialized. Has registry: {hasattr(metrics_manager, 'registry')}")

# db: Session = Depends(get_db) # <<<< THIS LINE WAS CAUSING THE NameError AND IS REMOVED/COMMENTED OUT

# STATIC_STYLES_DIR = Path("app/static/styles") # Path("app/static/styles") - This was defined too late
# STATIC_STYLES_DIR.mkdir(parents=True, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: Copying style images to static directory...")
    
    # Clean the static styles directory first (excluding styles.css)
    logger.info(f"Cleaning static styles directory: {STATIC_STYLES_DIR_ABS}")
    if STATIC_STYLES_DIR_ABS.exists():
        for item in STATIC_STYLES_DIR_ABS.iterdir():
            if item.name == "styles.css": # Don't delete the main CSS file
                continue
            if item.is_dir():
                import shutil
                shutil.rmtree(item)
                logger.debug(f"Removed directory: {item}")
            elif item.is_file():
                item.unlink()
                logger.debug(f"Removed file: {item}")
    
    all_styles = model_instance.get_style_list() # Get styles with their original file_paths
    copied_count = 0
    error_count = 0
    
    # Ensure the base static directory for styles exists
    STATIC_STYLES_DIR_ABS.mkdir(parents=True, exist_ok=True)

    for style_info in all_styles:
        try:
            # original_path is the source path of the style image
            # e.g., /app/data/styles/Claude_Monet/impression_sunrise.jpg if data is at /app/data
            # or relative to where model_serving.py calculated it (e.g. data/styles/...)
            # Let's ensure original_path is an absolute path within the container if it's not already
            
            original_path_str = style_info["file_path"]
            # In model_serving.py, STYLES_DIR = DATA_DIR / "styles" and DATA_DIR = PROJECT_ROOT / "data"
            # PROJECT_ROOT is 'Model Serving and Monitoring'. So, path is relative to 'Model Serving and Monitoring'
            # Inside the container, the app root is /app.
            # Assume 'data' directory is at '/app/data/' if Dockerfile copies it or mounts it there.
            # Let's try to resolve it relative to a potential /app if it's not absolute.
            original_path = Path(original_path_str)
            if not original_path.is_absolute():
                # This assumes the 'data' directory from the project root is mapped or copied to '/app/data' in the container
                # Or, more robustly, that model_serving.py provides a path relative to project root,
                # and we make it absolute based on a known project root in container.
                # For now, let's assume style_info["file_path"] might be like "data/styles/Artist/Painting.jpg"
                # and needs to be prefixed with /app if running in container.
                # However, model_serving.py uses Path(os.dirname(os.dirname(os.path.abspath(__file__))))
                # which should make original_path absolute IF the model_serving.py is inside the project structure
                # that's also the WORKDIR or copied into /app.
                # Let's log the original_path to debug
                logger.debug(f"Original path from style_info: {original_path}, is_absolute: {original_path.is_absolute()}")
                # If original_path is like "data/styles/..." it needs to be relative to APP_ROOT
                # This is tricky. model_serving.py calculates it based on ITS location.
                # Let's rely on the fact that get_style_list() is called by model instance in main.py (at /app)
                # and model_serving.py's PROJECT_ROOT is 'Model Serving and Monitoring'
                # This means style_info["file_path"] is an absolute path on the HOST.
                # We need to map this to an absolute path INSIDE the container.
                # This implies 'data/styles' from host's 'Model Serving and Monitoring' must be available at a known path in container.
                # Docker-compose mounts ./data:/app/data
                # So, a host path like ".../Model Serving and Monitoring/data/styles/Artist/File.jpg"
                # becomes "/app/data/styles/Artist/File.jpg" in container.
                
                # Correct approach: original_path from style_info is already what we need if 'data' is mounted to /app/data
                # and StyleTransferModel was initialized with styles_dir="data/styles/" (relative to /app)
                # Let's re-check StyleTransferModel init
                # model = get_model_instance() calls StyleTransferModel.get_instance(styles_dir="data/styles/")
                # __init__ uses styles_dir. Path(styles_dir) / artist_name / painting_filename
                # So, if styles_dir="data/styles/", then original_path is "data/styles/Artist/Painting.jpg"
                # This is relative to /app. So, it becomes /app/data/styles/Artist/Painting.jpg
                
                container_source_path = APP_ROOT / original_path # e.g. /app/data/styles/Artist/File.jpg

            else: # If original_path is already absolute, it might be a host path. This needs mapping.
                  # Let's assume for now the paths from get_style_list are relative to /app
                container_source_path = APP_ROOT / original_path.relative_to(original_path.anchor) if original_path.is_absolute() and str(APP_ROOT) not in str(original_path) else original_path


            if not container_source_path.exists():
                logger.warning(f"Source style image does not exist: {container_source_path}")
                error_count += 1
                continue

            # Destination artist directory should use the same artist name format as web_url
            # style_info[\"artist\"] is like "Claude Monet"
            artist_name_for_dir = style_info["artist"] # Use the title-cased name
            # Sanitize for directory name (though less critical if FastAPI handles URL encoding for static files)
            artist_name_for_dir_sanitized = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in artist_name_for_dir).strip()
            if not artist_name_for_dir_sanitized:
                artist_name_for_dir_sanitized = "Unknown_Artist"
            
            painting_filename = Path(style_info["painting_filename"]) # Already just filename.ext
            
            # STATIC_STYLES_DIR_ABS is /app/static/styles
            static_artist_dir = STATIC_STYLES_DIR_ABS / artist_name_for_dir_sanitized
            static_artist_dir.mkdir(parents=True, exist_ok=True)
            
            destination_path = static_artist_dir / painting_filename
            
            if not destination_path.exists():
                import shutil
                shutil.copy(container_source_path, destination_path)
                logger.info(f"Copied style image {container_source_path} to {destination_path}")
                copied_count += 1
            else:
                logger.debug(f"Style image {destination_path} already exists. Skipping copy.")
        except Exception as e:
            logger.error(f"Error copying style image {style_info.get('file_path', 'N/A')}: {e}", exc_info=True)
            error_count += 1
    logger.info(f"Finished copying style images. Copied: {copied_count}, Errors: {error_count}")

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    """Serve the index page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/styles", response_class=HTMLResponse)
async def list_styles(request: Request):
    """List all available styles."""
    styles_data = model_instance.get_style_list() # This now returns the detailed list
    
    # Group styles by artist
    artists = {}
    for style_info in styles_data:
        artist_name = style_info["artist"]
        if artist_name not in artists:
            artists[artist_name] = []
        # Pass the whole style_info dictionary to the template
        artists[artist_name].append(style_info) 
    
    return templates.TemplateResponse(
        "styles.html",
        {"request": request, "artists": artists}
    )

@app.get("/api/styles")
async def get_styles():
    """Get all available styles as JSON."""
    start_time = time.time()
    
    try:
        styles = model_instance.get_style_list()
        
        # Record metrics
        duration = time.time() - start_time
        metrics_manager.record_api_request("/api/styles", "GET", 200, duration)
        
        return {"styles": styles}
    except Exception as e:
        logger.error(f"Error getting styles: {e}")
        
        # Record metrics
        duration = time.time() - start_time
        metrics_manager.record_api_request("/api/styles", "GET", 500, duration)
        
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transform")
async def transform_image(
    style_id: str,
    content_image: UploadFile,
    model_instance: StyleTransferModel = Depends(get_model_instance) # Ensure latest instance
):
    """Transform content image using a specified style ID."""
    start_time = time.time()
    
    try:
        # Read content image
        logger.info(f"Reading image: filename={content_image.filename}")
        
        # Validate content type
        valid_types = ['image/jpeg', 'image/jpg', 'image/png']
        if content_image.content_type not in valid_types:
            logger.warning(f"Invalid content type: {content_image.content_type}")
            
            # Record metrics
            duration = time.time() - start_time
            metrics_manager.record_api_request("/transform", "POST", 400, duration)
            
            raise HTTPException(
                status_code=400,
                detail=f"Invalid content type. Supported types: {', '.join(valid_types)}"
            )
        
        # Read image bytes
        content_bytes = await content_image.read()
        
        if not content_bytes:
            logger.error("Empty content received")
            # Record metrics
            duration = time.time() - start_time
            # Use the actual metrics object, not the string 'metrics'
            metrics_manager.record_api_request("/transform", "POST", 400, duration)
            raise HTTPException(status_code=400, detail="Empty image uploaded")
        
        # Transform image
        logger.info(f"Starting transformation with style ID: {style_id}")
        # Use the injected model_instance
        result_img, processing_time = model_instance.transform_image(content_bytes, style_id) # Restore actual transform
        
        logger.info(f"Transformation completed in {processing_time:.2f} seconds")
        
        # Encode result image
        img_bytes = io.BytesIO()
        result_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        
        # Record metrics
        duration = time.time() - start_time
        metrics_manager.record_api_request("/transform", "POST", 200, duration)
        metrics_manager.record_model_prediction(style_id, "success", processing_time)
        
        image_data_url = f"data:image/png;base64,{img_base64}"
        
        return {
            "status": "success",
            "processing_time": processing_time,
            "transformed_image": image_data_url
        }
    
    except ValueError as e: # Specific handler for ValueErrors like style not found
        logger.error(f"Value error in transform_image: {e}")
        duration = time.time() - start_time
        metrics_manager.record_api_request("/transform", "POST", 404, duration)
        if style_id:
            metrics_manager.record_model_prediction(style_id, "error", duration)
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        # Log error
        logger.error(f"Error in transform_image: {e}")
        
        # Record metrics
        duration = time.time() - start_time
        metrics_manager.record_api_request("/transform", "POST", 500, duration)
        if style_id:
            # Use the actual metrics object, not the string 'metrics'
            metrics_manager.record_model_prediction(style_id, "error", duration)
        
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def submit_feedback(
    request: Request,
    style_id: str = Query(..., description="The ID of the style for which feedback is being submitted"),
    feedback: Evaluation = Body(...),
    metrics: MetricsManager = Depends(get_metrics_manager),  # Corrected: ensure this is the dependency
    # db: Session = Depends(get_db)
):
    """Submit feedback for a style transfer."""
    # Log the type and value of 'metrics' at the beginning of the function
    logger.info(f"Inside submit_feedback - type(metrics param): {type(metrics)}, metrics param: {metrics}") # Corrected to log the 'metrics' parameter
    start_time = time.time()
    
    try:
        # Example: Record feedback sentiment (e.g., from a user survey or direct input)
        # Extract detailed feedback
        rating = int(feedback.get("rating", 5))
        comments = feedback.get("comments", "")
        image_data = feedback.get("image_data", None)  # Base64 encoded image, if provided
        
        # Determine sentiment
        if rating >= 4:
            sentiment = "positive"
        elif rating <= 2:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Record metrics
        metrics.record_feedback(sentiment)
        
        # Prepare feedback data for storage
        feedback_data = {
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "style_id": style_id,
            "image_id": feedback.get("image_id"),
            "rating": rating,
            "sentiment": sentiment,
            "comments": comments,
            "metrics": metrics
        }
        
        # Store feedback in MinIO
        try:
            minio_client = get_minio_client()
            current_metrics_manager = get_metrics_manager() # get current manager
            
            # Store feedback metadata
            feedback_json = json.dumps(feedback_data).encode('utf-8')
            feedback_path = f"feedback/{feedback_data['id']}.json"
            minio_client.put_object(
                bucket_name="feedback",
                object_name=feedback_path,
                data=io.BytesIO(feedback_json),
                length=len(feedback_json),
                content_type="application/json"
            )
            
            # If this is a negative rating, store the image for retraining
            if sentiment == "negative" and image_data:
                try:
                    # Convert base64 to bytes
                    if isinstance(image_data, str) and image_data.startswith("data:image"):
                        # Handle data URL format
                        image_data = image_data.split(",")[1]
                    
                    image_bytes = base64.b64decode(image_data)
                    
                    # Save to MinIO for retraining
                    retraining_path = f"feedback/retraining/{feedback_data['id']}.png"
                    minio_client.put_object(
                        bucket_name="feedback",
                        object_name=retraining_path,
                        data=io.BytesIO(image_bytes),
                        length=len(image_bytes),
                        content_type="image/png"
                    )
                    
                    logger.info(f"Saved negative feedback image to MinIO: {retraining_path}")
                except Exception as img_err:
                    logger.error(f"Failed to save feedback image: {img_err}")
            
            logger.info(f"Stored feedback in MinIO: {feedback_path}")
        except Exception as minio_err:
            logger.error(f"Failed to store feedback in MinIO: {minio_err}")
        
        # Record metrics
        duration = time.time() - start_time
        metrics.record_api_request("/feedback", "POST", 200, duration)
        
        return {
            "status": "success",
            "feedback_id": feedback_data["id"]
        }
    
    except AttributeError as e:
        logger.error(f"AttributeError in submit_feedback: {e}. metrics object is {type(metrics)}") # Also log the type of the 'metrics' parameter here
        duration = time.time() - start_time
        # Even if there's an error with metrics object itself, try to log API failure if possible
        metrics.record_api_request("/feedback", "POST", 500, duration)
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        # Log error
        logger.error(f"Error in submit_feedback: {e}")
        
        # Record metrics
        duration = time.time() - start_time
        metrics.record_api_request("/feedback", "POST", 500, duration)
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics", tags=["Monitoring"], response_class=Response)
async def metrics_endpoint():
    """Serve Prometheus metrics."""
    # metrics_manager is already defined globally in this module now
    return Response(generate_latest(metrics_manager.registry), media_type="text/plain")

@app.get("/api/metrics")
async def get_api_metrics():
    """Get recent model metrics as JSON."""
    start_time = time.time()
    
    try:
        # Use the actual metrics object, not the string 'metrics'
        metrics_manager.record_api_request("/api/metrics", "GET", 200, time.time() - start_time)
        summary = metrics_manager.get_summary()
        return summary
    
    except Exception as e:
        # Log error
        logger.error(f"Error in get_api_metrics: {e}")
        
        # Record metrics
        duration = time.time() - start_time
        metrics_manager.record_api_request("/api/metrics", "GET", 500, duration)
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        return {
            "status": "healthy",
            "model": "loaded" if model_instance is not None else "not_loaded",
            "uptime_seconds": metrics_manager.get_metrics_summary()["uptime_seconds"]
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "error", "message": str(e)} 