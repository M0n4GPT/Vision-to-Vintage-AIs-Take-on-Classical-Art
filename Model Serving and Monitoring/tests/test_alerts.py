import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

def test_high_error_rate():
    """Test HighErrorRate alert by sending requests that will fail"""
    logger.info("Testing HighErrorRate alert...")
    
    # Send multiple requests with invalid parameters to trigger 500 errors
    for _ in range(20):
        try:
            # Send a request to a non-existent endpoint to trigger 500 error
            response = requests.post(
                f"{BASE_URL}/nonexistent",
                json={"invalid": "data"}
            )
            logger.info(f"Error rate test response: {response.status_code}")
        except Exception as e:
            logger.error(f"Error in error rate test: {e}")
        time.sleep(0.5)

def test_high_latency():
    """Test HighLatency alert by sending large images"""
    logger.info("Testing HighLatency alert...")
    
    # Create a large random image (2MB)
    large_image = np.random.randint(0, 255, (2000, 2000, 3), dtype=np.uint8)
    img = Image.fromarray(large_image)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=95)
    img_byte_arr = img_byte_arr.getvalue()
    
    for _ in range(10):
        try:
            response = requests.post(
                f"{BASE_URL}/transform",
                files={"file": ("large_image.jpg", img_byte_arr)},
                data={"style": "vangogh"}
            )
            logger.info(f"Latency test response: {response.status_code}")
        except Exception as e:
            logger.error(f"Error in latency test: {e}")
        time.sleep(1)

def test_too_many_requests():
    """Test TooManyRequestsInProgress alert by sending concurrent requests"""
    logger.info("Testing TooManyRequestsInProgress alert...")
    
    def send_request():
        try:
            # Create a small test image
            test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
            img = Image.fromarray(test_image)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            response = requests.post(
                f"{BASE_URL}/transform",
                files={"file": ("test.jpg", img_byte_arr)},
                data={"style": "vangogh"}
            )
            return response.status_code
        except Exception as e:
            logger.error(f"Error in concurrent request test: {e}")
            return None

    # Send 20 concurrent requests (increased from 15)
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(send_request) for _ in range(20)]
        for future in futures:
            future.result()

def main():
    logger.info("Starting alert tests...")
    
    # Run each test with a delay between them
    test_high_error_rate()
    time.sleep(15)  # Increased wait time for metrics collection
    
    test_high_latency()
    time.sleep(15)
    
    test_too_many_requests()
    time.sleep(15)
    
    logger.info("Alert tests completed. Check Prometheus and Grafana for alerts.")

if __name__ == "__main__":
    main() 