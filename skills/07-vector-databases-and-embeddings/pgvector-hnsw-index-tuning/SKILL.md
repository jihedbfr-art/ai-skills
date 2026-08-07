---
name: pgvector-hnsw-index-tuning
description: Performance optimization and index tuning guidelines for PostgreSQL PGVector using HNSW indexes.
version: 1.0.0
---

# PGVector HNSW Index Tuning & Performance Guide

## Architectural Purpose
Without proper indexing, similarity search in PostgreSQL performs a sequential scan over all vector rows. Hierarchical Navigable Small World (HNSW) indexes provide sub-millisecond approximate nearest neighbor (ANN) search.

---

## 1. HNSW Index Creation Syntax

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

## 2. Parameter Tuning Reference

| Parameter | Recommended Value | Impact |
| :--- | :--- | :--- |
| `m` | `16` (default: 16, max: 100) | Max number of bi-directional links per node. Higher `m` increases recall and index size. |
| `ef_construction` | `64` to `128` | Search queue size during index construction. Higher values improve index quality at cost of build time. |
| `hnsw.ef_search` | `40` to `100` (runtime) | Dynamic candidate list size during queries. Tunable per session: `SET hnsw.ef_search = 100;` |

---

## 3. Distance Metrics Selection

- **Cosine Distance (`vector_cosine_ops` / `<=>`)**: Best for text embeddings normalized to length 1.
- **L2 / Euclidean (`vector_l2_ops` / `<->`)**: Use for non-normalized geometric vectors.
- **Inner Product (`vector_ip_ops` / `<#>`)**: Fastest performance when vectors are pre-normalized.
