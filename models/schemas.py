from pydantic import BaseModel, Field
from typing import List, Optional

class CodeAnalysis(BaseModel):
    logic_summary: str = Field(description="High-level summary of the legacy code logic.")
    security_vulnerabilities: List[str] = Field(description="List of potential security risks.")
    modern_architecture_suggestion: str = Field(description="Recommendation for modernizing this specific logic.")
    refactored_code_snippet: str = Field(description="Modern Python/FastAPI equivalent of the legacy logic.")
    estimated_effort_hours: int = Field(description="Estimated developer hours required for full modernization.")
    modernization_cost_estimate: float = Field(description="Estimated cost in USD for the modernization effort.")
    potential_annual_savings: float = Field(description="Estimated annual savings in USD after modernization (e.g., cloud efficiency, maintenance).")

class ModernizationReport(BaseModel):
    original_code: str
    analysis: CodeAnalysis
    timestamp: str
