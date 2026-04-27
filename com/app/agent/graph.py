from langgraph.graph import StateGraph, END

from com.app.agent.state import AgentState
from com.app.agent.nodes import (
    classify_intent,
    run_tool,
    generate_response,
    escalate,
    handle_greeting,
    route_by_intent,
)


def build_graph() -> StateGraph:
    """
    Constructs and compiles the StayEase LangGraph agent.

    Graph flow:
        classify_intent
            ├── (intent: search/details/book) → run_tool → generate_response → END
            └── (intent: escalate/unknown)    → escalate → END
    """
    graph = StateGraph(AgentState)

    # ── Register nodes ────────────────────────────────────────────────────────
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("run_tool", run_tool)
    graph.add_node("generate_response", generate_response)
    graph.add_node("escalate", escalate)
    graph.add_node("greeting", handle_greeting)

    # ── Entry point ───────────────────────────────────────────────────────────
    graph.set_entry_point("classify_intent")

    # ── Conditional routing after classify_intent ─────────────────────────────
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "run_tool": "run_tool",
            "greeting": "greeting",
            "escalate": "escalate",
        },
    )

    # ── Linear edges ──────────────────────────────────────────────────────────
    graph.add_edge("run_tool", "generate_response")
    graph.add_edge("generate_response", END)
    graph.add_edge("escalate", END)
    graph.add_edge("greeting", END)

    return graph.compile()


# Singleton compiled graph — imported by chat service
agent_graph = build_graph()