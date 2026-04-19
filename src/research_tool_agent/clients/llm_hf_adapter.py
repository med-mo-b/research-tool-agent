from collections.abc import Callable, Sequence
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from ..config import settings


class ChatHuggingFaceAgentCompat(ChatHuggingFace):
    """ChatHuggingFace compatible with LangChain agents using ToolStrategy structured output.

    LangChain's agent passes ``tool_choice="any"`` together with multiple tools; the
    stock ``ChatHuggingFace.bind_tools`` rejects any non-``None`` ``tool_choice`` unless
    exactly one tool is bound. Clearing ``tool_choice`` when multiple tools are present
    matches the library's allowed multi-tool path.
    """

    def bind_tools(
        self,
        tools: Sequence[dict[str, Any] | type | Callable[..., Any] | BaseTool],
        *,
        tool_choice: dict[str, Any] | str | bool | None = None,
        **kwargs: Any,
    ) -> Runnable[Any, Any]:
        """Bind tools; drop ``tool_choice`` when multiple tools would trigger HF's guard."""
        tool_list = list(tools) if tools is not None else []
        if len(tool_list) > 1 and tool_choice is not None and tool_choice:
            tool_choice = None
        return super().bind_tools(tools, tool_choice=tool_choice, **kwargs)


class HuggingFaceLLMAdapter:
    """Provides a Hugging Face Inference chat model behind ``LLMPort``."""

    def get_model(self) -> BaseChatModel:
        """Return a chat model for the configured Hugging Face endpoint."""
        llm = HuggingFaceEndpoint(
            repo_id=settings.model_id,
            huggingfacehub_api_token=settings.hf_token,
            task="text-generation",
            max_new_tokens=settings.llm_max_new_tokens,
            temperature=settings.llm_temperature,
            do_sample=settings.llm_do_sample,
            top_p=settings.llm_top_p,
        )
        return ChatHuggingFaceAgentCompat(llm=llm)
