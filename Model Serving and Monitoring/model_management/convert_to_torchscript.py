import torch
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path to import the model architecture
sys.path.append(str(Path(__file__).parent.parent))

from app.model_serving import StyleTransferModel

def convert_to_torchscript():
    # Define paths
    base_dir = Path(__file__).parent.parent
    model_path = base_dir / "models" / "style_transfer_model.pt"
    output_path = base_dir / "models" / "style_transfer_model_torchscript.pt"
    
    # Create models directory if it doesn't exist
    os.makedirs(base_dir / "models", exist_ok=True)
    
    print(f"Loading model from {model_path}")
    
    try:
        # Try loading as TorchScript first
        try:
            print("Attempting to load as TorchScript model...")
            model = torch.jit.load(model_path, map_location='cpu')
            print("Model loaded successfully in TorchScript format!")
            
            # Save the model in CPU format
            print("Saving model in CPU format...")
            model.save(output_path)
            print(f"Model saved to {output_path}")
            
            # Verify the model can be loaded
            print("Verifying model can be loaded...")
            loaded_model = torch.jit.load(output_path)
            print("Model loaded successfully!")
            return
            
        except Exception as e:
            print(f"Error loading TorchScript model: {str(e)}")
            print("Attempting to load as state dict...")
        
        # If TorchScript loading fails, try loading as state dict
        model = StyleTransferModel()
        state_dict = torch.load(model_path, map_location='cpu', weights_only=False)
        model.load_state_dict(state_dict)
        model.eval()
        
        # Create example inputs for tracing
        content_input = torch.randn(1, 3, 512, 512)
        style_input = torch.randn(1, 3, 512, 512)
        
        # Convert to TorchScript
        print("Converting model to TorchScript format...")
        scripted_model = torch.jit.script(model)
        
        # Save the TorchScript model
        print(f"Saving TorchScript model to {output_path}")
        scripted_model.save(output_path)
        
        print("Conversion completed successfully!")
        
        # Verify the model can be loaded
        print("Verifying model can be loaded...")
        loaded_model = torch.jit.load(output_path)
        print("Model loaded successfully!")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    convert_to_torchscript() 