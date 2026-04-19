from .llm_port import LLMPort
from .llm_hf_adapter import HuggingFaceLLMAdapter

def get_llm_client(provider: str) -> LLMPort:
    if provider == "huggingface":
        return HuggingFaceLLMAdapter()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

__all__ = ["get_llm_client"]