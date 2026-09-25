"""
LangChain + LangGraph AI Agent — Myntra Customer Service
Detection signals: AgentExecutor, create_react_agent, langchain, langgraph
Asset type: ai_agent_1st_party
"""
import os
from typing import Annotated

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


# ── Tools available to the agent ──────────────────────────────────────────────

@tool
def search_catalog(query: str) -> str:
    """Search Myntra product catalog for items matching the query."""
    # Production: calls catalog microservice
    return f"Found 12 results for '{query}': Blue Denim Jacket (₹1,999), ..."


@tool
def check_order_status(order_id: str) -> str:
    """Look up the current status of an order by its ID."""
    return f"Order {order_id}: Dispatched — Expected delivery: 2 days"


@tool
def initiate_return(order_id: str, reason: str) -> str:
    """Initiate a return request for an order."""
    return f"Return initiated for {order_id}. Pickup scheduled for tomorrow."


@tool
def get_size_recommendation(product_id: str, measurements: dict) -> str:
    """Recommend the right size based on product and user measurements."""
    return f"Based on your measurements, we recommend Size M for product {product_id}."


TOOLS = [search_catalog, check_order_status, initiate_return, get_size_recommendation]

# ── LangChain ReAct Agent ──────────────────────────────────────────────────────

def build_react_agent():
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful Myntra customer service agent.
         You help users find products, check orders, and handle returns.
         Use the available tools to assist users accurately."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_react_agent(llm, TOOLS, prompt)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True, max_iterations=5)


# ── LangGraph Stateful Agent ───────────────────────────────────────────────────

class CXAgentState(dict):
    messages: list
    user_id: str
    session_id: str


def build_langgraph_agent():
    """Build a stateful LangGraph agent for multi-turn CX conversations."""
    llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    llm_with_tools = llm.bind_tools(TOOLS)

    def agent_node(state: CXAgentState):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": state["messages"] + [response]}

    def should_continue(state: CXAgentState) -> str:
        last_msg = state["messages"][-1]
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            return "tools"
        return END

    tool_node = ToolNode(TOOLS)
    graph = StateGraph(CXAgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue)
    graph.add_edge("tools", "agent")
    return graph.compile()


if __name__ == "__main__":
    # Test the ReAct agent
    agent = build_react_agent()
    result = agent.invoke({"input": "I want to return order ORD-99887. It doesn't fit."})
    print(result["output"])
