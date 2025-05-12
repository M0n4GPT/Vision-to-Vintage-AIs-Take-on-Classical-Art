import requests
import time
import logging
import numpy as np
from PIL import Image
import io
from datetime import datetime, timedelta
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

class ModelDegradationTester:
    def __init__(self):
        self.success_count = 0
        self.total_count = 0
        self.latencies = []
        
    def create_test_image(self, size=(224, 224), noise_level=0.1):
        """Create a test image with controlled noise level"""
        base_image = np.random.randint(0, 255, (*size, 3), dtype=np.uint8)
        noise = np.random.normal(0, noise_level * 255, base_image.shape).astype(np.uint8)
        noisy_image = np.clip(base_image + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_image)
    
    def simulate_data_drift(self, iterations=10):
        """Simulate data drift by gradually increasing noise in images"""
        logger.info("Simulating data drift...")
        for i in range(iterations):
            noise_level = 0.1 + (i * 0.05)  # Gradually increase noise
            image = self.create_test_image(noise_level=noise_level)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            try:
                start_time = time.time()
                response = requests.post(
                    f"{BASE_URL}/transform",
                    files={"file": ("test.jpg", img_byte_arr)},
                    data={"style": "vangogh"}
                )
                latency = time.time() - start_time
                self.latencies.append(latency)
                
                if response.status_code == 200:
                    self.success_count += 1
                self.total_count += 1
                
                logger.info(f"Drift test {i+1}/{iterations} - Noise: {noise_level:.2f}, "
                          f"Latency: {latency:.2f}s, Status: {response.status_code}")
                
            except Exception as e:
                logger.error(f"Error in drift test: {e}")
            
            time.sleep(1)
    
    def simulate_latency_degradation(self, iterations=10):
        """Simulate latency degradation by sending large images"""
        logger.info("Simulating latency degradation...")
        for i in range(iterations):
            # Create increasingly larger images
            size = (224 + i*50, 224 + i*50)
            image = self.create_test_image(size=size)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr = img_byte_arr.getvalue()
            
            try:
                start_time = time.time()
                response = requests.post(
                    f"{BASE_URL}/transform",
                    files={"file": ("test.jpg", img_byte_arr)},
                    data={"style": "vangogh"}
                )
                latency = time.time() - start_time
                self.latencies.append(latency)
                
                if response.status_code == 200:
                    self.success_count += 1
                self.total_count += 1
                
                logger.info(f"Latency test {i+1}/{iterations} - Size: {size}, "
                          f"Latency: {latency:.2f}s, Status: {response.status_code}")
                
            except Exception as e:
                logger.error(f"Error in latency test: {e}")
            
            time.sleep(1)
    
    def simulate_accuracy_degradation(self, iterations=10):
        """Simulate accuracy degradation by sending corrupted images"""
        logger.info("Simulating accuracy degradation...")
        for i in range(iterations):
            # Create increasingly corrupted images
            image = self.create_test_image(noise_level=0.1 + (i * 0.1))
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=50 - (i * 3))
            img_byte_arr = img_byte_arr.getvalue()
            
            try:
                start_time = time.time()
                response = requests.post(
                    f"{BASE_URL}/transform",
                    files={"file": ("test.jpg", img_byte_arr)},
                    data={"style": "vangogh"}
                )
                latency = time.time() - start_time
                self.latencies.append(latency)
                
                if response.status_code == 200:
                    self.success_count += 1
                self.total_count += 1
                
                logger.info(f"Accuracy test {i+1}/{iterations} - Quality: {50 - (i * 3)}, "
                          f"Latency: {latency:.2f}s, Status: {response.status_code}")
                
            except Exception as e:
                logger.error(f"Error in accuracy test: {e}")
            
            time.sleep(1)
    
    def run_all_tests(self):
        """Run all degradation tests"""
        logger.info("Starting model degradation tests...")
        
        self.simulate_data_drift()
        time.sleep(5)
        
        self.simulate_latency_degradation()
        time.sleep(5)
        
        self.simulate_accuracy_degradation()
        
        # Print summary
        accuracy = (self.success_count / self.total_count) * 100 if self.total_count > 0 else 0
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        
        logger.info("\nTest Summary:")
        logger.info(f"Total requests: {self.total_count}")
        logger.info(f"Successful requests: {self.success_count}")
        logger.info(f"Accuracy: {accuracy:.2f}%")
        logger.info(f"Average latency: {avg_latency:.2f}s")
        
        logger.info("\nCheck Prometheus and Grafana for alerts...")

def main():
    tester = ModelDegradationTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 