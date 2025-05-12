"""
Image processor for handling image transformations.
"""
import io
import torch
from PIL import Image
import torchvision.transforms as transforms
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Handles image processing and transformation.
    """
    
    def __init__(self):
        """Initialize the image processor."""
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])
    
    async def process_image(
        self, 
        content_image: bytes, 
        style_name: str,
        model: Any
    ) -> Dict[str, Any]:
        """
        Process and transform an image.
        
        Args:
            content_image: The image to transform
            style_name: The style to apply
            model: The style transfer model
            
        Returns:
            Dict[str, Any]: Processing results
        """
        try:
            # Load and preprocess image
            image = Image.open(io.BytesIO(content_image))
            image_tensor = self.transform(image).unsqueeze(0)
            
            # Apply style transfer
            with torch.no_grad():
                output = model(image_tensor)
            
            # Convert output to image
            output_image = transforms.ToPILImage()(output.squeeze(0).cpu())
            
            # Save or return the result
            output_buffer = io.BytesIO()
            output_image.save(output_buffer, format="JPEG")
            output_buffer.seek(0)
            
            return {
                "status": "success",
                "message": "Image transformed successfully",
                "image": output_buffer.getvalue()
            }
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise 