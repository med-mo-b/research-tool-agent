from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.agents import create_agent
from config import settings

def get_model() -> ChatHuggingFace:
    llm_endpoint = HuggingFaceEndpoint(
        repo_id=settings.model_id,
        huggingfacehub_api_token=settings.hf_token,
        task="text-generation",
        max_new_tokens=1024,
        temperature=0.8,
        do_sample=True,
        top_p=0.9,
    )
    return ChatHuggingFace(llm=llm_endpoint)

def main():
    print("Agent starting...") 
    model = get_model()
    
    agent = create_agent(
        model,
        tools=[],
        system_prompt="You are a helpful assistant. Answer clearly and concisely."
    )
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Hello! Could you help me with some research?"}]
    })
    
    print("\n--- Agent Response ---")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
