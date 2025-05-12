#!/usr/bin/env python3
"""
Script to generate reference data for drift monitoring.
This script creates dummy reference data for drift monitoring initialization.
In a real-world scenario, this would be replaced with actual reference data
from your validation dataset.
"""

import os
import argparse
import numpy as np
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_dummy_image(output_path, width=224, height=224):
    """Create a random colored image as dummy data."""
    # Create a random RGB image
    img_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save(output_path)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Generate reference data for drift monitoring")
    parser.add_argument(
        "--output-dir", 
        default="./data/reference",
        help="Directory to save reference data"
    )
    parser.add_argument(
        "--num-samples", 
        type=int, 
        default=10,
        help="Number of samples to generate per style"
    )
    args = parser.parse_args()
    
    # List of styles that match your application
    styles = ["impressionist", "cubist", "surrealist", "abstract", "renaissance"]
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    for style in styles:
        # Create style directory
        style_dir = os.path.join(args.output_dir, style)
        os.makedirs(style_dir, exist_ok=True)
        
        # Generate dummy images for this style
        for i in range(args.num_samples):
            image_path = os.path.join(style_dir, f"sample_{i}.png")
            create_dummy_image(image_path)
            logger.info(f"Created dummy image: {image_path}")
    
    logger.info(f"Generated {args.num_samples} reference samples for each of the {len(styles)} styles.")
    logger.info(f"Total: {args.num_samples * len(styles)} reference images created in {args.output_dir}")

if __name__ == "__main__":
    main() 