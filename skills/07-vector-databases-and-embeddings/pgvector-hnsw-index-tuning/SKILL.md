---
format: "v2"
name: "pgvector-hnsw-index-tuning"
title: "pgvector HNSW Index Tuning"
title_fr: "pgvector HNSW Index Tuning"
description: "Performance optimization and index tuning guidelines for PostgreSQL PGVector using HNSW indexes."
description_fr: "Directives d'optimisation des performances et de réglage des index pour PostgreSQL PGVector avec des index HNSW."
domain: "07-vector-databases-and-embeddings"
tags: [cybersecurity, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["bash", "git"]
updated: "2026-08-08"
---



## Prerequisites
- Target system, dependencies and environment configured.

## Usage
### Architectural Purpose
Without proper indexing, similarity search in PostgreSQL performs a sequential scan over all vector rows. Hierarchical Navigable Small World (HNSW) indexes provide sub-millisecond approximate nearest neighbor (ANN) search.

---

### 1. HNSW Index Creation Syntax

```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with 1536-dim vectors (e.g. text-embedding-3-small)
CREATE TABLE document_embeddings (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(1536)
);

-- Build HNSW index with Cosine similarity
CREATE INDEX idx_embeddings_hnsw_cosine 
ON document_embeddings 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

---

### 2. Parameter Tuning Reference

| Parameter | Recommended Value | Impact |
| :--- | :--- | :--- |
| `m` | `16` (default: 16, max: 100) | Max number of bi-directional links per node. Higher `m` increases recall and index size. |
| `ef_construction` | `64` to `128` | Search queue size during index construction. Higher values improve index quality at cost of build time. |
| `hnsw.ef_search` | `40` to `100` (runtime) | Dynamic candidate list size during queries. Tunable per session: `SET hnsw.ef_search = 100;` |

---

### 3. Distance Metrics Selection

- **Cosine Distance (`vector_cosine_ops` / `<=>`)**: Best for text embeddings normalized to length 1.
- **L2 / Euclidean (`vector_l2_ops` / `<->`)**: Use for non-normalized geometric vectors.
- **Inner Product (`vector_ip_ops` / `<#>`)**: Fastest performance when vectors are pre-normalized.

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.