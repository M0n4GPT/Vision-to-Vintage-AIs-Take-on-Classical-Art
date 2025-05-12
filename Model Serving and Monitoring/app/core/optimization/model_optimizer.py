import tensorflow as tf
import tensorflow_hub as hub
import tf2onnx
import onnx
import onnxruntime as ort
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ModelOptimizer:
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.model = None
        self.optimized_model = None
        self.quantized_model = None
        
    def load_model(self):
        """Load model from TensorFlow Hub or local path"""
        if self.model_path:
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            self.model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
        return self.model
    
    def convert_to_onnx(self, output_path: str):
        """Convert TensorFlow model to ONNX format"""
        if not self.model:
            raise ValueError("Model not loaded. Call load_model() first.")
            
        # Convert to ONNX
        spec = (tf.TensorSpec((None, None, None, 3), tf.float32, name="content_image"),
                tf.TensorSpec((None, None, None, 3), tf.float32, name="style_image"))
        onnx_model, _ = tf2onnx.convert.from_function(
            self.model, 
            input_signature=spec,
            opset=13
        )
        
        # Save ONNX model
        onnx.save(onnx_model, output_path)
        logger.info(f"Model converted to ONNX and saved to {output_path}")
        
        # Load ONNX model for inference
        self.optimized_model = ort.InferenceSession(output_path)
        return self.optimized_model
    
    def quantize_model(self, output_path: str):
        """Quantize model for better performance"""
        if not self.optimized_model:
            raise ValueError("ONNX model not loaded. Call convert_to_onnx() first.")
            
        # Quantize ONNX model
        from onnxruntime.quantization import quantize_dynamic, QuantType
        quantize_dynamic(
            self.optimized_model.get_model_path(),
            output_path,
            weight_type=QuantType.QUInt8
        )
        
        # Load quantized model
        self.quantized_model = ort.InferenceSession(output_path)
        logger.info(f"Model quantized and saved to {output_path}")
        return self.quantized_model
    
    def optimize_for_device(self, device: str = "cpu"):
        """Optimize model for specific device"""
        if not self.optimized_model:
            raise ValueError("ONNX model not loaded. Call convert_to_onnx() first.")
            
        # Set optimization options based on device
        options = ort.SessionOptions()
        if device == "gpu":
            options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            options.intra_op_num_threads = 1
            options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        else:
            options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            options.intra_op_num_threads = 4
            options.execution_mode = ort.ExecutionMode.ORT_PARALLEL
            
        # Create optimized session
        self.optimized_model = ort.InferenceSession(
            self.optimized_model.get_model_path(),
            options
        )
        return self.optimized_model 