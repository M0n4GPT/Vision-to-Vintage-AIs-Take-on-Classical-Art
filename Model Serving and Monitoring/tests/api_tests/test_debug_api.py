#!/usr/bin/env python
"""
Test the debug API service
"""
import requests
import json
import base64
from PIL import Image
import io
import os
import time

def test_upload(image_path):
    """Test uploading an image to debug service"""
    
    url = "http://localhost:8888/upload"
    
    print(f"Testing upload of {image_path}")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}")
        return
    
    # Print file info
    file_size = os.path.getsize(image_path)
    print(f"File size: {file_size} bytes")
    
    # Check if file seems to be a valid image
    try:
        with Image.open(image_path) as img:
            print(f"Image opened successfully: format={img.format}, mode={img.mode}, size={img.size}")
    except Exception as e:
        print(f"Warning: Could not open as image: {e}")
    
    # Read file bytes
    with open(image_path, 'rb') as f:
        content = f.read()
        
    # Print first bytes
    print(f"First bytes: {' '.join([f'{b:02x}' for b in content[:20]])}")
    
    # Upload the file
    try:
        print(f"Uploading to {url}...")
        
        files = {
            'file': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
        }
        
        response = requests.post(url, files=files)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("Response:")
                print(json.dumps(result, indent=2))
                
                # Save thumbnail if available
                if result.get('status') == 'success' and 'thumbnail' in result:
                    img_data = base64.b64decode(result['thumbnail'])
                    img = Image.open(io.BytesIO(img_data))
                    thumbnail_path = "thumbnail.jpg"
                    img.save(thumbnail_path)
                    print(f"Thumbnail saved to {thumbnail_path}")
            except Exception as e:
                print(f"Error parsing response: {e}")
                print(f"Raw response: {response.text[:100]}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Request error: {e}")
    

if __name__ == "__main__":
    test_image = "data/examples/test_image.jpg"
    test_upload(test_image) 