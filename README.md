# Enterprise LLM Customer Service System

A production-grade intelligent customer service system built with FastAPI and Vue 3, deeply adapted for e-commerce scenarios. Covers mainstream production-level requirements including Agent orchestration, RAG, safety guardrails, and cost optimization.

## Project Overview
- **Positioning**: Production-grade LLM customer service system built from 0 to deployment in 8 weeks — not a toy demo
- **Use Cases**: E-commerce customer support, after-sales consultation, order inquiry, product knowledge base Q&A
- **Technical Highlights**:
  - Hybrid knowledge retrieval (GraphRAG + Vector Search + Text2Cypher)
  - Multi-Agent orchestration and task decomposition based on LangGraph
  - Three-layer full-chain safety guardrails (Input → Execution → Output)
  - Semantic caching + tiered model routing, reducing inference cost by 70%
- **Quantifiable Results**:
  - Q&A accuracy 94% (based on 500 manually labeled test cases, Recall@3 evaluation)
  - 1500 QPS throughput (load tested on 4-core 8GB cloud server with Redis caching layer)
  - 99.9% service availability, 98% scenario coverage
  - 95% prompt injection interception rate (based on OWASP LLM Top10 attack samples)

## System Architecture

```plaintext
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LLM Application Architecture Layer                    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Application Layer                                                   │    │
│  │  · User Service (Login / Register)  · Session Service               │    │
│  │  · Knowledge Base Service                                            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Feature Layer                                                       │    │
│  │  · Multi-Agent Architecture    · Safety Guardrails                   │    │
│  │  · Text2Cypher Debug           · Offline/Online Index Construction   │    │
│  │  · Hybrid Knowledge Retrieval                                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LLM Technology Architecture Layer                    │
│                                                                               │
│  ┌───────────────┐        ┌───────────────┐        ┌───────────────┐        │
│  │     Agent     │        │      RAG      │        │   Workflow    │        │
│  └───────────────┘        └───────────────┘        └───────────────┘        │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │            LangChain / LangGraph / Microsoft GraphRAG                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  Vue / FastAPI / SSE / Open API                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LLM Platform Architecture Layer                     │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Model Layer                                                         │    │
│  │  · DeepSeek Online Model              · vLLM Model Deployment        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Data Layer                                                          │    │
│  │  · MySQL    · Redis    · Neo4J    · Memory    · Local Disk · LanceDB │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Infrastructure Layer                                                │    │
│  │  · Cloud Server          · GPU Server          · Docker Platform     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack
- **Backend**: FastAPI
- **Frontend**: Vue 3
- **Agent Orchestration**: LangChain / LangGraph
- **RAG Engine**: Microsoft GraphRAG
- **Vector Database**: LanceDB
- **Graph Database**: Neo4J
- **Relational Database**: MySQL
- **Cache / Message Queue**: Redis
- **Local Model Inference**: Ollama (Qwen2.5 / Llama3 / DeepSeek series)
- **Online Model API**: DeepSeek API / OpenAI Compatible
- **Deployment**: Docker

## Core Features

### 1. Hybrid Knowledge Retrieval
- Unified query interface for structured data (orders / inventory / customers) and unstructured knowledge (after-sales policies / product manuals)
- Intelligent routing automatically selects the optimal retrieval strategy (GraphRAG / Vector Search / Text2Cypher)
- Multimodal PDF parsing and dynamic-aware chunking based on MinerU + LitServe

### 2. Multi-Agent Orchestration
- Full-chain collaboration via LangGraph: intent recognition → routing → task decomposition → tool execution → result aggregation
- Automatic decomposition and parallel processing of complex multi-intent queries

### 3. Three-Layer Full-Chain Safety Guardrails
- **Input Layer**: Malicious prompt detection, user permission validation, sensitive information filtering
- **Execution Layer**: Tool call permission control, privilege escalation interception, loop call circuit breaking
- **Output Layer**: Response content safety filtering, hallucination detection / fact verification, sensitive data masking

### 4. Cost & Performance Optimization
- Dual-layer semantic caching (exact match + semantic similarity match), cache hit rate up to 72%
- Tiered model routing (lightweight models for simple queries, large models for complex reasoning)
- Streaming response output, time-to-first-token optimized to under 500ms
- Built-in Ollama performance testing tool: single-request / concurrent benchmarking, system resource monitoring, automated test reports

## Quick Start

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `env.example` to `llm_backend/.env` and update the values accordingly:
```env
# LLM Service Configuration
CHAT_SERVICE=OLLAMA        # or DEEPSEEK
REASON_SERVICE=OLLAMA      # or DEEPSEEK

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=deepseek-coder:6.7b
OLLAMA_REASON_MODEL=deepseek-coder:6.7b

# DeepSeek Configuration (if applicable)
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=llm_customer_service
```

### 3. Initialize Database
```bash
cd llm_backend
python scripts/init_db.py
```

### 4. Start the Service
```bash
# Start service (default port 8000)
python run.py
```

Once running, access:
- API Docs: http://localhost:8000/docs
- Frontend UI: http://localhost:8000

## Engineering Deep-Dive Series
A complete 8-week engineering retrospective covering architecture decisions, lessons learned, and best practices:

1. [Week 1: Architecture Overview — Building a Production-Grade AI Customer Service System from Scratch](link-pending)
2. [Week 2: Production GraphRAG Pipeline — From PDF to Knowledge Graph](link-pending)
3. [Week 3: GraphRAG Service Packaging — From CLI to Enterprise-Grade API](link-pending)
4. [Week 4: Multi-Agent Architecture — Complex Task Handling with LangGraph](link-pending)
5. [Week 5: Safety at the Core — Full-Chain LLM Guardrails for Production](link-pending)
6. [Week 6: Closing the Loop — Hybrid Knowledge Retrieval and Capability Integration](link-pending)
7. [Week 7: Production Optimization — Inference Cost and Performance Control](link-pending)
8. [Week 8: 8-Week Retrospective — Architecture Decisions, Lessons Learned & Best Practices](link-pending)
