import typer
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.messages import HumanMessage

from ...clients import get_llm_client
from ...config import settings
from ...middleware import handle_tool_errors
from ...prompts import system_prompt
from ...schemas import AgentContext, ResearchResponse
from ...tools import web_search_ddg, calculator, file_reader

chat = typer.Typer()


@chat.command()
def start(
    structured: bool = typer.Option(
        False, "--structured", "-s", help="Enable structured JSON output"
    ),
    role: str = typer.Option(
        "user", "--role", "-r", help="User role: user | expert | beginner"
    ),
):
    """Start an interactive chat with the Research Agent."""
    typer.echo("Initializing Research Agent...")

    llm_client = get_llm_client(settings.llm_provider)
    model = llm_client.get_model()

    response_format = ToolStrategy(ResearchResponse) if structured else None

    agent = create_agent(
        model,
        tools=[web_search_ddg, calculator, file_reader],
        middleware=[system_prompt, handle_tool_errors],
        response_format=response_format,
        context_schema=AgentContext,
        name="research_assistant",
    )

    typer.echo(f"Agent is ready (role={role}). Type 'exit' or 'quit' to stop.\n")

    messages = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            typer.echo("Goodbye!")
            raise typer.Exit()

        if not user_input:
            continue

        messages.append(HumanMessage(content=user_input))

        print("Agent: ", end="", flush=True)

        final_chunk = None
        tool_calls_made = set()

        for chunk in agent.stream(
            {"messages": messages},
            context=AgentContext(user_role=role),
            stream_mode="values",
        ):
            final_chunk = chunk
            latest_message = chunk["messages"][-1]

            if hasattr(latest_message, "tool_calls") and latest_message.tool_calls:
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
                print(final_chunk["messages"][-1].content)

        print()
