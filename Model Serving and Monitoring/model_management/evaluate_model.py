#!/usr/bin/env python3

import argparse
import logging
import os
from pathlib import Path
import numpy as np
from PIL import Image
import mlflow
import tensorflow as tf
import json
import io

from model_management.model_serving import StyleTransferModel
from app.core.evaluation.model_validation import ModelEvaluator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_test_data(data_dir: str) -> dict:
    """Load test data from directory"""
    data_dir = Path(data_dir)
    images = []
    
    # Load all images from the test directory
    for img_path in data_dir.glob("*.jpg"):
        try:
            img = Image.open(img_path)
            img_array = np.array(img)
            images.append(img_array)
        except Exception as e:
            logger.warning(f"Failed to load image {img_path}: {str(e)}")
    
    return {"images": np.array(images)}

def load_domain_cases(cases_dir: str) -> list:
    """Load domain-specific test cases"""
    cases_dir = Path(cases_dir)
    cases = []
    
    # Load case definitions from JSON files
    for case_file in cases_dir.glob("*.json"):
        try:
            with open(case_file, "r") as f:
                case = json.load(f)
                # Load the image
                img_path = cases_dir / case["image_path"]
                if img_path.exists():
                    img = Image.open(img_path)
                    case["image"] = np.array(img)
                    cases.append(case)
        except Exception as e:
            logger.warning(f"Failed to load case {case_file}: {str(e)}")
    
    return cases

def main():
    parser = argparse.ArgumentParser(description="Evaluate style transfer model")
    parser.add_argument("--model_path", required=True, help="Path to the model file")
    parser.add_argument("--test_data_dir", required=True, help="Directory containing test images")
    parser.add_argument("--domain_cases_dir", required=True, help="Directory containing domain-specific test cases")
    parser.add_argument("--mlflow_tracking_uri", default="http://localhost:5000", help="MLFlow tracking server URI")
    args = parser.parse_args()
    
    # Set up MLFlow
    mlflow.set_tracking_uri(args.mlflow_tracking_uri)
    
    try:
        # Load model
        logger.info("Loading model...")
        model = StyleTransferModel()
        model.load(args.model_path)
        
        # Load test data
        logger.info("Loading test data...")
        test_data = load_test_data(args.test_data_dir)
        
        # Load domain-specific cases
        logger.info("Loading domain-specific cases...")
        domain_cases = load_domain_cases(args.domain_cases_dir)
        
        # Run evaluation
        logger.info("Starting model evaluation...")
        evaluator = ModelEvaluator()
        metrics, validation_result = evaluator.evaluate_model(
            model, test_data, domain_cases)
        
        # Log results
        logger.info("Evaluation complete.")
        logger.info(f"Validation {'passed' if validation_result else 'failed'}")
        logger.info("Metrics:")
        for metric_name, value in metrics.items():
            logger.info(f"  {metric_name}: {value}")
        
        return 0 if validation_result else 1
        
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 

class OfflineModelEvaluator:
    def __init__(self, model: StyleTransferModel, content_image_path: str, style_id: str):
        self.model = model
        self.content_image_path = content_image_path
        self.style_id = style_id

    def _load_and_preprocess_image(self, image_path):
        image = Image.open(image_path).convert("RGB")
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])
        return transform(image)

    def evaluate(self):
        logger.info(f"Starting evaluation for style: {self.style_id}")
        try:
            with mlflow.start_run(run_name=f"eval_{self.style_id}") as run:
                mlflow.log_param("style_id", self.style_id)
                mlflow.log_param("content_image", os.path.basename(self.content_image_path))

                with open(self.content_image_path, "rb") as f:
                    content_image_bytes = f.read()
                
                transformed_image_data = self.model.transform_image(
                    content_image_bytes, self.style_id
                )
                
                transformed_image_pil = Image.open(io.BytesIO(transformed_image_data["image_bytes"]))
                
                original_tensor = self._load_and_preprocess_image(self.content_image_path)
                transformed_tensor = transforms.ToTensor()(transformed_image_pil)

                original_np = original_tensor.cpu().numpy().transpose(1, 2, 0)
                transformed_np = transformed_tensor.cpu().numpy().transpose(1, 2, 0)

                current_psnr = psnr(original_np, transformed_np, data_range=1.0)
                current_ssim = ssim(original_np, transformed_np, data_range=1.0, channel_axis=-1, win_size=7)

                logger.info(f"Style: {self.style_id}, PSNR: {current_psnr:.2f}, SSIM: {current_ssim:.4f}")
                mlflow.log_metric("psnr", current_psnr)
                mlflow.log_metric("ssim", current_ssim)

                transformed_image_path = f"transformed_{self.style_id}.png"
                transformed_image_pil.save(transformed_image_path)
                mlflow.log_artifact(transformed_image_path, "transformed_images")
                os.remove(transformed_image_path)

                if current_psnr > 20 and current_ssim > 0.7:
                    logger.info("Metrics meet threshold, registering model.")
                else:
                    logger.info("Metrics below threshold, model not registered from this evaluation.")

                return {"psnr": current_psnr, "ssim": current_ssim}

        except Exception as e:
            logger.error(f"Error during evaluation for style {self.style_id}: {e}")
            mlflow.log_param("evaluation_error", str(e))
            if mlflow.active_run():
                 mlflow.end_run(status="FAILED")
            return None

if __name__ == "__main__":
    logger.info("Starting offline model evaluation script.")
    model_instance = StyleTransferModel.get_instance()
    
    content_image = "../data/examples/content/chicago.jpg"
    
    if not os.path.exists(content_image):
        logger.error(f"Content image not found at {content_image}. Please check the path.")
    else:
        example_style_id = "Claude_Monet_Impression_Sunrise"

        logger.info(f"Using content image: {content_image} and style: {example_style_id}")
        evaluator = OfflineModelEvaluator(model_instance, content_image, example_style_id)
        results = evaluator.evaluate()
        if results:
            logger.info(f"Evaluation finished for style {example_style_id}: {results}")
        else:
            logger.error(f"Evaluation failed for style {example_style_id}.")

# Add a section for ModelEvaluator if it's simple and was in app.core.evaluation.model_validation
# For now, I'm commenting out its direct usage to avoid NameError if it's not defined here.

# If ModelEvaluator was a simple class, it might look like this:
# class ModelEvaluator:
#     def __init__(self, model):
#         self.model = model
#
#     def evaluate_style_consistency(self, original_tensor, transformed_tensor, style_id):
#         # Placeholder for actual style consistency logic
#         logger.info(f"Evaluating style consistency for {style_id} (placeholder).")
#         return {"dummy_consistency_score": 0.85} 