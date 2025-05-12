#!/usr/bin/env python3
"""
Generate test production data for drift monitoring.
This script copies and modifies some reference images to simulate production data
for testing drift monitoring functionality.
"""

import os
import sys
import argparse
import shutil
import random
from PIL import Image, ImageEnhance, ImageFilter

def parse_args():
    parser = argparse.ArgumentParser(description="Generate test production data")
    parser.add_argument("--reference-dir", type=str, required=True, 
                        help="Directory containing reference data")
    parser.add_argument("--output-dir", type=str, required=True,
                        help="Output directory for production data")
    parser.add_argument("--num-samples", type=int, default=5,
                        help="Number of samples to generate")
    parser.add_argument("--drift-factor", type=float, default=0.3,
                        help="How much to modify images (0.0-1.0), higher means more drift")
    return parser.parse_args()

def apply_random_transform(img, drift_factor):
    """Apply random transformations to an image to simulate drift"""
    transforms = [
        lambda x: ImageEnhance.Brightness(x).enhance(1.0 + random.uniform(-0.5, 0.5) * drift_factor),
        lambda x: ImageEnhance.Contrast(x).enhance(1.0 + random.uniform(-0.5, 0.5) * drift_factor),
        lambda x: ImageEnhance.Color(x).enhance(1.0 + random.uniform(-0.5, 0.5) * drift_factor),
        lambda x: x.filter(ImageFilter.GaussianBlur(radius=random.uniform(0, 2) * drift_factor))
    ]
    
    # Apply 1-3 random transforms
    num_transforms = random.randint(1, 3)
    selected_transforms = random.sample(transforms, num_transforms)
    
    result = img
    for transform in selected_transforms:
        result = transform(result)
    
    return result

def main():
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Define art styles matching the application
    styles = ["impressionist", "cubist", "surrealist", "abstract", "renaissance"]
    
    # Create style directories
    for style in styles:
        style_dir = os.path.join(args.output_dir, style)
        os.makedirs(style_dir, exist_ok=True)
    
    # Get all image files in reference directory
    ref_files = []
    for root, _, files in os.walk(args.reference_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                ref_files.append(os.path.join(root, file))
    
    if not ref_files:
        print(f"No image files found in {args.reference_dir}")
        return 1
    
    # For each style, generate samples
    samples_per_style = max(1, args.num_samples // len(styles))
    
    for style in styles:
        style_dir = os.path.join(args.output_dir, style)
        
        # Generate samples for this style
        for i in range(samples_per_style):
            try:
                # Select a random reference image
                file_path = random.choice(ref_files)
                
                # Open the image
                img = Image.open(file_path).convert('RGB')
                
                # Apply random transformations
                modified_img = apply_random_transform(img, args.drift_factor)
                
                # Save to style directory
                output_filename = f"{style}_sample_{i+1}.jpg"
                output_path = os.path.join(style_dir, output_filename)
                modified_img.save(output_path)
                print(f"Generated {output_path}")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    total_generated = samples_per_style * len(styles)
    print(f"Successfully generated {total_generated} test images across {len(styles)} styles in {args.output_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 