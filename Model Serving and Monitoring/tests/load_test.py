import requests
import time
import logging
import numpy as np
from PIL import Image
import io
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import json
from datetime import datetime
from pathlib import Path
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"  # Always use port 8000
RESULTS_DIR = "load_test_results"

def ensure_server_running() -> bool:
    """Ensure the FastAPI server is running"""
    try:
        # Start services using services.sh
        subprocess.run(["./scripts/services.sh", "start"], check=True)
        time.sleep(5)  # Wait for server to start
        return True
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        return False

class LoadTest:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "scenarios": [],
            "summary": {}
        }
        os.makedirs(RESULTS_DIR, exist_ok=True)

    def create_test_image(self, size: tuple = (224, 224)) -> bytes:
        """Create a test image of specified size"""
        image = np.random.randint(0, 255, (*size, 3), dtype=np.uint8)
        img = Image.fromarray(image)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()

    def test_single_request(self, style: str, image_size: tuple = (224, 224)) -> Dict[str, Any]:
        """Test a single request with specified parameters"""
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/transform",
                files={"content_image": ("test.jpg", self.create_test_image(image_size))},
                data={"style_name": style}
            )
            latency = time.time() - start_time
            
            return {
                "status_code": response.status_code,
                "latency": latency,
                "style": style,
                "image_size": image_size,
                "success": response.status_code == 200
            }
        except Exception as e:
            logger.error(f"Error in single request test: {e}")
            return {
                "status_code": 500,
                "latency": 0,
                "style": style,
                "image_size": image_size,
                "success": False,
                "error": str(e)
            }

    def test_concurrent_requests(self, num_requests: int, style: str) -> List[Dict[str, Any]]:
        """Test multiple concurrent requests"""
        results = []
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(self.test_single_request, style) for _ in range(num_requests)]
            for future in futures:
                results.append(future.result())
        return results

    def test_different_image_sizes(self) -> List[Dict[str, Any]]:
        """Test with different image sizes"""
        sizes = [(224, 224), (512, 512), (1024, 1024), (2048, 2048)]
        results = []
        for size in sizes:
            result = self.test_single_request("starry_night", size)
            results.append(result)
        return results

    def test_all_styles(self) -> List[Dict[str, Any]]:
        """Test with all available styles"""
        # Get available styles
        try:
            response = requests.get(f"{BASE_URL}/styles")
            styles = response.json()
        except Exception as e:
            logger.error(f"Error getting styles: {e}")
            styles = ["starry_night"]  # Fallback to default style

        results = []
        for style in styles:
            result = self.test_single_request(style)
            results.append(result)
        return results

    def run_load_test(self):
        """Run comprehensive load test"""
        logger.info("Starting comprehensive load test...")

        # Test 1: Basic functionality
        logger.info("Testing basic functionality...")
        basic_results = self.test_single_request("starry_night")
        self.results["scenarios"].append({
            "name": "basic_functionality",
            "results": basic_results
        })

        # Test 2: Different image sizes
        logger.info("Testing different image sizes...")
        size_results = self.test_different_image_sizes()
        self.results["scenarios"].append({
            "name": "different_image_sizes",
            "results": size_results
        })

        # Test 3: All styles
        logger.info("Testing all styles...")
        style_results = self.test_all_styles()
        self.results["scenarios"].append({
            "name": "all_styles",
            "results": style_results
        })

        # Test 4: Concurrent requests
        logger.info("Testing concurrent requests...")
        concurrent_results = self.test_concurrent_requests(10, "starry_night")
        self.results["scenarios"].append({
            "name": "concurrent_requests",
            "results": concurrent_results
        })

        # Calculate summary statistics
        self.calculate_summary()
        
        # Save results
        self.save_results()

    def calculate_summary(self):
        """Calculate summary statistics from test results"""
        all_latencies = []
        success_count = 0
        total_count = 0

        for scenario in self.results["scenarios"]:
            for result in scenario["results"]:
                if isinstance(result, dict):  # Handle both single and list results
                    if result.get("success"):
                        success_count += 1
                        all_latencies.append(result.get("latency", 0))
                    total_count += 1

        self.results["summary"] = {
            "total_requests": total_count,
            "successful_requests": success_count,
            "success_rate": (success_count / total_count * 100) if total_count > 0 else 0,
            "average_latency": np.mean(all_latencies) if all_latencies else 0,
            "median_latency": np.median(all_latencies) if all_latencies else 0,
            "p95_latency": np.percentile(all_latencies, 95) if all_latencies else 0,
            "p99_latency": np.percentile(all_latencies, 99) if all_latencies else 0
        }

    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(RESULTS_DIR, f"load_test_results_{timestamp}.json")
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"Results saved to {filename}")
        logger.info("\nTest Summary:")
        logger.info(f"Total Requests: {self.results['summary']['total_requests']}")
        logger.info(f"Success Rate: {self.results['summary']['success_rate']:.2f}%")
        logger.info(f"Average Latency: {self.results['summary']['average_latency']*1000:.2f}ms")
        logger.info(f"P95 Latency: {self.results['summary']['p95_latency']*1000:.2f}ms")

def main():
    # Ensure server is running before starting tests
    if not ensure_server_running():
        logger.error("Failed to start server, aborting tests")
        return
    
    load_test = LoadTest()
    load_test.run_load_test()

if __name__ == "__main__":
    main() 