import os
from dotenv import load_dotenv, find_dotenv
import warnings
import requests
import json
import time

# Load environment variables (if using a .env file)
_ = load_dotenv(find_dotenv())

# OpenWebUI API URL
url = "http://ai.uaf.edu.pk/api/chat/completions"


# API Key (Store in .env or set manually)

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Get API key
api_key = os.getenv("OW_API_KEY")


# Headers with Authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"  # Add API key to headers
}

def llama(prompt, 
          model="llama3.2-vision:latest",  # Ensure this matches your model name in OpenWebUI
          temperature=0.7, 
          max_tokens=1024,
          verbose=False,
          url=url,
          headers=headers,
          base=2,  # Number of seconds to wait
          max_tries=3):
    
    if verbose:
        print(f"Prompt:\n{prompt}\n")
        print(f"Model: {model}")

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # Retry logic for handling downtime
    wait_seconds = [base**i for i in range(max_tries)]

    for num_tries in range(max_tries):
        try:
            response = requests.post(url, headers=headers, json=data)
            response_json = response.json()

            # Extract response text
            return response_json["choices"][0]["message"]["content"]
        
        except Exception as e:
            if response.status_code != 500:
                return response.json()

            print(f"Error: {e}")
            print(f"Response: {response}")
            print(f"Attempt {num_tries + 1} failed. Retrying in {wait_seconds[num_tries]} seconds...")
            time.sleep(wait_seconds[num_tries])
            
    print(f"Tried {max_tries} times but couldn't get a valid response.")
    return None