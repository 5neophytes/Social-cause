import cv2
import base64
import requests
import os
import json
from dotenv import load_dotenv

# Load the environment variable
load_dotenv()

# Get API key from .env file
api_key = os.getenv("OPENAI_API_KEY")

# Function to encode the image in base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to get advice and save the response to a JSON file
def get_advice(image_path):
    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze the graph I am providing you of my personal transactions in around 50 words"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        output = response.json()
        output_content = output['choices'][0]['message']['content']
        print(output_content)

        # Save response to a JSON file named after the image file
        image_name = os.path.basename(image_path).split('.')[0]  # Get the image name without extension
        json_filename = f"{image_name}.json"
        with open(json_filename, 'w') as json_file:
            json.dump(output_content, json_file, indent=4)
        
        return output_content
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# List of image paths to process
image_paths = [
    "C:/Users/satvi/Social-cause/DonutChart.png",
    "C:/Users/satvi/Social-cause/LineChart.png",
    "C:/Users/satvi/Social-cause/LineChart_CCFT.png",
    "C:/Users/satvi/Social-cause/BarChart.png",  # Add your additional images here
    "C:/Users/satvi/Social-cause/PieChart1.png",  # Replace with actual paths
    "C:/Users/satvi/Social-cause/PieChart2.png",
]

# Loop over each image and run the function
for image_path in image_paths:
    get_advice(image_path)
