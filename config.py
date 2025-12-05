import os

# Try to load from .env file if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use environment variables directly

# Check for token in various formats (case-sensitive)
api_token = os.getenv("Token") or os.getenv("token") or os.getenv("GITHUB_TOKEN")
