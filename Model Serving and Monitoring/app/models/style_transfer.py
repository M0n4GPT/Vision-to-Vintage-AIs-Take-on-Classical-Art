import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import io
import mlflow
import logging
from app.core.config import settings
import numpy as np
from typing import Dict, Any, Tuple

logger = logging.getLogger("style_transfer")

class StyleTransferModel:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model()
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])
        
    def _load_model(self) -> nn.Module:
        """Load the model with optimizations"""
        try:
            # Load model from MLflow
            model = mlflow.pytorch.load_model(
                f"models:/{settings.MLFLOW_EXPERIMENT_NAME}/{settings.MODEL_VERSION}"
            )
            
            # Optimize model
            model = model.to(self.device)
            model.eval()
            
            # Enable model optimizations
            if torch.cuda.is_available():
                model = torch.jit.script(model)  # TorchScript optimization
                model = model.half()  # FP16 optimization
            
            return model
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    async def transform(self, image_bytes: bytes, style: str) -> Dict[str, Any]:
        """Transform an image using the specified style"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Preprocess image
            input_tensor = self.transform(image).unsqueeze(0)
            input_tensor = input_tensor.to(self.device)
            
            # Apply model optimizations
            with torch.no_grad():
                if torch.cuda.is_available():
                    with torch.cuda.amp.autocast():  # Mixed precision
                        output = self.model(input_tensor)
                else:
                    output = self.model(input_tensor)
            
            # Convert output to image
            output_image = self._tensor_to_image(output[0])
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            output_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return {
                "image": img_byte_arr,
                "style": style,
                "device": str(self.device)
            }
            
        except Exception as e:
            logger.error(f"Error transforming image: {str(e)}")
            raise
    
    async def evaluate(self, original: bytes, transformed: bytes, style: str) -> float:
        """Evaluate the quality of the transformation"""
        try:
            # Load images
            original_img = Image.open(io.BytesIO(original))
            transformed_img = Image.open(io.BytesIO(transformed))
            
            # Convert to tensors
            original_tensor = self.transform(original_img)
            transformed_tensor = self.transform(transformed_img)
            
            # Calculate metrics
            mse = nn.MSELoss()(original_tensor, transformed_tensor)
            psnr = 10 * torch.log10(1 / mse)
            
            # Calculate style consistency
            style_score = self._calculate_style_consistency(
                original_tensor, transformed_tensor, style
            )
            
            # Combine scores
            final_score = (psnr.item() + style_score) / 2
            
            return final_score
            
        except Exception as e:
            logger.error(f"Error evaluating images: {str(e)}")
            raise
    
    def _tensor_to_image(self, tensor: torch.Tensor) -> Image.Image:
        """Convert tensor to PIL Image"""
        tensor = tensor.cpu().clamp(0, 1)
        tensor = tensor.squeeze()
        return transforms.ToPILImage()(tensor)
    
    def _calculate_style_consistency(
        self, original: torch.Tensor, transformed: torch.Tensor, style: str
    ) -> float:
        """Calculate style consistency score"""
        # Implement style-specific metrics
        # This is a placeholder - implement actual style metrics
        return 0.8  # Placeholder score 