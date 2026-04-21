from dataclasses import dataclass

@dataclass
class AgentContext:
    user_role: str = "user"