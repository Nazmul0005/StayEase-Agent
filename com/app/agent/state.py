from typing import TypedDict, Optional, Any


class AgentState(TypedDict):
    """
    Shared state object passed between every node in the LangGraph agent.
    Each field is updated by specific nodes and read by others downstream.
    """

    conversation_id: str
    # Unique session identifier — used to load/save conversation from DB.

    messages: list[dict]
    # Full chat history as [{role: user|assistant, content: str, timestamp: str}].
    # Passed to the LLM for context on every turn.

    intent: Optional[str]
    # Classified intent of the latest user message.
    # One of: "search" | "details" | "book" | "escalate" | None.
    # Set by classify_intent node; drives conditional routing.

    search_params: Optional[dict]
    # Extracted search parameters from the user message.
    # Keys: location (str), check_in (str), check_out (str), guests (int).
    # Set by classify_intent; consumed by run_tool when intent == "search".

    selected_listing_id: Optional[str]
    # The listing UUID the guest is asking about or wants to book.
    # Set by classify_intent when intent is "details" or "book".

    booking_params: Optional[dict]
    # Guest details needed to create a booking.
    # Keys: guest_name (str), guest_phone (str).
    # Set by classify_intent when intent == "book".

    tool_result: Optional[Any]
    # Raw output from the last tool call (search results / listing detail / booking confirmation).
    # Set by run_tool node; consumed by generate_response node.

    should_escalate: bool
    # Flag indicating the agent could not handle the request and a human should take over.
    # Set to True by escalate node.