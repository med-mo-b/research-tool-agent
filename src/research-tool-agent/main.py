from clients import get_llm_client
from config import settings
from langchain.agents import create_agent
from tools import web_search_ddg


def main():
    print("Initializing Research Agent...")

    llm_client = get_llm_client(settings.llm_provider)
    model = llm_client.get_model()

    agent = create_agent(
        model,
        tools=[web_search_ddg],
        system_prompt=(
            "You are a helpful research assistant."
            "If you don't know something or need current data, use your search tool."
            "Always cite the URLs you found."
        )
    )
    query = "What are the latest news about Anthropic?"

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }
    )

    print("\n--- Agent Response ---")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
