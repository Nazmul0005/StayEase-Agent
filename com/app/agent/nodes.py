import json
from datetime import datetime
from typing import Literal

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from com.app.agent.state import AgentState
from com.app.agent.tools import search_available_properties, get_listing_details, create_booking, TOOLS
from com.app.config.config import Config

config = Config()

# ─── LLM Setup ────────────────────────────────────────────────────────────────

llm = ChatGroq(
    api_key=config.GROQ_API_KEY,
    model=config.GROQ_MODEL,
    temperature=0,
)

llm_with_tools = llm.bind_tools(TOOLS)

# ─── System Prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful booking assistant for StayEase, a short-term accommodation 
rental platform in Bangladesh. You help guests search for properties, get listing details, 
and make bookings.

You can ONLY handle these three tasks:
1. Search — Guest provides location, dates, and number of guests. Return available properties.
2. Details — Guest asks about a specific property. Return listing information.
3. Book — Guest confirms they want to book a property. Create the booking.

For anything outside these three tasks, respond that you need to escalate to a human agent.

When extracting information from user messages:
- Dates should be in YYYY-MM-DD format
- Prices are always in BDT (Bangladeshi Taka)
- Be friendly and professional in Bangladeshi context

Always respond in the same language the guest uses (Bengali or English)."""


# ─── Nodes ────────────────────────────────────────────────────────────────────

def classify_intent(state: AgentState) -> AgentState:
    """
    Sends the latest user message to the LLM to classify intent and extract parameters.
    Determines whether the agent should search, get details, book, or escalate.
    Updates: intent, search_params, selected_listing_id, booking_params.
    Next: run_tool (if actionable intent) or escalate (if unhandled).
    """
    messages = state["messages"]
    latest_message = messages[-1]["content"] if messages else ""

    classification_prompt = f"""Analyze this user message and respond ONLY with a JSON object.

User message: "{latest_message}"

Respond with exactly this JSON structure:
{{
  "intent": "<search|details|book|escalate>",
  "search_params": {{
    "location": "<location or null>",
    "check_in": "<YYYY-MM-DD or null>",
    "check_out": "<YYYY-MM-DD or null>",
    "guests": <number or null>
  }},
  "selected_listing_id": "<listing UUID or null>",
  "booking_params": {{
    "guest_name": "<name or null>",
    "guest_phone": "<phone or null>"
  }}
}}

Rules:
- intent = "search" if the guest wants to find available properties
- intent = "details" if asking about a specific property
- intent = "book" if confirming a booking
- intent = "escalate" for anything else
- Fill only the fields relevant to the intent, null for others"""

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=classification_prompt),
    ])

    try:
        raw = response.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        parsed = json.loads(raw.strip())
    except (json.JSONDecodeError, IndexError):
        parsed = {
            "intent": "escalate",
            "search_params": None,
            "selected_listing_id": None,
            "booking_params": None,
        }

    return {
        **state,
        "intent": parsed.get("intent", "escalate"),
        "search_params": parsed.get("search_params"),
        "selected_listing_id": parsed.get("selected_listing_id"),
        "booking_params": parsed.get("booking_params"),
    }


def run_tool(state: AgentState) -> AgentState:
    """
    Executes the appropriate tool based on the classified intent and extracted parameters.
    Calls one of: search_available_properties, get_listing_details, or create_booking.
    Updates: tool_result.
    Next: generate_response.
    """
    intent = state["intent"]
    result = None

    if intent == "search":
        params = state.get("search_params") or {}
        result = search_available_properties.invoke({
            "location": params.get("location", ""),
            "check_in": params.get("check_in", ""),
            "check_out": params.get("check_out", ""),
            "guests": params.get("guests", 1),
        })

    elif intent == "details":
        listing_id = state.get("selected_listing_id", "")
        result = get_listing_details.invoke({"listing_id": listing_id})

    elif intent == "book":
        params = state.get("search_params") or {}
        booking = state.get("booking_params") or {}
        result = create_booking.invoke({
            "listing_id": state.get("selected_listing_id", ""),
            "guest_name": booking.get("guest_name", "Guest"),
            "guest_phone": booking.get("guest_phone"),
            "check_in": params.get("check_in", ""),
            "check_out": params.get("check_out", ""),
            "guests": params.get("guests", 1),
        })

    return {**state, "tool_result": result}


def generate_response(state: AgentState) -> AgentState:
    """
    Sends the tool result to the LLM to produce a natural, friendly guest-facing reply.
    Formats prices in BDT and property details in a readable way.
    Updates: messages (appends the assistant reply with timestamp).
    Next: END.
    """
    tool_result = state.get("tool_result", {})
    intent = state["intent"]

    context_prompt = f"""Based on this tool result, write a helpful, friendly reply to the guest.

Intent: {intent}
Tool result: {json.dumps(tool_result, indent=2)}

Guidelines:
- Format prices as BDT X,XXX (e.g. BDT 3,500)
- If search results, list properties clearly with names and prices
- If booking confirmed, include booking ID and total price
- If an error occurred, apologize and suggest alternatives
- Keep it concise and warm"""

    history = [
        HumanMessage(content=m["content"]) if m["role"] == "user"
        else AIMessage(content=m["content"])
        for m in state["messages"]
    ]

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        *history,
        HumanMessage(content=context_prompt),
    ])

    assistant_message = {
        "role": "assistant",
        "content": response.content,
        "timestamp": datetime.utcnow().isoformat(),
    }

    updated_messages = state["messages"] + [assistant_message]

    return {**state, "messages": updated_messages}


def escalate(state: AgentState) -> AgentState:
    """
    Generates a polite escalation message when the agent cannot handle the guest's request.
    Informs the guest that a human agent will assist them shortly.
    Updates: messages (appends escalation reply), should_escalate = True.
    Next: END.
    """
    escalation_message = {
        "role": "assistant",
        "content": (
            "I'm sorry, I can only help with searching for properties, "
            "getting listing details, and making bookings. "
            "For anything else, I'm connecting you with a human agent who will "
            "assist you shortly. Thank you for your patience!"
        ),
        "timestamp": datetime.utcnow().isoformat(),
    }

    updated_messages = state["messages"] + [escalation_message]

    return {
        **state,
        "messages": updated_messages,
        "should_escalate": True,
    }


# ─── Routing ──────────────────────────────────────────────────────────────────

def route_by_intent(state: AgentState) -> Literal["run_tool", "escalate"]:
    """
    Conditional edge function: routes to run_tool for actionable intents,
    or to escalate for anything the agent cannot handle.
    """
    intent = state.get("intent")
    if intent in ("search", "details", "book"):
        return "run_tool"
    return "escalate"