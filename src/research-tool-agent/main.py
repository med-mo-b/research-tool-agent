from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.agents import create_agent
from config import settings

def get_model() -> ChatHuggingFace:
    model = HuggingFaceEndpoint(
        name=settings.model_id,
        huggingfacehub_api_token=settings.hf_token,
        task="text-generation",
        max_new_tokens=512,
        do_sample=False
    )
    return ChatHuggingFace(llm=model)

def main():
    print("Agent starting...") 
    model = get_model()
    
    agent = create_agent(
        model,
        tools=[], # Keine Tools, nur reiner Chat-Loop zum Testen
        system_prompt="Du bist ein hilfreicher deutscher Forschungsassistent."
    )
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Hallo! Kannst du mich bei Recherchen helfen?"}]
    })
    
    print("\n--- Agent Antwort ---")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
