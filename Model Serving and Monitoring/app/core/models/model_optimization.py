"""
Model optimization and loading utilities.
"""

import os
import logging
import tensorflow_hub as hub
import tensorflow as tf
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelOptimizer:
    """
    Handles model optimization and loading.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the model optimizer.
        
        Args:
            model_path: Path to the model file or directory
        """
        self.model_path = Path(model_path)
        self.model = None
        self.device = "GPU" if tf.config.list_physical_devices('GPU') else "CPU"
        logger.info(f"Using {self.device} for inference")
        
    def load_model(self):
        """
        Load the style transfer model from TensorFlow Hub.
        
        Returns:
            Loaded model
        """
        try:
            # Load the TensorFlow Hub model
            hub_url = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
            self.model = hub.load(hub_url)
            logger.info("Model loaded successfully from TensorFlow Hub")
            return self.model
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
            
    def optimize_model(self):
        """
        Optimize the model for inference.
        Currently a placeholder as the TensorFlow Hub model is already optimized.
        """
        logger.info("Model is already optimized from TensorFlow Hub")
        return self.model 