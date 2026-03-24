from pydantic import BaseModel, Field
from dataclasses import dataclass, field
from typing import Literal, TypedDict, List, Dict, Any, Optional

class AgentState(BaseModel):
    """
    State definition for agent workflow.
    """
    user_query: str
    context: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    status: Optional[str] = None

class InputState(BaseModel):
    """
    Input state for agent initialization.
    """
    query: str

class Router(BaseModel):
    """
    Router state for workflow branching.
    """
    route_type: Literal["general-query", "rag-search", "image-query", "additional-query", "guardrails", "hallucination-check"]

@dataclass
class GradeHallucinations:
    """
    State for hallucination grading.
    """
    score: float
    details: Optional[str] = None