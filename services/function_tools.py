from typing import List, Dict, Any, Callable
import json
from dataclasses import dataclass

@dataclass
class FunctionToolSchema:
    """
    Schema for function tool definition.
    """
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable