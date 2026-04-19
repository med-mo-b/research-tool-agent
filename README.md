# Research Tool Agent

A modular AI agent built with LangChain and LangGraph capable of researching current information on the web. It uses free Hugging Face Inference (e.g., Qwen models) and follows a port-adapter architecture for maximum LLM provider interchangeability.

## Architecture

The project follows modern Python practices (including a `src` layout and `uv` as the package manager) and strictly separates infrastructure from business logic:

- **Port-Adapter (Hexagonal)**: The LLM is abstracted via the `LLMPort` protocol. The adapter (e.g., `HuggingFaceLLMAdapter`) can be easily swapped for on-premise (Ollama, vLLM) or cloud models (OpenAI, Anthropic) without modifying the agent logic.
- **Tools as Capabilities**: Tools are implemented as simple, declarative `@tool` functions and extend the agent's capabilities without interfering with the core architecture.
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
├── prompts/                    # System prompts
│   └── system.py
├── schemas/                    # Pydantic response schemas
│   └── responses.py
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

| Tool | Description |
|------|-------------|
| `web_search_ddg` | Searches the web via DuckDuckGo, returns titles, snippets and URLs |
| `calculator` | Evaluates mathematical expressions safely via `eval` with restricted builtins |
| `file_reader` | Reads local text files (truncated at 2000 characters) |

## Roadmap

- [x] **Phase 1:** Basic LangChain agent architecture & Port-Adapter setup
- [x] **Phase 1.5:** Modular CLI via Typer (`cli/commands/` structure)
- [ ] **Phase 2:** Structured Output & Tool Error Handling
- [ ] **Phase 3:** Migration to LangGraph (Stateful Workflows, Branching, Checkpointing)
- [ ] **Phase 4:** Agentic RAG (Iterative Retrieval, Verifier, Confidence Gates)