#!/usr/bin/env python
"""
Setup script to ensure style images are properly organized for the style transfer model.
This script copies style images from data/styles to the required directories.
"""
import os
import shutil
import logging
import json
from pathlib import Path
from PIL import Image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = PROJECT_ROOT / "data"
STYLES_DIR = DATA_DIR / "styles"
PRODUCTION_DIR = DATA_DIR / "production"

def ensure_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs(STYLES_DIR, exist_ok=True)
    os.makedirs(PRODUCTION_DIR, exist_ok=True)
    logger.info(f"Created directories: {STYLES_DIR}, {PRODUCTION_DIR}")

def get_style_images():
    """Get all style images from the styles directory."""
    if not os.path.exists(STYLES_DIR):
        logger.error(f"Style directory not found: {STYLES_DIR}")
        return []
    
    style_files = [f for f in os.listdir(STYLES_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    logger.info(f"Found {len(style_files)} style images")
    return style_files

def process_style_images():
    """Process and organize style images."""
    ensure_directories()
    style_files = get_style_images()
    
    if not style_files:
        logger.error("No style images found")
        return
    
    # Create artist directories and process images
    styles_metadata = []
    
    for style_file in style_files:
        # Get name without extension
        style_name = os.path.splitext(style_file)[0]
        
        # Determine artist and painting name
        if ',' in style_name:
            artist, painting = style_name.split(',', 1)
            display_name = f"{artist.replace('_', ' ')} - {painting.replace('_', ' ')}"
        else:
            artist = style_name
            display_name = style_name.replace('_', ' ')
        
        # Create style ID
        style_id = style_name.replace(' ', '_').replace(',', '_').lower()
        
        # Create artist directory in production folder
        artist_dir = PRODUCTION_DIR / artist.replace(' ', '_')
        os.makedirs(artist_dir, exist_ok=True)
        
        # Add metadata
        styles_metadata.append({
            'id': style_id,
            'name': display_name,
            'artist': artist.replace('_', ' '),
            'file': style_file,
            'path': str(STYLES_DIR / style_file)
        })
    
    # Save styles metadata
    with open(DATA_DIR / "styles_metadata.json", "w") as f:
        json.dump(styles_metadata, f, indent=2)
    
    logger.info(f"Processed {len(styles_metadata)} style images")
    
    # Log available styles
    for style in styles_metadata:
        logger.info(f"Style: {style['name']} (ID: {style['id']})")

def main():
    """Main entry point."""
    logger.info("Starting style setup...")
    process_style_images()
    logger.info("Style setup completed")

if __name__ == "__main__":
    main() 