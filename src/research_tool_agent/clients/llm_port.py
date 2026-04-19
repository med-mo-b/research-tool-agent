from typing import Protocol, runtime_checkable

from langchain_core.language_models.chat_models import BaseChatModel


@runtime_checkable
class LLMPort(Protocol):
    def get_model(self) -> BaseChatModel: ...
