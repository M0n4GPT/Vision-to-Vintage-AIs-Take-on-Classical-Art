## What You Need to Do

**1. Define the Online Data Pipeline**
You should clearly define that your app already acts as an online inference service: 

1] The user uploads a content image.

2] The app stylizes it using a style transfer model.

3] The user is presented with multiple choices for artist prediction.

4] Based on their selection, feedback is given.


This is real-time data processing – you're simulating user interactions with stylized outputs.

**2. Simulate Online Data Requests**
To simulate production usage, you’ll write a script that:

1] Randomly picks content images from your existing dataset.

2] Sends them (via POST request) to your Flask app's upload endpoint (http://129.114.25.100/).

3] Mimics a user by triggering the POST and "guessing" from the artist options (this can be random or always correct).

4] Waits a few seconds between each request to simulate real usage over time.

```
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
```

**3. Clean and Preprocess (Mirror Your Transform Step)**
In the simulation script, if needed:

Resize or normalize the image before sending.

But since your app handles preprocessing internally via load_img, no need to replicate this unless you change the input format.


## How to Verify that it works!

**Step 1: Confirm the Web App Is Running**
Make sure your style transfer app is running at:
```cpp
http://129.114.25.100/
```

You should be able to open this URL in your browser and see the upload interface.

If not, start the web service container (likely with docker run or docker compose).

**Step 2: Confirm the Directory Exists**
SSH into your compute instance and run:

```bash
ls /mnt/project35/random_inputs/random_test
```

Make sure it contains at least 10 .jpg images. If not, upload a few test images to this folder.

**Step 3: Run the Simulation Script**
From your GitHub-cloned project directory on the instance:

```bash
cd ~/Vision-to-Vintage-AIs-Take-on-Classical-Art/Data\ Pipelining/Simulate\ Online\ Data
python3 simulate_online_data.py
```

You should see outputs like:

![image](https://github.com/user-attachments/assets/674b1511-106f-4233-b7bb-35bfca8c28c0)

If you get a Status: 200, it means the request was successfully received by the app.

**Step 4: Check Its Logs**

Once you have the name (e.g., web_container), run:

```bash
docker logs b1341baa8cc4
```

This will show the internal log messages from app.py — including when your simulate_online_data.py script sends requests. Look for:

POST requests being received

any errors or success messages

optionally, you can print() something in app.py upon successful stylization or image handling

![image](https://github.com/user-attachments/assets/fe878c72-b41c-49f8-a74b-373cf214e9c5)


