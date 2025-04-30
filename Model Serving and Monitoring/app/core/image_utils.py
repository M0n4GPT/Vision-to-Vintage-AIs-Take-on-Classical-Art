import torch
import numpy as np
from PIL import Image
from typing import Tuple
import logging
from .logging import setup_logger
import tensorflow as tf
import io

logger = setup_logger(__name__)

def preprocess_image(image: Image.Image) -> torch.Tensor:
    """
    Preprocess an image for model input.
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed image tensor
    """
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image to model's expected size
        target_size = (256, 256)  # TODO: Make this configurable
        image = image.resize(target_size, Image.LANCZOS)
        
        # Convert to numpy array and normalize
        image_array = np.array(image).astype(np.float32) / 255.0
        
        # Convert to tensor and add batch dimension
        image_tensor = torch.from_numpy(image_array).permute(2, 0, 1)
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor
        
    except Exception as e:
        logger.error(f"Image preprocessing failed: {str(e)}")
        raise

def postprocess_image(prediction: torch.Tensor) -> Image.Image:
    """
    Postprocess model output into a displayable image.
    
    Args:
        prediction: Model output tensor
        
    Returns:
        Postprocessed PIL Image
    """
    try:
        # Remove batch dimension and convert to numpy
        prediction = prediction.squeeze(0).permute(1, 2, 0).numpy()
        
        # Clip values to [0, 1] range
        prediction = np.clip(prediction, 0, 1)
        
        # Convert to uint8
        prediction = (prediction * 255).astype(np.uint8)
        
        # Create PIL Image
        result_image = Image.fromarray(prediction)
        
        return result_image
        
    except Exception as e:
        logger.error(f"Image postprocessing failed: {str(e)}")
        raise

def load_img(path_or_bytes, max_dim=512):
    """
    Load an image from disk or bytes, resize so longest side <= max_dim, normalize [0,1], batch it.
    
    Args:
        path_or_bytes: Path to image file or bytes object
        max_dim: Maximum dimension for resizing
        
    Returns:
        Preprocessed image tensor
    """
    if isinstance(path_or_bytes, str):
        img = tf.io.read_file(path_or_bytes)
    else:
        img = path_or_bytes
    
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    return img[tf.newaxis, :]

def tensor_to_image(tensor):
    """
    Convert a tensor to a PIL Image.
    
    Args:
        tensor: Image tensor
        
    Returns:
        PIL Image
    """
    tensor = tensor * 255
    tensor = tf.cast(tensor, tf.uint8)[0].numpy()
    return Image.fromarray(tensor) 