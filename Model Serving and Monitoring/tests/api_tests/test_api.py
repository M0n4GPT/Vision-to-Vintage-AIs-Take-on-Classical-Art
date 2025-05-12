#!/usr/bin/env python
"""
Test script for the API endpoint using Python requests
"""
import sys
import requests
import json
from PIL import Image
import io
import base64

def test_transform(image_path, style_name):
    """
    Test the transform endpoint with the given image and style
    """
    # API endpoint
    url = "http://localhost:8000/transform"
    
    # Open the image file
    with open(image_path, 'rb') as img_file:
        # Create files payload
        files = {
            'content_image': (image_path, img_file, 'image/jpeg')
        }
        
        # Query parameters
        params = {
            'style_name': style_name
        }
        
        print(f"Sending request to {url} with style_name={style_name}")
        print(f"Using image: {image_path}")
        
        # Send POST request
        response = requests.post(url, params=params, files=files)
        
        # Print status code
        print(f"Response status code: {response.status_code}")
        
        # Save response to file
        with open('response.json', 'w') as f:
            f.write(response.text)
        print("Response saved to response.json")
        
        # If successful, save the image
        if response.status_code == 200:
            try:
                # Parse JSON response
                data = response.json()
                
                # If 'image' field exists, decode and save
                if 'image' in data:
                    img_data = base64.b64decode(data['image'])
                    result_img = Image.open(io.BytesIO(img_data))
                    result_path = f"result_{style_name}.png"
                    result_img.save(result_path)
                    print(f"Transformed image saved to {result_path}")
                else:
                    print("No image field in the response")
            except Exception as e:
                print(f"Error processing response: {e}")
        
        # Print response content for debugging
        try:
            pretty_json = json.dumps(response.json(), indent=2)
            print(f"Response content:\n{pretty_json}")
        except:
            print(f"Response content (not JSON):\n{response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_api.py <image_path> <style_name>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    style_name = sys.argv[2]
    
    test_transform(image_path, style_name) 