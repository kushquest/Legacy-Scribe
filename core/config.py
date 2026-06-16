import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    DEFAULT_MODEL = "gemini-1.5-flash" # Default to stable flash if dynamic fails

    @classmethod
    def get_available_gemini_models(cls) -> list:
        """Dynamically fetch available Gemini models from Vertex AI."""
        try:
            from google import genai
            from google.auth import default
            
            credentials, project = default()
            client = genai.Client(
                vertexai=True, 
                project=cls.GOOGLE_CLOUD_PROJECT, 
                location=cls.GOOGLE_CLOUD_LOCATION,
                credentials=credentials
            )
            
            available = []
            for m in client.models.list():
                name = m.name
                if 'gemini' in name.lower() and 'embedding' not in name.lower():
                    display_name = name.split('/')[-1]
                    available.append(display_name)
            
            available = list(set(available))
            # Sort: Pro/Ultra first, then Flash, then older versions
            available.sort(key=lambda name: (
                'pro' not in name.lower(), 
                'flash' not in name.lower(), 
                name
            ))
            return available if available else [cls.DEFAULT_MODEL, 'gemini-1.5-pro']
        except Exception as e:
            print(f"⚠️ Could not fetch Gemini model list: {e}")
            return [cls.DEFAULT_MODEL, 'gemini-1.5-pro']
