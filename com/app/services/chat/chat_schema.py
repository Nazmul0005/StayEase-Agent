from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageRequest(BaseModel):
    """Request body for sending a guest message."""
    message: str = Field(..., min_length=1, description="The guest's message text")


class MessageItem(BaseModel):
    """A single message in the conversation history."""
    role: str = Field(..., description="Either 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")


class MessageResponse(BaseModel):
    """Response after processing a guest message."""
    conversation_id: str
    reply: str = Field(..., description="The agent's response to the guest")
    should_escalate: bool = Field(
        default=False,
        description="True if the request has been escalated to a human agent"
    )
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp of the reply")


class ConversationHistoryResponse(BaseModel):
    """Full conversation history for a session."""
    conversation_id: str
    messages: list[MessageItem]
    total_messages: int


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    status_code: int