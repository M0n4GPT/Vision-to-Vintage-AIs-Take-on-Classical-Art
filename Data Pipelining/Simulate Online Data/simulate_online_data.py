import requests
import os
import time
import random

CONTENT_DIR = "/mnt/project35/random_inputs/random_test"  # Or any artist folder
SERVER_URL = "http://129.114.25.100/"
SLEEP_INTERVAL = (5, 10)  # seconds

def simulate_request(image_path):
    files = {'file': open(image_path, 'rb')}
    try:
        response = requests.post(SERVER_URL, files=files)
        print(f"✅ Sent: {os.path.basename(image_path)} | Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending {image_path}: {e}")

if __name__ == "__main__":
    images = [os.path.join(CONTENT_DIR, f) for f in os.listdir(CONTENT_DIR) if f.endswith(".jpg")]
    random.shuffle(images)

    for img in images[:10]:  # Simulate 10 images
        simulate_request(img)
        time.sleep(random.randint(*SLEEP_INTERVAL))
