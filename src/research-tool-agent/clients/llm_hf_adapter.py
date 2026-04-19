from config import settings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


class HuggingFaceLLMAdapter:
    def get_model(self) -> BaseChatModel:
        llm = HuggingFaceEndpoint(
            repo_id=settings.model_id,
            huggingfacehub_api_token=settings.hf_token,
            task="text-generation",
            max_new_tokens=1024,
            temperature=0.8,
            do_sample=True,
            top_p=0.9,
        )
        return ChatHuggingFace(llm=llm)
