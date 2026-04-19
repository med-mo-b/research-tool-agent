from pydantic import BaseModel, Field

class ResearchResponse(BaseModel):
    """Schema for the final structured response of the agent."""
    answer: str = Field(description="The final answer to the user's question.")
    sources: list[str] = Field(description="List of URLs or file paths used to derive the answer.")
    tools_used: list[str] = Field(description="Names of the tools that were actually used.")