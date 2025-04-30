"""
Image processing utility functions for the Vision-to-Vintage model serving application.
"""
import numpy as np
from PIL import Image
import cv2
from typing import Tuple, Optional

def preprocess_image(image: Image.Image, target_size: tuple = (224, 224)) -> np.ndarray:
    """
    Preprocess an image for model inference.
    
    Args:
        image: PIL Image object
        target_size: Target size for resizing (width, height)
        
    Returns:
        Preprocessed numpy array
    """
    # Ensure image is RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array
    image_array = np.array(image)
    
    # Convert to float32 and normalize
    image_array = image_array.astype(np.float32) / 255.0
    
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

def postprocess_image(image_array: np.ndarray) -> Image.Image:
    """
    Postprocess model output to create a displayable image.
    
    Args:
        image_array: Numpy array from model output
        
    Returns:
        PIL Image object
    """
    # Remove batch dimension if present
    if len(image_array.shape) == 4:
        image_array = image_array[0]
    
    # Clip values to valid range
    image_array = np.clip(image_array, 0, 1)
    
    # Convert to uint8
    image_array = (image_array * 255).astype(np.uint8)
    
    # Convert to PIL Image
    return Image.fromarray(image_array)

def resize_and_pad(image: Image.Image, 
                  target_size: Tuple[int, int], 
                  pad_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    """
    Resize image maintaining aspect ratio and pad if necessary.
    
    Args:
        image: PIL Image object
        target_size: Desired size (width, height)
        pad_color: Color to use for padding
        
    Returns:
        Resized and padded image
    """
    # Calculate aspect ratios
    target_ratio = target_size[0] / target_size[1]
    image_ratio = image.size[0] / image.size[1]
    
    if image_ratio > target_ratio:
        # Width is limiting factor
        new_width = target_size[0]
        new_height = int(new_width / image_ratio)
    else:
        # Height is limiting factor
        new_height = target_size[1]
        new_width = int(new_height * image_ratio)
    
    # Resize image
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create padded image
    padded = Image.new('RGB', target_size, pad_color)
    
    # Calculate padding
    left = (target_size[0] - new_width) // 2
    top = (target_size[1] - new_height) // 2
    
    # Paste resized image onto padded background
    padded.paste(resized, (left, top))
    
    return padded

def validate_image(image: Image.Image, 
                  min_size: Tuple[int, int] = (32, 32),
                  max_size: Tuple[int, int] = (4096, 4096)) -> Optional[str]:
    """
    Validate image dimensions and format.
    
    Args:
        image: PIL Image object
        min_size: Minimum allowed dimensions (width, height)
        max_size: Maximum allowed dimensions (width, height)
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if not isinstance(image, Image.Image):
        return "Invalid image format"
    
    width, height = image.size
    
    if width < min_size[0] or height < min_size[1]:
        return f"Image too small. Minimum size is {min_size[0]}x{min_size[1]} pixels"
    
    if width > max_size[0] or height > max_size[1]:
        return f"Image too large. Maximum size is {max_size[0]}x{max_size[1]} pixels"
    
    return None 