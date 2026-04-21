# Research Tool Agent

A modular AI agent built with LangChain and LangGraph capable of researching current information on the web. It uses free Hugging Face Inference (e.g., Qwen models) and follows a port-adapter architecture for maximum LLM provider interchangeability.

## Architecture

The project follows modern Python practices (including a `src` layout and `uv` as the package manager) and strictly separates infrastructure from business logic:

- **Port-Adapter (Hexagonal)**: The LLM is abstracted via the `LLMPort` protocol. The adapter (e.g., `HuggingFaceLLMAdapter`) can be easily swapped for on-premise (Ollama, vLLM) or cloud models (OpenAI, Anthropic) without modifying the agent logic.
- **Tools as Capabilities**: Tools are implemented as simple, declarative `@tool` functions and extend the agent's capabilities without interfering with the core architecture.
- **Middleware**: The agent uses LangChain middleware for a **dynamic system prompt** (`@dynamic_prompt`, tuned by runtime context) and **tool error handling** (`wrap_tool_call`), so failed tools return a clear `ToolMessage` instead of aborting the run.
- **Runtime context**: Each chat turn passes an `AgentContext` (e.g. `user_role`: `user` | `expert` | `beginner`) into `agent.stream(...)`, which adjusts the system instructions without stuffing a static `SystemMessage` into the message list.
- **Runtime tool registration (goal)**: The project should move toward **runtime tool registration** (dynamic tool sets exposed per model turn, e.g. via LangChain middleware such as `wrap_model_call` / `wrap_tool_call`) instead of relying only on a **static** tool list fixed at agent construction time. That better supports MCP server discovery, lazy connections, and per-session or per-tenant tool catalogs without overloading the model with every possible tool upfront.
- **Configuration**: All secrets and environment variables are managed centrally in `config.py` using `pydantic-settings`.
- **CLI via Typer**: The user interface is a dedicated `cli/` sub-package, fully decoupled from the agent logic. New commands can be added without touching existing code.

```text
src/research_tool_agent/
├── cli/                        # Typer CLI (user interface layer)
│   ├── __init__.py             # Central app + sub-command registration
│   └── commands/
│       ├── __init__.py
│       └── chat.py             # `research-agent chat start` command
├── clients/                    # Port-Adapters for LLMs
│   ├── __init__.py             # Factory function (Dependency Injection)
│   ├── llm_port.py             # Protocol (Interface)
│   └── llm_hf_adapter.py      # Concrete Adapter (HuggingFace)
├── middleware/                 # Agent middleware (errors, prompts)
│   └── tool_error_handler.py
├── prompts/                    # Dynamic system prompt middleware
│   ├── __init__.py
│   └── system.py
├── schemas/                    # Structured output + runtime context types
│   ├── context.py              # AgentContext (e.g. user_role)
│   └── responses.py            # ResearchResponse (Pydantic)
├── tools/                      # LangChain Tools (Agent capabilities)
│   ├── __init__.py
│   ├── calculator.py           # Math expression evaluator
│   ├── file_reader.py          # Local file reader
│   └── web_search.py           # DuckDuckGo Web Search
├── config.py                   # Pydantic BaseSettings
└── main.py                     # Dev entrypoint fallback
```

## Setup & Installation

**1. Clone the repository:**
```bash
git clone <your-repo-url>
cd research-tool-agent
```

**2. Install dependencies (using [uv](https://github.com/astral-sh/uv)):**
```bash
uv sync
```

**3. Configure environment variables:**

Create a `.env` file in the project root:
```env
HF_TOKEN=hf_your_huggingface_token_here
MODEL_ID=model_of_your_choice
LLM_PROVIDER=huggingface
```

## Usage

Start the agent in interactive chat mode:

```bash
uv run research-agent chat start
```

Enable structured JSON output (answer + sources + tools used):

```bash
uv run research-agent chat start --structured
```

Adjust the assistant style with a **role** (`user` is the default; `expert` adds more technical depth, `beginner` favors simple explanations):

```bash
uv run research-agent chat start --role expert
uv run research-agent chat start -r beginner
```

Combine flags as needed, for example:

```bash
uv run research-agent chat start --structured --role expert
```

Show all available commands:

```bash
uv run research-agent --help
```

The agent uses the ReAct loop (Reason → Act → Observe): it decides autonomously whether to call a tool or answer directly from its training knowledge. Active tool calls are shown inline during streaming:

```
You: What is the current weather in Berlin?
Agent: [Using tool: web_search_ddg]... The current weather in Berlin is ...
```

## Tools

Today, tools are wired into the agent as a static set at startup. The intended direction is **runtime tool registration** (see Architecture) so tools can be added or narrowed after MCP `list_tools`, user-enabled integrations, or routing logic.

| Tool | Description |
|------|-------------|
| `web_search_ddg` | Searches the web via DuckDuckGo, returns titles, snippets and URLs |
| `calculator` | Evaluates mathematical expressions safely via `eval` with restricted builtins |
| `file_reader` | Reads local text files (truncated at 2000 characters) |

## Roadmap

- [x] **Phase 1:** Basic LangChain agent architecture & Port-Adapter setup
- [x] **Phase 1.5:** Modular CLI via Typer (`cli/commands/` structure)
- [x] **Phase 2:** Structured output (`ResearchResponse` / `--structured`) & tool error handling middleware
- [ ] **Runtime tool registration:** Adopt dynamic tool binding (middleware / per-invocation tool sets) for MCP and evolving catalogs instead of only static `tools=[...]` at agent creation
- [ ] **Minimal MCP server (3 tools):** Ship or integrate a small reference MCP process exposing exactly three tools (e.g. ping/echo, simple lookup, and one domain-specific helper) to exercise `list_tools`, connection lifecycle, and runtime registration end-to-end
- [ ] **Phase 3:** Migration to LangGraph (Stateful Workflows, Branching, Checkpointing)
- [ ] **Phase 4:** Agentic RAG (Iterative Retrieval, Verifier, Confidence Gates)