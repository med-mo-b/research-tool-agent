from langchain.agents.middleware import ModelRequest, dynamic_prompt

BASE_PROMPT = (
    "You are a highly capable research assistant. "
    "You have access to tools for web searching, calculating math expressions, and reading local files. "
    "Use the tools whenever necessary to answer accurately. "
    "If you use the web search tool, always cite the URLs you found. "
    "If you read a file, summarize its content clearly."
)


@dynamic_prompt
def system_prompt(request: ModelRequest) -> str:
    """Generates system prompt dynamically based on user role."""
    ctx = request.runtime.context
    user_role = getattr(ctx, "user_role", "user") if ctx is not None else "user"

    if user_role == "expert":
        return BASE_PROMPT + " Provide detailed, technical responses with sources."
    if user_role == "beginner":
        return BASE_PROMPT + " Explain concepts simply and avoid jargon."
    return BASE_PROMPT
