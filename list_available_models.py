"""
Quick diagnostic script to list available Gemini models for your API key.
Run this to find which models you have access to.
"""

import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("ERROR: GOOGLE_API_KEY not found in .env file")
    exit(1)

try:
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)
    print("Configured Gemini API client.\n")
except Exception as e:
    print(f"ERROR: Could not configure Gemini client: {e}")
    exit(1)

# Try to list available models
try:
    print("Fetching available models...")
    models = genai.list_models()
    
    print("\n" + "="*70)
    print("AVAILABLE GEMINI MODELS FOR YOUR API KEY:")
    print("="*70 + "\n")
    
    for model in models:
        # Extract just the model name
        model_name = model.name  # e.g., "models/gemini-pro"
        display_name = model_name.replace("models/", "")
        
        # Check if it supports generateContent
        supports_generate = False
        if hasattr(model, "supported_generation_methods"):
            supports_generate = "generateContent" in model.supported_generation_methods
        
        status = "✓ Supports generateContent" if supports_generate else "✗ Does not support generateContent"
        print(f"{display_name:30s} {status}")
    
    print("\n" + "="*70)
    print("RECOMMENDED:")
    print("Set GEMINI_MODEL in .env to one of the model names above.")
    print("Example: GEMINI_MODEL=gemini-pro")
    print("="*70)

except Exception as e:
    print(f"ERROR while listing models: {e}")
    print("\nMake sure your API key has access to the Gemini API.")
    exit(1)
