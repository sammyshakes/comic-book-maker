import requests
import json
import time
import os
from PIL import Image
from io import BytesIO

API_KEY = "37e209ef799f547d4363ac2a190ef723eff260f8353c3ef9c1ffb2021a75fa43"  # Replace with your actual API key

def check_task_status(task_id):
    url = "https://api.midjourneyapi.xyz/mj/v2/fetch"
    headers = {
        "X-API-KEY": API_KEY
    }
    data = {
        "task_id": task_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Error: {response.status_code}",
            "response_text": response.text
        }

def save_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(filename)
        return True
    return False

def save_metadata(metadata, filename):
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=4)

# Read task IDs from file
with open('task_ids.txt', 'r') as f:
    tasks = dict(line.strip().split(': ') for line in f)

# Create a directory to save images and metadata
os.makedirs("generated_images", exist_ok=True)

# Check status for each task with retries
for name, task_id in tasks.items():
    print(f"Checking status for {name}:")
    attempts = 5
    status = None
    for attempt in range(attempts):
        status = check_task_status(task_id)
        if 'error' not in status:
            break
        print(f"Attempt {attempt + 1}/{attempts} failed: {status['error']}, {status['response_text']}")
        time.sleep(10)  # Wait before retrying
    
    print(json.dumps(status, indent=2))
    
    if status.get('status') == 'finished':
        image_url = status['task_result']['image_url']
        filename = f"generated_images/{name.replace(' ', '_')}.png"
        if save_image(image_url, filename):
            print(f"Image for {name} saved as {filename}")
            # Save metadata
            metadata = {
                "task_id": task_id,
                "name": name,
                "status_response": status
            }
            metadata_filename = f"generated_images/{name.replace(' ', '_')}_metadata.json"
            save_metadata(metadata, metadata_filename)
            print(f"Metadata for {name} saved as {metadata_filename}")
        else:
            print(f"Failed to save image for {name}")
    else:
        print(f"Task for {name} is not finished yet or failed.")

    print()
