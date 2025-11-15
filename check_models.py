import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

# Get the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    
    print("Finding available models for your API key...")
    print("---------------------------------------------")
    
    try:
        for model in genai.list_models():
            # We only care about models that support the 'generateContent' method
            if 'generateContent' in model.supported_generation_methods:
                print(f"Model name: {model.name}")
                print(f"  Description: {model.description}\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please double-check that your GEMINI_API_KEY is correct and active.")
        
    print("---------------------------------------------")
    print("Please copy the 'Model name' (like 'models/gemini-pro') and paste it in the chat.")