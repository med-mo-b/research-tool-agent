import typer
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

# Relative Imports (3 Punkte = gehe 3 Ebenen hoch zum Haupt-Package)
from ...clients import get_llm_client
from ...config import settings
from ...prompts.system import SYSTEM_PROMPT
from ...tools import web_search_ddg, calculator, file_reader
from ...schemas import ResearchResponse

chat = typer.Typer() 

@chat.command()
def start(
    structured: bool = typer.Option(False, "--structured", "-s", help="Enable structured JSON output")
):
    """Start an interactive chat with the Research Agent."""
    typer.echo("Initializing Research Agent...")
    
    llm_client = get_llm_client(settings.llm_provider)
    model = llm_client.get_model()

    response_format = ToolStrategy(ResearchResponse) if structured else None

    agent = create_agent(
        model,
        tools=[web_search_ddg, calculator, file_reader],
        system_prompt=SYSTEM_PROMPT,
        response_format=response_format,
    )

    typer.echo("Agent is ready. Type 'exit' or 'quit' to stop.\n")
    
    messages = []

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            typer.echo("Goodbye!")
            raise typer.Exit()
        
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        print("Agent: ", end="", flush=True)
        
        final_chunk = None
        tool_calls_made = set()

        for chunk in agent.stream(
            {"messages": messages}, 
            stream_mode="values"
        ):
            final_chunk = chunk
            latest_message = chunk["messages"][-1]

            if isinstance(latest_message, object) and hasattr(latest_message, 'tool_calls') and latest_message.tool_calls:
                for tc in latest_message.tool_calls:
                    if tc["name"] not in tool_calls_made:
                        print(f"[Using tool: {tc['name']}]...", end=" ", flush=True)
                        tool_calls_made.add(tc["name"])

        if final_chunk:
            messages = final_chunk["messages"]
            
            if structured and final_chunk.get("structured_response"):
                resp = final_chunk["structured_response"]
                print(f"\nAnswer: {resp.answer}")
                print(f"Sources: {resp.sources}")
                print(f"Tools used: {resp.tools_used}")
            else:
                final_ai_message = final_chunk["messages"][-1]
                print(final_ai_message.content)
        
        print()