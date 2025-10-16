from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access your API key
api_key = os.getenv("YOUTUBE_API_KEY")

print("Loaded API key:", api_key[:5] + "..." if api_key else "Missing key!")
