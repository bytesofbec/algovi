from  dataclasses import dataclass
from typing import Any

@dataclass
class ExecutionStep:
    """
    Represents one step in the an algorithm's execution.
    """

    step_number: int
    state: Any
    action: str
    indices: list[int]
    description: str