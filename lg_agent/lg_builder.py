from app.lg_agent.lg_states import AgentState, Router
from app.lg_agent.lg_prompts import (
    ROUTER_SYSTEM_PROMPT,
    GET_ADDITIONAL_SYSTEM_PROMPT,
    GENERAL_QUERY_SYSTEM_PROMPT,
    GET_IMAGE_SYSTEM_PROMPT,
    GUARDRAILS_SYSTEM_PROMPT,
    RAGSEARCH_SYSTEM_PROMPT,
    CHECK_HALLUCINATIONS,
    GENERATE_QUERIES_SYSTEM_PROMPT
)
from langchain_core.runnables import RunnableConfig
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from app.core.config import settings, ServiceType
from app.core.logger import get_logger
from typing import cast, Literal, TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from app.lg_agent.lg_states import AgentState, InputState, Router, GradeHallucinations
from app.lg_agent.kg_sub_graph.agentic_rag_agents.retrievers.cypher_examples.northwind_retriever import NorthwindCypherRetriever
from app.lg_agent.kg_sub_graph.agentic_rag_agents.components.planner.node import create_planner_node
from app.lg_agent.kg_sub_graph.agentic_rag_agents.workflows.multi_agent.multi_tool import create_multi_tool_workflow
from app.lg_agent.kg_sub_graph.kg_neo4j_conn import get_neo4j_graph
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage
from langchain_core.runnables.base import Runnable
from app.lg_agent.kg_sub_graph.agentic_rag_agents.components.utils.utils import retrieve_and_parse_schema_from_graph_for_prompts
from langchain_core.prompts import ChatPromptTemplate
import base64
import os
import aiohttp
import asyncio
import json
import time
from pathlib import Path

# Logger
logger = get_logger(service="lg_builder")

# Structured output schema for guardrails decision
class AdditionalGuardrailsOutput(BaseModel):
    decision: Literal["end", "continue"] = Field(
        description="Decision on whether the question is related to the graph contents."
    )

# ----------- Query Analysis & Routing Node -----------
async def analyze_and_route_query(state: AgentState, *, config: RunnableConfig) -> dict[str, Router]:
    """
    Analyze user query and determine routing type.
    Uses LLM to classify user input and decide the downstream workflow branch.
    """
    # Select model
    if settings.AGENT_SERVICE == ServiceType.DEEPSEEK:
        model = ChatDeepSeek(...)
    else:
        model = ChatOllama(...)
    # Prepend system prompt to conversation history
    messages = [{"role": "system", "content": ROUTER_SYSTEM_PROMPT}] + state.messages
    logger.info("-----Analyze user query type-----")
    # Invoke model with structured output for classification
    response = cast(Router, await model.with_structured_output(Router).ainvoke(messages))
    logger.info(f"Analyze user query type completed, result: {response}")
    return {"router": response}

# ----------- Routing Branch Logic -----------
def route_query(state: AgentState) -> Literal[
    "respond_to_general_query", "get_additional_info", "create_research_plan",
    "create_image_query", "create_file_query"
]:
    """
    Determine the next node based on routing result.
    """
    _type = state.router["type"]
    # Image path takes priority
    if hasattr(state, "config") and state.config and state.config.get("configurable", {}).get("image_path"):
        logger.info("Image path detected, routing to image query handler")
        return "create_image_query"
    # Route by classification type
    if _type == "general-query":
        return "respond_to_general_query"
    elif _type == "additional-query":
        return "get_additional_info"
    elif _type == "graphrag-query":
        return "create_research_plan"
    elif _type == "image-query":
        return "create_image_query"
    elif _type == "file-query":
        return "create_file_query"
    else:
        raise ValueError(f"Unknown router type {_type}")

# ----------- General Query Response Node -----------
async def respond_to_general_query(state: AgentState, *, config: RunnableConfig) -> Dict[str, List[BaseMessage]]:
    """
    Generate a response for general queries (LLM only, no knowledge base or tool calls).
    """
    logger.info("-----generate general-query response-----")
    # Select model
    if settings.AGENT_SERVICE == ServiceType.DEEPSEEK:
        model = ChatDeepSeek(...)
    else:
        model = ChatOllama(...)
    # Build prompt with routing logic context
    system_prompt = GENERAL_QUERY_SYSTEM_PROMPT.format(logic=state.router["logic"])
    messages = [{"role": "system", "content": system_prompt}] + state.messages
    response = await model.ainvoke(messages)
    return {"messages": [response]}

# ----------- Additional Info Collection Node -----------
async def get_additional_info(state: AgentState, *, config: RunnableConfig) -> Dict[str, List[BaseMessage]]:
    """
    Generate a response asking the user for more information,
    grounded in business scope and graph schema.
    """
    logger.info("------continue to get additional info------")
    # Select model
    ...
    # Connect to Neo4j and extract graph schema
    ...
    # Build system prompt
    ...
    # Invoke model with structured output to decide whether to continue
    ...
    # Return appropriate response based on decision
    ...

# ----------- Image Query Node -----------
async def create_image_query(state: AgentState, *, config: RunnableConfig) -> Dict[str, List[BaseMessage]]:
    """
    Handle image queries: compress image, encode to base64,
    call vision model API, and generate a descriptive response.
    """
    logger.info("-----Found User Upload Image-----")
    image_path = config.get("configurable", {}).get("image_path", None)
    if not image_path or not Path(image_path).exists():
        logger.warning(f"User uploaded image not found: {image_path}")
        return {"messages": [AIMessage(content="Sorry, I'm unable to view this image. Please re-upload and try again.")]}
    # Compress image, encode to base64, prepare API request
    ...
    # Call vision model API and retrieve image description
    ...
    # Generate final response using image description
    ...

# ----------- File Query Node (TODO) -----------
async def create_file_query(state: AgentState, *, config: RunnableConfig) -> Dict[str, List[BaseMessage]]:
    """
    File query handler (not yet implemented).
    """
    # TODO: implement file processing logic
    ...

# ----------- Knowledge Base Query & Task Decomposition Node -----------
async def create_research_plan(state: AgentState, *, config: RunnableConfig) -> Dict[str, List[str] | str]:
    """
    Query local knowledge base, decompose tasks,
    and generate a multi-hop query execution plan.
    """
    logger.info("------execute local knowledge base query------")
    # Select model
    ...
    # Connect to Neo4j graph database
    ...
    # Initialize custom retriever, tool list, and predefined Cypher queries
    ...
    # Build and execute multi-tool workflow
    ...
    # Return execution results
    ...

# ----------- Hallucination Detection Node -----------
async def check_hallucinations(state: AgentState, *, config: RunnableConfig) -> dict[str, Any]:
    """
    Check LLM output for hallucinations and return a graded result.
    """
    ...
    # Build prompt, invoke model, parse structured output
    ...

# ----------- State Graph & Persistence -----------
checkpointer = MemorySaver()
builder = StateGraph(AgentState, input=InputState)
builder.add_node(analyze_and_route_query)
builder.add_node(respond_to_general_query)
builder.add_node(get_additional_info)
builder.add_node("create_research_plan", create_research_plan)
builder.add_node(create_image_query)
builder.add_node(create_file_query)
builder.add_edge(START, "analyze_and_route_query")
builder.add_conditional_edges("analyze_and_route_query", route_query)

graph = builder.compile(checkpointer=checkpointer)
