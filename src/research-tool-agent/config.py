from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env")

    hf_token: str = Field(..., description="The token for the Hugging Face API")
    model_id: str = Field(..., description="The ID of the model to use")

    llm_provider: str = Field(default="huggingface", description="The provider of the LLM")
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()