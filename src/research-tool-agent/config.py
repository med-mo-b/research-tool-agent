from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from functools import lru_cache

@lru_cache
class Settings(BaseSettings):
    
    model_config = ConfigDict(env_file=".env")

    hf_token: str = Field(..., env="HUGGINGFACEHUB_ACCESS_TOKEN")
    model_id: str = Field(..., env="MODEL_ID")
    
    
settings = Settings()