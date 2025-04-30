"""
Style transfer model implementation using PyTorch.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import logging

logger = logging.getLogger(__name__)

class StyleTransferModel(nn.Module):
    """
    Neural style transfer model that combines content and style images.
    """
    
    def __init__(self):
        super(StyleTransferModel, self).__init__()
        
        # Encoder layers
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True)
        )
        
        # Decoder layers
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(512, 256, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 3, kernel_size=3, stride=1, padding=1),
            nn.Tanh()
        )
        
        # Style transfer layers
        self.style_transfer = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True)
        )
        
        logger.info("Style transfer model initialized")
        
    def forward(self, content_image, style_image):
        """
        Forward pass of the style transfer model.
        
        Args:
            content_image: Content image tensor
            style_image: Style image tensor
            
        Returns:
            Stylized image tensor
        """
        # Encode content and style images
        content_features = self.encoder(content_image)
        style_features = self.encoder(style_image)
        
        # Apply style transfer
        stylized_features = self.style_transfer(content_features)
        
        # Combine content and style features
        combined_features = stylized_features + 0.1 * style_features
        
        # Decode to get final image
        output = self.decoder(combined_features)
        
        return output 