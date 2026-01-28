from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatMessage(BaseModel):
    sender: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str
    confidence: Optional[float] = None
    sources: Optional[List[str]] = None

# Example for streaming response (if used)
class ChatStreamChunk(BaseModel):
    chunk: str
    done: bool = False