import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    DEFAULT_MODEL = "gemini-2.5-flash" # Hardcoded model requirement
