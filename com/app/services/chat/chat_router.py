from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from com.app.database.db_connection.db_connection import get_db
from com.app.services.chat.chat import process_message, get_conversation_history
from com.app.services.chat.chat_schema import (
    MessageRequest,
    MessageResponse,
    ConversationHistoryResponse,
)

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post(
    "/{conversation_id}/message",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a guest message",
    description="Sends a guest message to the StayEase AI agent and returns the agent's reply.",
)
def send_message(
    conversation_id: str,
    body: MessageRequest,
    db: Session = Depends(get_db),
) -> MessageResponse:
    """
    Accepts a guest message, runs it through the LangGraph agent,
    and returns the agent's reply along with escalation status.
    """
    try:
        result = process_message(
            conversation_id=conversation_id,
            user_message=body.message,
            db=db,
        )
        return MessageResponse(
            conversation_id=conversation_id,
            reply=result["reply"],
            should_escalate=result["should_escalate"],
            timestamp=result["timestamp"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent processing failed: {str(e)}",
        )


@router.get(
    "/{conversation_id}/history",
    response_model=ConversationHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get conversation history",
    description="Returns the full message history for a conversation session.",
)
def get_history(
    conversation_id: str,
    db: Session = Depends(get_db),
) -> ConversationHistoryResponse:
    """
    Retrieves all messages (user and assistant) for the given conversation ID.
    Returns an empty list if the conversation has not started yet.
    """
    result = get_conversation_history(conversation_id=conversation_id, db=db)
    return ConversationHistoryResponse(**result)