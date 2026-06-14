# Enterprise LLM Application System

A production-grade multi-agent intelligent system built with FastAPI + LangGraph + GraphRAG. 8 weeks from 0 to production deployment — not a toy demo.


> Unlike simple RAG chatbots, this system implements full production-grade capabilities: multi-agent orchestration, hybrid knowledge retrieval, end-to-end safety guardrails, cost optimization, and continuous evaluation — all validated in real e-commerce customer service scenarios.

---

## Project Overview

- **Positioning**: Production-grade LLM application built from 0 to deployment in 8 weeks — not a toy demo.Although validated in e-commerce customer service scenarios, the core architecture patterns (GraphRAG, Multi-Agent orchestration, hybrid retrieval, safety guardrails) are domain-agnostic and directly transferable to finance, legal, ESG compliance, healthcare, and any knowledge-intensive LLM application.
- **Reference Implementation**: E-commerce customer support, after-sales consultation, order inquiry, product knowledge base Q&A

### Technical Highlights

- Hybrid knowledge retrieval (GraphRAG + Vector Search + Text2Cypher)
- Multi-Agent orchestration and task decomposition based on LangGraph
- Three-layer full-chain safety guardrails (Input → Execution → Output)
- Semantic caching + tiered model routing, reducing inference cost by 70%
- **Three-key Redis design** (vec / resp / meta separation) — query scans vector keys only, minimizing Redis bandwidth
- **UUID5-based deterministic multi-tenant isolation** for concurrent GraphRAG indexing
- **LangGraph Send API fan-out/fan-in** for parallel multi-subtask execution
- **Four GraphRAG query modes** (Local / Global / Drift / Basic) with adaptive data dependency selection
- **Cache-transparent pseudo-streaming**: cache hits simulate token-by-token output, frontend UX identical to live inference

### Quantifiable Results

| Metric | Before | After | Measurement Basis |
|:---|:---|:---|:---|
| Q&A Accuracy | 70% | **94%** | 500 manually labeled test cases, Recall@3 |
| Throughput | — | **1500 QPS** | Load tested on 4-core 8GB cloud server with Redis caching |
| Inference Cost | baseline | **-70%** | vs. single large-model inference |
| Service Availability | — | **99.9%** | 72-hour stability load test |
| Scenario Coverage | — | **98%** | 8 core business scenario statistics |
| Prompt Injection Interception | — | **95%** | OWASP LLM Top10 attack samples |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Request                              │
└─────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Redis Semantic Cache Layer                      │
│                                                                   │
│   Three-Key Design: vec:{md5} / resp:{md5} / meta:{md5}          │
│   ① Cosine similarity scan on vec keys only                      │
│   ② Cache HIT  → pseudo-streaming response (UX identical)       │
│   ③ Cache MISS → proceed to Agent                               │
└─────────────────────────┬───────────────────────────────────────┘
                           │ MISS
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  LangGraph Agent Orchestration                    │
│                                                                   │
│   analyze_and_route_query (LLM structured output → 5 classes)   │
│          │                                                        │
│          ├── general-query    → respond_to_general_query         │
│          ├── additional-query → Dual-Layer Guardrails            │
│          │                      Layer 1: Intent filter           │
│          │                      Layer 2: Live Neo4j Schema check │
│          │                      → get_additional_info            │
│          ├── graphrag-query   → create_research_plan             │
│          ├── image-query      → create_image_query               │
│          └── file-query       → create_file_query                │
│                                                                   │
│   ┌────────────────────────────────────────────────────────┐    │
│   │           kg_sub_graph: Multi-Tool Workflow             │    │
│   │                                                         │    │
│   │  planner → [Send API fan-out]                           │    │
│   │      ↓           ↓           ↓      (parallel)         │    │
│   │  tool_sel    tool_sel    tool_sel                        │    │
│   │      ↓           ↓           ↓                          │    │
│   │  ┌────────┐ ┌──────────┐ ┌─────────┐                   │    │
│   │  │Cypher  │ │GraphRAG  │ │ Search  │                   │    │
│   │  │Query   │ │Semantic  │ │ SerpAPI │                   │    │
│   │  └────────┘ └──────────┘ └─────────┘                   │    │
│   │      ↓           ↓           ↓      (fan-in)            │    │
│   │                summarize                                 │    │
│   │                   ↓                                      │    │
│   │              final_answer                                │    │
│   └────────────────────────────────────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Knowledge Retrieval Layer                       │
│                                                                   │
│  ┌──────────────────┐ ┌──────────────────┐ ┌────────────────┐   │
│  │  Text2Cypher     │ │  GraphRAG         │ │ Vector Search  │   │
│  │                  │ │                   │ │                │   │
│  │  NL → Cypher     │ │  Local Search     │ │ FAISS +        │   │
│  │  → Neo4j         │ │  Global Search    │ │ Multilingual   │   │
│  │  Self-correct    │ │  Drift Search     │ │ MiniLM         │   │
│  │  (max 3 retry)   │ │  Basic Search     │ │                │   │
│  └──────────────────┘ └──────────────────┘ └────────────────┘   │
│  Structured Data        Unstructured Knowledge   Semantic Docs   │
│  (orders/inventory)     (after-sales/manuals)    (RAG files)     │
└─────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data & Model Layer                           │
│  MySQL · Redis · Neo4J · LanceDB · Local Disk                    │
│  DeepSeek API · Ollama (Qwen2.5 / Llama3 / DeepSeek)            │
│  Docker · Cloud Server · GPU Server                              │
└─────────────────────────────────────────────────────────────────┘
```

> *Request flow: User request → Redis semantic cache (HIT: pseudo-streaming response / MISS: proceed) → LangGraph agent routing → parallel knowledge retrieval → result aggregation → response.*

---

## Tech Stack

| Category | Technology |
|:---|:---|
| Backend | FastAPI |
| Frontend | Vue 3 |
| Agent Orchestration | LangChain / LangGraph |
| RAG Engine | Microsoft GraphRAG |
| Vector Database | LanceDB |
| Embedding / Index | Multilingual MiniLM + FAISS |
| Graph Database | Neo4J |
| Relational Database | MySQL |
| Cache / Message Queue | Redis |
| Local Model Inference | Ollama (Qwen2.5 / Llama3 / DeepSeek series) |
| Online Model API | DeepSeek API / OpenAI Compatible |
| Deployment | Docker |

---

## Core Features

### 1. Hybrid Knowledge Retrieval

Unified query interface for structured data (orders / inventory / customers) and unstructured knowledge (after-sales policies / product manuals). Intelligent routing automatically selects the optimal retrieval strategy (GraphRAG / Vector Search / Text2Cypher). Multimodal PDF parsing and dynamic-aware chunking based on MinerU + LitServe.

**Four GraphRAG Query Modes** (adaptive selection based on query type):

| Mode | Use Case | Data Dependency |
|:---|:---|:---|
| Local | Precise entity queries | entities + relationships + text_units + covariates |
| Global | Thematic / macro analysis | communities + community_reports |
| Drift | Exploratory queries (loose relevance constraints) | entities + relationships + text_units |
| Basic | Lightweight lookup | text_units only |

### 2. Multi-Agent Orchestration

Full-chain collaboration via LangGraph: intent recognition → routing → task decomposition → tool execution → result aggregation. Automatic decomposition and parallel processing of complex multi-intent queries.

**LangGraph Send API fan-out/fan-in pattern**:
- **Problem**: Serial tool execution for multi-intent queries leads to compounding latency
- **Design**: `planner` node decomposes complex queries into independent subtasks, each dispatched in parallel via Send API, results aggregated in `summarize` → `final_answer`
- **Result**: Complex multi-tool query latency reduced by 40%+
- **Short-circuit optimization**: single-tool scenarios bypass LLM routing, saving token cost
- **Sliding window history**: last 5 Q&A pairs maintained per session to bound context growth

### 3. Three-Layer Full-Chain Safety Guardrails

**Input Layer**: Malicious prompt detection, user permission validation, sensitive information filtering

**Execution Layer**: Tool call permission control, privilege escalation interception, loop call circuit breaking

**Output Layer**: Response content safety filtering, hallucination detection / fact verification, sensitive data masking

### 4. Cost & Performance Optimization

Dual-layer semantic caching (exact match + semantic similarity match), cache hit rate up to 72%. Tiered model routing (lightweight models for simple queries, large models for complex reasoning). Streaming response output, time-to-first-token optimized to under 500ms. Built-in Ollama performance testing tool: single-request / concurrent benchmarking, system resource monitoring, automated test reports.

**Redis Semantic Cache — Three-Key Architecture**:

```
cache:{user_id}:vec:{md5}   ← Vector key (cosine similarity scan only)
cache:{user_id}:resp:{md5}  ← Response content
cache:{user_id}:meta:{md5}  ← Metadata (access time / hit count)
```

- **Problem**: Full cache entry scanning wastes Redis bandwidth; monolithic key design risks cross-user data leakage
- **Design**: Separate vector / response / metadata into independent key sets; queries scan only lightweight vector entries; per-user namespace enforces full isolation
- **Result**: Redis bandwidth minimized, LRU auto-eviction (`last_access` sorted) guarantees memory stability
- **Cache-transparent pseudo-streaming**: cache hits simulate token-by-token streaming — frontend UX identical to live inference, zero perceived difference

**Multi-Tenant GraphRAG Indexing**:

```python
# UUID5 deterministic isolation — same user_id always maps to same directory
user_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f"user_{user_id}")

# Runtime config injection — no global config file modification needed
config_overrides = {
    'input.base_dir': user_input_dir,
    'output.base_dir': user_output_dir,
}
```

- **Problem**: UUID4 random paths break after service restarts; concurrent multi-user indexing causes mutual interference
- **Design**: UUID5 deterministic mapping from user ID to directory path; `config_overrides` runtime injection without modifying global config files
- **Result**: Zero cross-user data pollution, directory paths persist across service restarts, supports fully concurrent multi-user indexing

### 5. Continuous Evaluation & Iteration Loop

- **Golden dataset**: 200+ labeled test cases covering 8 core business scenarios, mixing real production data and adversarial edge cases
- **Regression gate**: 2% accuracy drop threshold automatically blocks deployment, preventing online degradation
- **Two-layer accuracy definition**: execution accuracy (70%) + semantic accuracy (30%) with manual sampling
- **Closed feedback loop**: online failure cases automatically archived and periodically supplemented to test sets and Few-shot samples
- **Result**: SQL generation accuracy improved from 60% to 93%, human review rate reduced to 5%

---

## Quick Start

### 1. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `env.example` to `llm_backend/.env`:

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
MYSQL_DATABASE=llm_app_system
```

### 3. Initialize Database

```bash
cd llm_backend
python scripts/init_db.py
```

### 4. Start the Service

```bash
python run.py
```

- API Docs: http://localhost:8000/docs
- Frontend UI: http://localhost:8000

---

## Engineering Deep-Dive Series

A complete 8-week engineering retrospective covering architecture decisions, lessons learned, and best practices:

1. [Week 1: Architecture Overview — Building a Production-Grade LLM Application from Scratch](https://dev.to/jamesli/-from-0-to-mvp-in-2-weeks-building-a-production-grade-ai-customer-service-system-322n)
2. [Week 2: Production GraphRAG Pipeline — From PDF to Knowledge Graph](https://dev.to/jamesli/-production-grade-graphrag-data-pipeline-end-to-end-construction-from-pdf-parsing-to-knowledge-1dhj)
3. [Week 3: GraphRAG Service Packaging — From CLI to Enterprise-Grade API](https://dev.to/jamesli/engineering-graphrag-for-production-api-design-query-optimization-and-service-reliability-2mh6)
4. [Week 4: Multi-Agent Architecture — Complex Task Handling with LangGraph](https://dev.to/jamesli/building-an-enterprise-grade-multi-agent-customer-service-system-with-langgraph-2a31)
5. [Week 5: Safety at the Core — Full-Chain LLM Guardrails for Production](https://dev.to/jamesli/building-safety-guardrails-for-llm-customer-service-that-actually-work-in-production-3g7b)
6. [Week 6: Closing the Loop — Hybrid Knowledge Retrieval and Capability Integration](https://dev.to/jamesli/hybrid-knowledge-retrieval-combining-neo4j-graph-queries-graphrag-and-vector-search-for-3f89)
7. [Week 7: Production Optimization — Inference Cost and Performance Control](https://dev.to/jamesli/production-optimization-inference-cost-and-performance-control-2433)
8. [Week 8: 8-Week Retrospective — Architecture Decisions, Lessons Learned & Best Practices](https://dev.to/jamesli/building-a-production-grade-llm-customer-service-in-8-weeks-architecture-decisions-pitfalls-and-4nmi)
9. [Bonus: From 60% to 93% — How We Built a Continuous Evaluation Framework for LLM Systems](https://dev.to/jamesli/from-60-to-93-how-we-built-a-continuous-evaluation-framework-for-llm-systems-i4)
