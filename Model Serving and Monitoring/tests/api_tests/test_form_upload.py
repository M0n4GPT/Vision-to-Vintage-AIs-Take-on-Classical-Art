#!/usr/bin/env python
"""
Simple FastAPI test server for file uploads
"""

import uvicorn
import io
import logging
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="File Upload Test API")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Test endpoint for file uploads.
    """
    try:
        logger.info(f"Received file with name: {file.filename}, content-type: {file.content_type}")
        
        # Read file
        file_bytes = await file.read()
        logger.info(f"File size: {len(file_bytes)} bytes")
        
        if len(file_bytes) == 0:
            logger.error("Received empty file")
            return JSONResponse(
                status_code=400,
                content={"error": "Empty file received"}
            )
        
        # Debug first few bytes
        hex_prefix = ' '.join([f'{b:02x}' for b in file_bytes[:20]])
        logger.info(f"First bytes: {hex_prefix}")
        
        # Check file signatures
        if file_bytes.startswith(b'\xff\xd8\xff'):
            logger.info("File has JPEG signature")
            file_type = "JPEG"
        elif file_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            logger.info("File has PNG signature")
            file_type = "PNG"
        else:
            logger.warning("File doesn't have recognized image signature")
            file_type = "unknown"
        
        # Try to validate as image
        try:
            image = Image.open(io.BytesIO(file_bytes))
            image_info = {
                "format": image.format,
                "mode": image.mode,
                "size": image.size
            }
            logger.info(f"Successfully loaded as image: {image_info}")
            
            # Try verification
            image.verify()
            logger.info("Image verification passed")
            valid_image = True
        except Exception as img_err:
            logger.error(f"Image validation error: {str(img_err)}")
            image_info = {}
            valid_image = False
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": len(file_bytes),
            "file_type": file_type,
            "is_valid_image": valid_image,
            "image_info": image_info
        }
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    logger.info(f"Starting test server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 