"""
Model loading and management utility functions for the Vision-to-Vintage model serving application.
"""
import tensorflow as tf
from pathlib import Path
from typing import Dict, Any, Optional, Union
import json
import os

class ModelManager:
    """Manager class for handling model operations."""
    
    def __init__(self, model_dir: str):
        """
        Initialize ModelManager.
        
        Args:
            model_dir: Directory containing model files
        """
        self.model_dir = Path(model_dir)
        self.model: Optional[tf.keras.Model] = None
        self.metadata: Dict[str, Any] = {}
        
    def load_model(self, model_name: str) -> tf.keras.Model:
        """
        Load a TensorFlow model from disk.
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            Loaded TensorFlow model
        """
        model_path = self.model_dir / model_name
        self.model = tf.keras.models.load_model(str(model_path))
        self._load_metadata(model_name)
        return self.model
    
    def save_model(self, model: tf.keras.Model, model_name: str) -> None:
        """
        Save a TensorFlow model to disk.
        
        Args:
            model: TensorFlow model to save
            model_name: Name to save the model as
        """
        model_path = self.model_dir / model_name
        model.save(str(model_path))
        self._save_metadata(model, model_name)
    
    def get_model_metadata(self, model: Optional[tf.keras.Model] = None) -> Dict[str, Any]:
        """
        Get metadata about a model.
        
        Args:
            model: TensorFlow model (uses stored model if None)
            
        Returns:
            Dictionary containing model metadata
        """
        if model is None:
            model = self.model
        if model is None:
            raise ValueError("No model loaded")
            
        return {
            "input_shape": model.input_shape,
            "output_shape": model.output_shape,
            "num_layers": len(model.layers),
            "trainable_params": model.count_params(),
            "model_config": model.get_config()
        }
    
    def optimize_for_inference(self, 
                             model: Optional[tf.keras.Model] = None,
                             quantize: bool = True,
                             target_dtype: str = 'float16') -> Union[tf.keras.Model, tf.lite.Interpreter]:
        """
        Optimize model for inference.
        
        Args:
            model: Model to optimize (uses stored model if None)
            quantize: Whether to apply quantization
            target_dtype: Target data type for quantization
            
        Returns:
            Optimized model or TFLite interpreter
        """
        if model is None:
            model = self.model
        if model is None:
            raise ValueError("No model loaded")
        
        # Convert to TensorFlow Lite format
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        
        if quantize:
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            if target_dtype == 'float16':
                converter.target_spec.supported_types = [tf.float16]
            elif target_dtype == 'int8':
                converter.target_spec.supported_types = [tf.int8]
        
        tflite_model = converter.convert()
        
        # Load the optimized model
        interpreter = tf.lite.Interpreter(model_content=tflite_model)
        interpreter.allocate_tensors()
        
        return interpreter
    
    def _save_metadata(self, model: tf.keras.Model, model_name: str) -> None:
        """Save model metadata to disk."""
        metadata = self.get_model_metadata(model)
        metadata_path = self.model_dir / f"{model_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        self.metadata = metadata
    
    def _load_metadata(self, model_name: str) -> None:
        """Load model metadata from disk."""
        metadata_path = self.model_dir / f"{model_name}_metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = self.get_model_metadata(self.model) 