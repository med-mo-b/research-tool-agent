# Research Tool Agent

A modular AI agent built with LangChain and LangGraph capable of researching current information on the web. It currently uses free Hugging Face Inference (e.g., Qwen models) and follows a port-adapter architecture for maximum LLM provider interchangeability.

## Architecture

The project follows modern Python practices (including a `src` layout and `uv` as the package manager) and strictly separates infrastructure from business logic:

- **Port-Adapter (Hexagonal)**: The LLM is abstracted via the `LLMPort` protocol. The adapter (e.g., `HuggingFaceLLMAdapter`) can be easily swapped for on-premise (Ollama, vLLM) or cloud models (OpenAI, Anthropic) without modifying the agent logic.
- **Tools as Capabilities**: Tools (like web search) are implemented as simple, declarative `@tool` functions. They extend the agent's "toolbox" without interfering with the core architecture.
- **Configuration**: All secrets and environment variables are managed centrally in `config.py` using `pydantic-settings`.

```text
src/research-tool-agent/
├── clients/                # Port-Adapters for LLMs
│   ├── __init__.py         # Factory function (Dependency Injection)
│   ├── llm_port.py         # Protocol (Interface)
│   └── llm_hf_adapter.py   # Concrete Adapter (HuggingFace)
├── tools/                  # LangChain Tools (Agent capabilities)
│   ├── __init__.py
│   └── web_search.py       # DuckDuckGo Web Search
├── config.py               # Pydantic BaseSettings
└── main.py                 # Agent setup & CLI Entry-Point
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd research-tool-agent
   ```

2. **Install dependencies (using [uv](https://github.com/astral-sh/uv)):**
   ```bash
   uv sync
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   HF_TOKEN=hf_your_huggingface_token_here
   MODEL_ID=model_of_your_choice
   LLM_PROVIDER=huggingface
   ```

## Usage

Start the agent via the terminal:

```bash
uv run python -m research_tool_agent.main
```

The agent uses the ReAct loop (Reason -> Act -> Observe): It decides autonomously based on your query whether it needs to call the `web_search_ddg` tool to fetch current data or if it can answer directly from its training knowledge.

## Roadmap

This project serves as a learning and reference implementation for advanced agent patterns:

- [x] **Phase 1:** Basic LangChain agent architecture & Port-Adapter setup
- [ ] **Phase 2:** Tool expansion (Calculator, File-Reader), Structured Output & Tool Error Handling
- [ ] **Phase 3:** Migration to LangGraph (Stateful Workflows, Branching, Checkpointing)
- [ ] **Phase 4:** Agentic RAG (Iterative Retrieval, Verifier, Confidence Gates)