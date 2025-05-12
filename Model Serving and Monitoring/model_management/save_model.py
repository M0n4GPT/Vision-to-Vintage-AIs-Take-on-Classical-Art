import os
import sys
import torch
import logging
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.model_serving import StyleTransferModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_model(model_path: str, output_path: str):
    """Save the trained model in the correct format for serving"""
    try:
        # Create model instance
        model = StyleTransferModel()
        
        # Load trained weights
        state_dict = torch.load(model_path, map_location='cpu')
        model.load_state_dict(state_dict)
        
        # Set model to evaluation mode
        model.eval()
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save model
        torch.save(model.state_dict(), output_path)
        logger.info(f"Model saved successfully to {output_path}")
        
        # Save model info
        info_path = os.path.join(os.path.dirname(output_path), 'model_info.txt')
        with open(info_path, 'w') as f:
            f.write(f"Model: StyleTransferModel\n")
            f.write(f"Input size: 256x256\n")
            f.write(f"Output size: 256x256\n")
            f.write(f"Device: CPU\n")
            f.write(f"Framework: PyTorch\n")
            f.write(f"Version: {torch.__version__}\n")
        
    except Exception as e:
        logger.error(f"Failed to save model: {str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python save_model.py <input_model_path> <output_model_path>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    save_model(input_path, output_path) 