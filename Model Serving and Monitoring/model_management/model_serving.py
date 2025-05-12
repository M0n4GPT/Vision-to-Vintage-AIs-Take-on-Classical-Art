"""
Model serving module for style transfer application.
This module handles loading the model and performing style transfer.
"""
import os
import time
import logging
import torch
from pathlib import Path
import io
from PIL import Image
import numpy as np
from typing import Tuple, List, Dict, Optional, Union
import torchvision.transforms as transforms

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths configuration
PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# MODEL_DIR = PROJECT_ROOT / "models" # No longer needed if using absolute path from env
DATA_DIR = PROJECT_ROOT / "data"
STYLES_DIR = DATA_DIR / "styles"
RESULTS_DIR = DATA_DIR / "production"

# Model parameters
DEFAULT_IMAGE_SIZE = 512

class StyleTransferModel:
    """Style transfer model handler"""
    
    _instance = None

    @classmethod
    def get_instance(cls, styles_dir: str = "data/styles/"):
        # Use environment variable for model_path, with a fallback for local testing if needed
        model_path_from_env = os.environ.get('MODEL_PATH', "models/model.pt") 
        if cls._instance is None:
            cls._instance = cls(model_path=model_path_from_env, styles_dir=styles_dir)
        return cls._instance

    def __init__(self, model_path: str, styles_dir: str = "data/styles/"):
        if StyleTransferModel._instance is not None:
            raise Exception("StyleTransferModel is a singleton. Use get_instance().")
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        self.style_dir = styles_dir
        self.style_labels_to_ids = {}
        self.style_ids_to_labels = {}
        
        self._load_style_mappings() # Build the mappings

        try:
            self.model = torch.jit.load(model_path, map_location=self.device)
            self.model.eval()
            logger.info(f"Model '{model_path}' loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading TorchScript model from {model_path}: {e}")
            raise
        
        # The JIT model (Stylizer) expects integer labels corresponding to sorted style directory names.
        # Create a mapping from style_name (artist_painting) to this integer label.
        self.style_name_to_label_map: Dict[str, int] = {}
        self.available_styles: Dict[str, str] = {} # For displaying available styles {style_id: full_path_to_style_image}
        
        try:
            # The Stylizer class in the training script uses sorted directory names as labels.
            # These directory names are integers (e.g., "00", "01").
            # We need to map our style names (artist_painting) to these integer labels.
            # For now, let's assume styles_dir contains artist named subfolders,
            # and each of those contain painting files.
            # The Stylizer would have been trained with style images from directories like "0", "1", ...
            # or it took style images from subdirectories of 'styles_dir' and sorted those subdirectories.
            # The key is that the JIT model's internal `self.style_feats` list is ordered.

            # We need to match the order of `self.style_feats` in the scripted `Stylizer` model.
            # The `Stylizer` in train_style_transfer.py does:
            #   style_dirs = sorted(os.listdir(style_dir)) # style_dir here is like 'data/styles_for_training/00', 'data/styles_for_training/01'
            #   for label in style_dirs:
            #       self.style_feats.append(feat)
            # So, the integer label corresponds to the sorted order of these 'label' directories.

            # For the current `styles_dir` structure ("data/styles/Artist/Painting.jpg"),
            # we need a consistent way to map these to integer indices that `model.pt` expects.
            # Let's sort artists, then paintings within artists, and assign an index.
            
            current_label = 0
            sorted_artists = sorted(os.listdir(self.style_dir))
            for artist_name in sorted_artists:
                artist_path = os.path.join(self.style_dir, artist_name)
                if os.path.isdir(artist_path):
                    sorted_paintings = sorted(os.listdir(artist_path))
                    for painting_filename in sorted_paintings:
                        if painting_filename.lower().endswith((".png", ".jpg", ".jpeg")):
                            painting_name = os.path.splitext(painting_filename)[0]
                            # style_id = f"{artist_name.lower().replace(' ', '_')}_{painting_name.lower().replace(' ', '_')}"
                            style_id = painting_name.lower().replace(' ', '_') # As per previous request
                            
                            self.style_name_to_label_map[style_id] = current_label
                            self.available_styles[style_id] = os.path.join(artist_path, painting_filename)
                            current_label += 1
            
            if not self.style_name_to_label_map:
                logger.warning(f"No styles found in {styles_dir}. Style transfer will not work.")
            else:
                logger.info(f"Loaded {len(self.style_name_to_label_map)} styles with label mapping.")
                # logger.debug(f"Style to label map: {self.style_name_to_label_map}")

        except Exception as e:
            logger.error(f"Error loading styles from {styles_dir}: {e}")
            # Not raising here, as the app might still run but style transfer will fail.

        # Make sure the transform matches what the Stylizer model was trained with.
        # The training script `train_style_transfer.py` uses:
        # transforms.Compose([transforms.Resize(256), transforms.CenterCrop(256), transforms.ToTensor()])
        # It does not include Normalization in the Stylizer's transform passed to its __init__,
        # as VGG encoding (which includes normalization if pretrained VGG is used) happens inside Stylizer.
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)), # Consistent with training script
            transforms.CenterCrop((256,256)), # Consistent with training script
            transforms.ToTensor(),
        ])
        self.output_transform = transforms.ToPILImage()

    def _load_style_mappings(self):
        logger.info(f"StyleTransferModel loading style mappings from: {self.style_dir}")
        idx_counter = 0
        if not os.path.exists(self.style_dir):
            logger.error(f"Style directory {self.style_dir} does not exist!")
            return

        for artist_name in os.listdir(self.style_dir):
            artist_path = os.path.join(self.style_dir, artist_name)
            if os.path.isdir(artist_path):
                for style_image_name in os.listdir(artist_path):
                    if style_image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        # Use filename without extension as style_id_str
                        style_id_str = os.path.splitext(style_image_name)[0]
                        # Use the same style_id_str that Stylizer class would generate
                        
                        if style_id_str not in self.style_labels_to_ids:
                            self.style_labels_to_ids[style_id_str] = idx_counter
                            self.style_ids_to_labels[idx_counter] = style_id_str
                            # logger.debug(f"Loaded style mapping: '{style_id_str}' -> {idx_counter}")
                            idx_counter += 1
        if not self.style_labels_to_ids:
            logger.warning(f"No style mappings loaded from {self.style_dir}. Check directory structure: {{style_dir}}/{{ArtistName}}/{{image_file}}")
        else:
            logger.info(f"Loaded {len(self.style_labels_to_ids)} style mappings: {self.style_labels_to_ids}")

    def _preprocess_image(self, image_path_or_bytes, is_content=True):
        try:
            if isinstance(image_path_or_bytes, str): # path
                image = Image.open(image_path_or_bytes).convert('RGB')
            elif isinstance(image_path_or_bytes, bytes): # bytes
                image = Image.open(io.BytesIO(image_path_or_bytes)).convert('RGB')
            else:
                raise ValueError("Input must be a file path or bytes.")
            
            image_tensor = self.transform(image)
            return image_tensor.unsqueeze(0).to(self.device) # Add batch dimension
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise

    def _postprocess_image(self, tensor):
        try:
            image = tensor.squeeze(0).cpu().clamp(0, 1) # Remove batch, move to CPU, clamp
            return self.output_transform(image)
        except Exception as e:
            logger.error(f"Error postprocessing image: {e}")
            raise

    def get_available_styles(self) -> Dict[str, str]:
        return self.available_styles
    
    def get_style_list(self) -> List[Dict[str, str]]:
        """
        Returns a list of available styles formatted for the frontend.
        Each item includes id, artist, name, image_url, and original file_path.
        """
        style_list = []
        # Ensure styles are loaded and mappings exist
        if not self.style_ids_to_labels:
             self._load_style_mappings() # Attempt to load if empty

        for style_idx, style_id_str in self.style_ids_to_labels.items():
            # Reconstruct artist and image name from style_id_str if needed, or from a path
            # For simplicity, assuming style_id_str is "PaintingName" and we need to find its artist folder
            # This requires knowing the structure inside self.style_dir (e.g., data/styles/ArtistName/PaintingName.jpg)
            
            found_path = None
            artist_name_from_path = "Unknown"
            image_filename_on_disk = f"{style_id_str}.jpg" # Assume jpg, could be png etc.

            for artist_folder in os.listdir(self.style_dir):
                artist_folder_path = os.path.join(self.style_dir, artist_folder)
                if os.path.isdir(artist_folder_path):
                    # Attempt to find the file, checking common extensions
                    for ext in ['.jpg', '.jpeg', '.png']:
                        potential_file = os.path.join(artist_folder_path, style_id_str + ext)
                        if os.path.exists(potential_file):
                            found_path = potential_file
                            artist_name_from_path = artist_folder
                            image_filename_on_disk = style_id_str + ext
                            break
                    if found_path:
                        break
            
            if found_path:
                image_url = f"{artist_name_from_path}/{image_filename_on_disk}" # Relative to static/styles/
                style_list.append({
                    "id": style_id_str, # Use the string ID from mapping
                    "artist": artist_name_from_path.replace("_", " "),
                    "name": style_id_str.replace("_", " "),
                    "image_url": image_url, # Path relative to the styles directory for url_for
                    "original_file_path": found_path
                })
            else:
                logger.warning(f"Could not find image file for style_id: {style_id_str} in {self.style_dir}")
        
        # Sort by artist then by name
        style_list.sort(key=lambda x: (x['artist'].lower(), x['name'].lower()))
        return style_list

    def transform_image(self, content_image_bytes: bytes, style_id: str) -> Tuple[Image.Image, float]:
        """Transform content image using a specified style ID."""
        process_start_time = time.time()

        logger.debug(f"Transforming with style ID: {style_id}")
        content_tensor = self._preprocess_image(content_image_bytes)
        
        if style_id not in self.style_name_to_label_map:
            logger.error(f"Style ID '{style_id}' not found in style_name_to_label_map.")
            raise ValueError(f"Style ID '{style_id}' not found.")
        
        style_label_int = self.style_name_to_label_map[style_id]
        logger.debug(f"Mapped style ID '{style_id}' to integer label: {style_label_int}")
        
        # The JIT model (Stylizer) expects 'style_label' as its second argument.
        # The error "len() of a 0-d tensor" indicates it expects an iterable (e.g., 1-D tensor).
        style_label_tensor = torch.tensor([style_label_int], device=self.device, dtype=torch.long)

        try:
            with torch.no_grad():
                start_inference_time = time.time()
                # Pass the style_label_tensor to the model
                output_tensor = self.model(content_tensor, style_label_tensor)
                # Ensure this log is INFO to capture it easily
                logger.info(f"Output tensor from JIT: min={output_tensor.min().item():.4f}, max={output_tensor.max().item():.4f}, mean={output_tensor.mean().item():.4f}, shape={output_tensor.shape}, dtype={output_tensor.dtype}")
                end_inference_time = time.time()
                processing_time = end_inference_time - start_inference_time
                logger.info(f"Inference completed in {processing_time:.4f} seconds for style '{style_id}'.")

            output_image = self._postprocess_image(output_tensor)
            total_processing_time = time.time() - process_start_time
            logger.info(f"Total transformation process completed in {total_processing_time:.4f} seconds.")
            return output_image, processing_time
        except RuntimeError as e:
            logger.error(f"TorchScript runtime error during model inference for style '{style_id}' (label {style_label_int}): {e}")
            # Reraise the exception to be caught by the API endpoint handler
            raise
        except Exception as e:
            logger.error(f"Unexpected error during model inference for style '{style_id}' (label {style_label_int}): {e}")
            raise

def get_model_instance() -> StyleTransferModel:
    """
    Get or create a model instance.
    
    Returns:
        StyleTransferModel instance
    """
    # Pass styles_dir if it needs to be configurable, otherwise defaults can be used
    # Default styles_dir is 'data/styles/' which should resolve to '/app/data/styles/'
    return StyleTransferModel.get_instance() 