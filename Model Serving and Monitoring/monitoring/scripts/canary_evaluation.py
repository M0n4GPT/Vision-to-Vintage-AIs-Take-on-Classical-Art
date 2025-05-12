import requests
import time
import random
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Tuple
import json
import os
from datetime import datetime
import numpy as np
from PIL import Image
import io
import cv2
from skimage.metrics import structural_similarity as ssim

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CanaryEvaluator:
    def __init__(
        self,
        base_url: str,
        canary_url: str,
        num_requests: int,
        concurrency: int,
        styles: List[str],
        test_images_dir: str,
        evaluation_threshold: float = 0.95
    ):
        self.base_url = base_url
        self.canary_url = canary_url
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.styles = styles
        self.test_images_dir = test_images_dir
        self.evaluation_threshold = evaluation_threshold
        self.results: List[Dict[str, Any]] = []
        
    def load_test_image(self, image_path: str) -> bytes:
        """Load a test image from the specified path."""
        with open(image_path, 'rb') as f:
            return f.read()
    
    def calculate_image_similarity(self, img1: bytes, img2: bytes) -> float:
        """Calculate structural similarity between two images."""
        # Convert bytes to numpy arrays
        img1_array = np.array(Image.open(io.BytesIO(img1)))
        img2_array = np.array(Image.open(io.BytesIO(img2)))
        
        # Convert to grayscale if needed
        if len(img1_array.shape) == 3:
            img1_array = cv2.cvtColor(img1_array, cv2.COLOR_RGB2GRAY)
        if len(img2_array.shape) == 3:
            img2_array = cv2.cvtColor(img2_array, cv2.COLOR_RGB2GRAY)
        
        # Calculate SSIM
        return ssim(img1_array, img2_array)
    
    def make_comparison_request(self, image_path: str) -> Dict[str, Any]:
        """Make transform requests to both production and canary endpoints."""
        style = random.choice(self.styles)
        image_data = self.load_test_image(image_path)
        
        start_time = time.time()
        try:
            # Request to production
            prod_response = requests.post(
                f"{self.base_url}/transform",
                files={"file": ("image.jpg", image_data)},
                data={"style": style},
                timeout=30
            )
            prod_response.raise_for_status()
            
            # Request to canary
            canary_response = requests.post(
                f"{self.canary_url}/transform",
                files={"file": ("image.jpg", image_data)},
                data={"style": style},
                timeout=30
            )
            canary_response.raise_for_status()
            
            # Calculate similarity
            similarity = self.calculate_image_similarity(
                prod_response.content,
                canary_response.content
            )
            
            end_time = time.time()
            latency = end_time - start_time
            
            return {
                "status_code": 200,
                "latency": latency,
                "style": style,
                "similarity": similarity,
                "success": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            end_time = time.time()
            latency = end_time - start_time
            
            return {
                "status_code": getattr(e, "response", None) and e.response.status_code or 500,
                "latency": latency,
                "style": style,
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def run_evaluation(self):
        """Run the canary evaluation with specified concurrency."""
        test_images = [
            os.path.join(self.test_images_dir, f)
            for f in os.listdir(self.test_images_dir)
            if f.endswith(('.jpg', '.jpeg', '.png'))
        ]
        
        if not test_images:
            raise ValueError(f"No test images found in {self.test_images_dir}")
        
        logger.info(f"Starting canary evaluation with {self.num_requests} requests, {self.concurrency} concurrent workers")
        
        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = []
            for _ in range(self.num_requests):
                image_path = random.choice(test_images)
                futures.append(executor.submit(self.make_comparison_request, image_path))
            
            for future in futures:
                self.results.append(future.result())
        
        self.analyze_results()
    
    def analyze_results(self):
        """Analyze and log the canary evaluation results."""
        successful_requests = [r for r in self.results if r["success"]]
        failed_requests = [r for r in self.results if not r["success"]]
        
        total_requests = len(self.results)
        success_rate = len(successful_requests) / total_requests * 100
        
        similarities = [r["similarity"] for r in successful_requests]
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0
        
        # Group results by style
        style_results = {}
        for style in self.styles:
            style_requests = [r for r in successful_requests if r["style"] == style]
            style_similarities = [r["similarity"] for r in style_requests]
            style_results[style] = {
                "count": len(style_requests),
                "avg_similarity": sum(style_similarities) / len(style_similarities) if style_similarities else 0
            }
        
        # Save detailed results
        results_dir = "canary_evaluation_results"
        os.makedirs(results_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(results_dir, f"canary_evaluation_{timestamp}.json")
        
        with open(results_file, 'w') as f:
            json.dump({
                "summary": {
                    "total_requests": total_requests,
                    "success_rate": success_rate,
                    "avg_similarity": avg_similarity,
                    "evaluation_threshold": self.evaluation_threshold,
                    "passed_evaluation": avg_similarity >= self.evaluation_threshold,
                    "failed_requests": len(failed_requests)
                },
                "style_results": style_results,
                "detailed_results": self.results
            }, f, indent=2)
        
        # Log summary
        logger.info("\nCanary Evaluation Results Summary:")
        logger.info(f"Total Requests: {total_requests}")
        logger.info(f"Success Rate: {success_rate:.2f}%")
        logger.info(f"Average Similarity: {avg_similarity:.3f}")
        logger.info(f"Evaluation Threshold: {self.evaluation_threshold}")
        logger.info(f"Passed Evaluation: {avg_similarity >= self.evaluation_threshold}")
        logger.info(f"Failed Requests: {len(failed_requests)}")
        logger.info("\nResults by Style:")
        for style, stats in style_results.items():
            logger.info(f"{style}: {stats['count']} requests, avg similarity: {stats['avg_similarity']:.3f}")
        logger.info(f"\nDetailed results saved to: {results_file}")

def main():
    parser = argparse.ArgumentParser(description="Evaluate canary deployment of style transfer API")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of production API")
    parser.add_argument("--canary-url", default="http://localhost:8001", help="Base URL of canary API")
    parser.add_argument("--num-requests", type=int, default=100, help="Number of requests to make")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent requests")
    parser.add_argument("--styles", nargs="+", default=["starry_night", "mona_lisa"], help="Styles to test")
    parser.add_argument("--test-images-dir", default="test_images", help="Directory containing test images")
    parser.add_argument("--evaluation-threshold", type=float, default=0.95, help="Similarity threshold for evaluation")
    
    args = parser.parse_args()
    
    evaluator = CanaryEvaluator(
        base_url=args.base_url,
        canary_url=args.canary_url,
        num_requests=args.num_requests,
        concurrency=args.concurrency,
        styles=args.styles,
        test_images_dir=args.test_images_dir,
        evaluation_threshold=args.evaluation_threshold
    )
    
    evaluator.run_evaluation()

if __name__ == "__main__":
    main() 