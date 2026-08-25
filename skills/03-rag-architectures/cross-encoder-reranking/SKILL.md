---
format: "v2"
name: "cross-encoder-reranking"
title: "Cross Encoder Reranking"
title_fr: "Reranking par Cross-Encoder"
description: "Adding a second-stage cross-encoder pass after vector/hybrid retrieval to re-score candidates jointly with the query, correcting for the recall-over-precision bias of embedding search."
description_fr: "Ajouter une seconde passe de cross-encoder après la recherche vectorielle/hybride pour re-noter les candidats conjointement avec la requête, corrigeant le biais recall-sur-precision de la recherche par embeddings."
domain: "03-rag-architectures"
tags: [rag, retrieval, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["bash", "python"]
updated: "2026-08-25"
---



## Prerequisites
- A first-stage retriever (vector, BM25, or hybrid) already returning a candidate set (top-50 to top-100).
- A cross-encoder model available either self-hosted (`sentence-transformers` cross-encoders) or via a reranking API.

## Usage
### Architectural Purpose
Bi-encoder retrieval (embed query, embed docs, compare by cosine similarity) encodes the query and each document independently, so it can never model query-document interaction terms — it optimizes for "roughly the same topic", not "actually answers this specific question". A cross-encoder feeds `(query, document)` as a single joint input to a transformer and outputs a direct relevance score, which is far more precise but too slow to run over an entire corpus. The standard pattern is: cheap bi-encoder for broad recall, expensive cross-encoder for precise reordering of a small candidate set.

---

### 1. Two-Stage Retrieval Pipeline

```text
Query
  |
  v
+------------------+     top-50      +-------------------+     top-5..8
| Bi-Encoder /      | ------------>  |   Cross-Encoder    | -----------> LLM Context
| Hybrid Retriever  |  (cheap, fast) |   Reranker          |  (precise, slower)
+------------------+                 +-------------------+
```

The cross-encoder never touches the full corpus — it only rescores the already-narrowed candidate set, keeping total latency bounded regardless of corpus size.

---

### 2. Implementation

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, candidates: list[str], top_k: int = 6) -> list[str]:
    pairs = [(query, doc) for doc in candidates]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]

# Pipeline: broad recall then precise cut
candidates = hybrid_retrieve(query, k=50)
final_context = rerank(query, candidates, top_k=6)
```

For hosted alternatives (Cohere Rerank, Voyage rerank), the contract is identical: send `(query, candidates)`, receive a relevance-ordered list — swap the `rerank()` implementation without touching the retrieval stage.

---

### 3. Cost, Latency & Trade-offs

- **Latency**: a cross-encoder pass over 50 candidates typically adds 50-150ms self-hosted (batch-friendly, GPU) or 100-300ms via a hosted reranking API — acceptable when it replaces sending 50 noisy chunks to the LLM instead of 6 precise ones (which itself costs far more in generation tokens and hallucination risk).
- **Candidate set size**: rerank at most 50-100 candidates. Reranking is O(n) in the candidate count with a much heavier per-item cost than the first-stage retriever; feeding it the top-1000 defeats the purpose.
- **When to skip it**: for corpora under a few thousand chunks with high-quality embeddings and low query ambiguity, the bi-encoder alone is often sufficient — measure retrieval precision@k before adding a reranking stage, don't add it by default.

## Inputs
- The user query.
- Candidate document/chunk list from first-stage retrieval (recommended: 20-100 candidates).

## Outputs
- A precision-ordered subset (typically top-5 to top-8) passed to the LLM as context.
- Measurable lift in `context_precision` (see [ragas-evaluation-metrics](../../09-evaluations-and-observability/ragas-evaluation-metrics/SKILL.md)) vs first-stage retrieval alone.
