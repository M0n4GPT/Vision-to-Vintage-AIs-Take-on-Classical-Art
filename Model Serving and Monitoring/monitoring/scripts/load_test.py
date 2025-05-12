import requests
import time
import random
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import json
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoadTester:
    def __init__(
        self,
        base_url: str,
        num_requests: int,
        concurrency: int,
        styles: List[str],
        test_images_dir: str
    ):
        self.base_url = base_url
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.styles = styles
        self.test_images_dir = test_images_dir
        self.results: List[Dict[str, Any]] = []
        
    def load_test_image(self, image_path: str) -> bytes:
        """Load a test image from the specified path."""
        with open(image_path, 'rb') as f:
            return f.read()
    
    def make_request(self, image_path: str) -> Dict[str, Any]:
        """Make a single transform request."""
        style = random.choice(self.styles)
        image_data = self.load_test_image(image_path)
        
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/transform",
                files={"file": ("image.jpg", image_data)},
                data={"style": style},
                timeout=30
            )
            response.raise_for_status()
            
            end_time = time.time()
            latency = end_time - start_time
            
            return {
                "status_code": response.status_code,
                "latency": latency,
                "style": style,
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
    
    def run_load_test(self):
        """Run the load test with specified concurrency."""
        test_images = [
            os.path.join(self.test_images_dir, f)
            for f in os.listdir(self.test_images_dir)
            if f.endswith(('.jpg', '.jpeg', '.png'))
        ]
        
        if not test_images:
            raise ValueError(f"No test images found in {self.test_images_dir}")
        
        logger.info(f"Starting load test with {self.num_requests} requests, {self.concurrency} concurrent workers")
        
        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = []
            for _ in range(self.num_requests):
                image_path = random.choice(test_images)
                futures.append(executor.submit(self.make_request, image_path))
            
            for future in futures:
                self.results.append(future.result())
        
        self.analyze_results()
    
    def analyze_results(self):
        """Analyze and log the load test results."""
        successful_requests = [r for r in self.results if r["success"]]
        failed_requests = [r for r in self.results if not r["success"]]
        
        total_requests = len(self.results)
        success_rate = len(successful_requests) / total_requests * 100
        
        latencies = [r["latency"] for r in successful_requests]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
        p99_latency = sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0
        
        # Group results by style
        style_results = {}
        for style in self.styles:
            style_requests = [r for r in successful_requests if r["style"] == style]
            style_latencies = [r["latency"] for r in style_requests]
            style_results[style] = {
                "count": len(style_requests),
                "avg_latency": sum(style_latencies) / len(style_latencies) if style_latencies else 0
            }
        
        # Save detailed results
        results_dir = "load_test_results"
        os.makedirs(results_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(results_dir, f"load_test_{timestamp}.json")
        
        with open(results_file, 'w') as f:
            json.dump({
                "summary": {
                    "total_requests": total_requests,
                    "success_rate": success_rate,
                    "avg_latency": avg_latency,
                    "p95_latency": p95_latency,
                    "p99_latency": p99_latency,
                    "failed_requests": len(failed_requests)
                },
                "style_results": style_results,
                "detailed_results": self.results
            }, f, indent=2)
        
        # Log summary
        logger.info("\nLoad Test Results Summary:")
        logger.info(f"Total Requests: {total_requests}")
        logger.info(f"Success Rate: {success_rate:.2f}%")
        logger.info(f"Average Latency: {avg_latency:.3f}s")
        logger.info(f"95th Percentile Latency: {p95_latency:.3f}s")
        logger.info(f"99th Percentile Latency: {p99_latency:.3f}s")
        logger.info(f"Failed Requests: {len(failed_requests)}")
        logger.info("\nResults by Style:")
        for style, stats in style_results.items():
            logger.info(f"{style}: {stats['count']} requests, avg latency: {stats['avg_latency']:.3f}s")
        logger.info(f"\nDetailed results saved to: {results_file}")

def main():
    parser = argparse.ArgumentParser(description="Load test the style transfer API")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--num-requests", type=int, default=100, help="Number of requests to make")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent requests")
    parser.add_argument("--styles", nargs="+", default=["starry_night", "mona_lisa"], help="Styles to test")
    parser.add_argument("--test-images-dir", default="test_images", help="Directory containing test images")
    
    args = parser.parse_args()
    
    load_tester = LoadTester(
        base_url=args.base_url,
        num_requests=args.num_requests,
        concurrency=args.concurrency,
        styles=args.styles,
        test_images_dir=args.test_images_dir
    )
    
    load_tester.run_load_test()

if __name__ == "__main__":
    main() 