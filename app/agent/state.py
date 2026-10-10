from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    task: str
    messages: list[dict[str, Any]] = field(default_factory=list)

    turn: int = 0
    max_turns: int = 100
    

    files_changed: list[str] = field(default_factory=list)

    tests_run: bool = False
    tests_passed: bool | None = False