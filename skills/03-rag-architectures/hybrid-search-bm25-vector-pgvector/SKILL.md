---
format: "v2"
name: "hybrid-search-bm25-vector-pgvector"
title: "Hybrid Search Bm25 Vector Pgvector"
title_fr: "Hybrid Search: BM25 + Vector + pgvector"
description: "Design pattern for hybrid retrieval combining sparse keyword search (BM25/TSVector) and dense vector search with RRF scoring in PostgreSQL/PGVector."
description_fr: "Pattern de recherche hybride combinant recherche par mots-clés (BM25/TSVector) et recherche vectorielle dense, avec scoring RRF dans PostgreSQL/PGVector."
domain: "03-rag-architectures"
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
Pure dense vector search excels at semantic similarity but fails on exact keyword matches (part numbers, technical error codes, proper nouns). Hybrid search combines BM25 keyword matching with dense vector retrieval using Reciprocal Rank Fusion (RRF).

---

### 1. Reciprocal Rank Fusion (RRF) Algorithm

$$\text{RRF Score}(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where $k$ is a smoothing constant (typically $k=60$) and $r_m(d)$ is the rank of document $d$ in retrieval method $m$.

---

### 2. PostgreSQL / PGVector Implementation

```sql
-- Combined TSVector (BM25 keyword) + HNSW Vector Search query in PGVector
WITH keyword_search AS (
    SELECT id, RANK() OVER (ORDER BY ts_rank_cd(text_search_vector, query) DESC) as rank
    FROM document_chunks, plainto_tsquery('english', 'Kafka SLA timeout') query
    WHERE text_search_vector @@ query
    LIMIT 20
),
vector_search AS (
    SELECT id, RANK() OVER (ORDER BY embedding <=> '[0.012, -0.045, ...]'::vector) as rank
    FROM document_chunks
    ORDER BY embedding <=> '[0.012, -0.045, ...]'::vector
    LIMIT 20
)
SELECT COALESCE(k.id, v.id) as chunk_id,
       (COALESCE(1.0 / (60 + k.rank), 0.0) + COALESCE(1.0 / (60 + v.rank), 0.0)) as rrf_score
FROM keyword_search k
FULL OUTER JOIN vector_search v ON k.id = v.id
ORDER BY rrf_score DESC
LIMIT 10;
```

---

### 3. Performance & Trade-offs

- **Search Accuracy (Recall@10)**: +25% higher than vector-only or keyword-only.
- **Latency Overhead**: ~10-15ms additional execution time in PostgreSQL.
- **Storage Requirement**: Requires GIN index for `tsvector` + HNSW index for `vector`.

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.