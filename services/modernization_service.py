import os
import asyncio
import json
from google import genai
from google.auth import default
from google.oauth2 import service_account
import streamlit as st
from core.config import Config
from models.schemas import CodeAnalysis

class ModernizationService:
    def __init__(self):
        credentials = None
        project = None

        # Try loading credentials from Streamlit secrets (for deployment)
        if "gcp_service_account" in st.secrets:
            try:
                credentials = service_account.Credentials.from_service_account_info(
                    dict(st.secrets["gcp_service_account"])
                )
                project = st.secrets["gcp_service_account"].get("project_id")
            except Exception as e:
                print(f"⚠️ Failed to load credentials from Streamlit secrets: {e}")

        # Fallback to local Application Default Credentials (ADC)
        if not credentials:
            credentials, project = default()

        gcp_project = Config.GOOGLE_CLOUD_PROJECT or project

        self.client = genai.Client(
            vertexai=True,
            project=gcp_project,
            location=Config.GOOGLE_CLOUD_LOCATION,
            credentials=credentials
        )

    async def analyze_legacy_code(self, code: str, model_name: str = Config.DEFAULT_MODEL):
        yield "Initializing Legacy Scribe..."
        await asyncio.sleep(0.5)
        yield f"Using Engine: {model_name}..."
        await asyncio.sleep(0.5)
        yield "Deconstructing legacy syntax and state machine..."
        
        try:
            # Using native google-genai structured output
            response = self.client.models.generate_content(
                model=model_name,
                contents=f"Analyze this legacy asset and provide a modernization strategy with detailed cost/effort estimates:\n\n{code}",
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': CodeAnalysis,
                    'system_instruction': "You are an expert Legacy Modernization Agent. Your task is to transform legacy codebases and schemas into modern, scalable, cloud-native solutions. Analyze the provided legacy code/schema/logs and provide a comprehensive modernization strategy, refactored implementation, and realistic ROI metrics. For costs, assume a blended developer rate of $150/hr for modernization effort."
                }
            )
            
            # The SDK returns the parsed model directly if response_schema is provided
            # but sometimes we need to ensure it's converted to our local Pydantic model
            result = response.parsed
            if not result:
                # Fallback to manual parsing if .parsed is not available or failed
                result = CodeAnalysis.model_validate_json(response.text)
            
            yield result
        except Exception as e:
            yield f"ERROR_MODERNIZATION_PIPELINE: {str(e)}"
