"""
Prompt templates for agent workflow.
Includes system prompts for routing, query classification, RAG search, hallucination checking, etc.
"""

# Routing system prompt
ROUTER_SYSTEM_PROMPT = """
You are an intelligent customer service agent in the e-commerce domain. 
Your task is to classify user queries into types such as general-query, rag-search, image-query, etc.
"""

# Additional system prompt
GET_ADDITIONAL_SYSTEM_PROMPT = "..."

# General query system prompt
GENERAL_QUERY_SYSTEM_PROMPT = "..."

# Image query system prompt
GET_IMAGE_SYSTEM_PROMPT = "..."

# Guardrails system prompt
GUARDRAILS_SYSTEM_PROMPT = "..."

# RAG search system prompt
RAGSEARCH_SYSTEM_PROMPT = "..."

# Hallucination check prompt
CHECK_HALLUCINATIONS = "..."

# Query generation system prompt
GENERATE_QUERIES_SYSTEM_PROMPT = "..."