"""
Pydantic models for structured AI output.

ClaimAnalysis is used as the response schema for Gemini
to enforce consistent JSON output.
"""

from pydantic import BaseModel, Field


class ClaimAnalysis(BaseModel):
    """Schema for structured claim analysis returned by AI."""

    client_name: str | None = Field(
        default=None,
        description="Full name of the client/claimant extracted from text",
    )
    accident_date: str | None = Field(
        default=None,
        description="Date of the accident/incident (any recognizable format)",
    )
    claim_type: str = Field(
        default="Other",
        description='Type of claim: "Car Accident", "Medical", "Property Damage", "Workplace Injury", "Other"',
    )
    damage_estimation: float | None = Field(
        default=None,
        description="Estimated damage amount as a number (no currency symbols)",
    )
    ai_summary: str = Field(
        description="Brief 2-3 sentence summary of the claim",
    )
    suggested_status: str = Field(
        default="Pending",
        description='Suggested status: "Pending", "Approved", or "Requires Human Review"',
    )
