from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env")

    hf_token: str = Field(..., description="The token for the Hugging Face API")
    model_id: str = Field(..., description="The ID of the model to use")

    llm_provider: str = Field(default="huggingface", description="The provider of the LLM")
    llm_temperature: float = Field(default=0.8, description="The temperature for the LLM")
    llm_top_p: float = Field(default=0.9, description="The top-p for the LLM")
    llm_max_new_tokens: int = Field(default=1024, description="The maximum number of new tokens for the LLM")
    llm_do_sample: bool = Field(default=True, description="Whether to sample from the LLM")
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()