import os

# Try to load from .env file if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use environment variables directly

# Check for token in various formats (handles different casing)
api_token = os.getenv("TOKEN")
