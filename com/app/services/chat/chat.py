from datetime import datetime
from sqlalchemy.orm import Session

from com.app.agent.graph import agent_graph
from com.app.agent.state import AgentState
from com.app.database.models.models import Conversation


def process_message(
    conversation_id: str,
    user_message: str,
    db: Session,
) -> dict:
    """
    Processes an incoming guest message through the LangGraph agent.

    Steps:
    1. Load or create the conversation from the database.
    2. Append the user message to conversation history.
    3. Invoke the LangGraph agent with the full state.
    4. Extract the agent's reply from the updated state.
    5. Persist the updated conversation back to the database.

    Returns a dict with reply, should_escalate, and timestamp.
    """
    # Load or create conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()

    if not conversation:
        conversation = Conversation(id=conversation_id, messages=[])
        db.add(conversation)
        db.commit()

    # Append user message
    user_msg = {
        "role": "user",
        "content": user_message,
        "timestamp": datetime.utcnow().isoformat(),
    }
    current_messages = list(conversation.messages or []) + [user_msg]

    # Build initial agent state
    initial_state: AgentState = {
        "conversation_id": conversation_id,
        "messages": current_messages,
        "intent": None,
        "search_params": None,
        "selected_listing_id": None,
        "booking_params": None,
        "tool_result": None,
        "should_escalate": False,
    }

    # Run the LangGraph agent
    final_state: AgentState = agent_graph.invoke(initial_state)

    # Extract the last assistant message
    updated_messages = final_state["messages"]
    assistant_reply = next(
        (m for m in reversed(updated_messages) if m["role"] == "assistant"),
        {"content": "Sorry, something went wrong.", "timestamp": datetime.utcnow().isoformat()},
    )

    # Persist updated conversation
    conversation.messages = updated_messages
    conversation.updated_at = datetime.utcnow()
    db.commit()

    return {
        "reply": assistant_reply["content"],
        "should_escalate": final_state.get("should_escalate", False),
        "timestamp": assistant_reply["timestamp"],
    }


def get_conversation_history(conversation_id: str, db: Session) -> dict:
    """
    Retrieves the full message history for a given conversation ID.
    Returns an empty messages list if the conversation does not exist yet.
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()

    if not conversation:
        return {
            "conversation_id": conversation_id,
            "messages": [],
            "total_messages": 0,
        }

    messages = conversation.messages or []

    return {
        "conversation_id": conversation_id,
        "messages": messages,
        "total_messages": len(messages),
    }