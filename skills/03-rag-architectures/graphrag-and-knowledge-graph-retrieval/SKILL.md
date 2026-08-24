---
format: "v2"
name: "graphrag-and-knowledge-graph-retrieval"
title: "GraphRAG And Knowledge Graph Retrieval"
title_fr: "GraphRAG et Récupération par Graphe de Connaissances"
description: "Extracting an entity-relationship graph from a corpus at index time and querying it alongside vector search to answer multi-hop questions vector retrieval alone cannot resolve."
description_fr: "Extraire un graphe entités-relations d'un corpus à l'indexation puis l'interroger en complément de la recherche vectorielle pour répondre à des questions multi-sauts que la recherche vectorielle seule ne résout pas."
domain: "03-rag-architectures"
tags: [rag, retrieval, knowledge-graph, engineering]
maturity: "experimental"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["bash", "python"]
updated: "2026-08-25"
---



## Prerequisites
- A corpus with meaningful entity relationships (org charts, incident timelines, regulatory dependencies) — GraphRAG adds cost that is not justified for loosely-connected document sets.
- A graph store (Neo4j, or an in-memory `networkx` graph for smaller corpora) alongside the existing vector store.

## Usage
### Architectural Purpose
Standard chunk-based RAG retrieves passages that are semantically similar to the query, which fails on questions requiring synthesis across multiple documents — e.g. "which services depend on the auth module that had an incident in March?" has no single chunk containing the full answer. GraphRAG addresses this by extracting a structured entity-relationship graph at index time, so multi-hop questions can be answered by graph traversal rather than hoping the right combination of chunks lands in one similarity-search result set.

---

### 1. Indexing: Chunk-and-Vector Path vs Graph Path

```text
                     +------------------+
                     |   Source Corpus   |
                     +--------+---------+
                              |
              +---------------+---------------+
              |                               |
     +--------v--------+           +----------v----------+
     | Chunk + Embed    |           | Entity/Relation      |
     | (existing RAG)    |           | Extraction (LLM pass)|
     +--------+---------+           +----------+----------+
              |                               |
     +--------v--------+           +----------v----------+
     |  Vector Store    |           |    Graph Store       |
     +------------------+           +-----------------------+
```

Entity extraction runs once per document at index time (LLM call per chunk or per document, extracting `(subject, relation, object)` triples), not at query time — the cost is amortized across all future queries.

---

### 2. Query-Time Hybrid Retrieval

```python
def graphrag_retrieve(query: str, top_k_vector: int = 10) -> str:
    # 1. Standard vector retrieval for broad relevant context
    vector_hits = vector_store.similarity_search(query, k=top_k_vector)

    # 2. Extract query entities, traverse graph for structured relationships
    query_entities = extract_entities(query)  # LLM or NER pass
    graph_facts = []
    for entity in query_entities:
        graph_facts += graph_store.traverse(entity, max_hops=2)

    # 3. Combine: unstructured passages + structured relationship facts
    return format_context(vector_hits, graph_facts)
```

The graph traversal supplies precise relationship facts ("Service X depends on Module Y") that a vector search would only surface if a single chunk happened to state that relationship explicitly.

---

### 3. Cost, Latency & Trade-offs

- **Indexing cost**: entity extraction is an LLM call per document (or per chunk for finer granularity) — for a 10,000-document corpus this is a materially larger one-time indexing bill than embedding alone. Budget for it explicitly; do not add GraphRAG to a corpus you re-index frequently without amortizing this cost.
- **Maintenance complexity**: the graph needs incremental updates as documents change (stale entities/relationships are worse than no graph at all — they produce confidently wrong multi-hop answers). Treat graph staleness as a first-class monitored metric, same as vector index freshness.
- **When to use it**: only when the failure mode is specifically "answer requires combining facts scattered across documents" — verified via a [golden-dataset regression set](../../09-evaluations-and-observability/golden-dataset-regression-testing/SKILL.md) of multi-hop questions that a vector-only baseline demonstrably fails. Do not adopt GraphRAG on the assumption it improves generic retrieval quality; it targets a specific failure class.

## Inputs
- Corpus with extractable entities and relationships.
- User query, from which entities are extracted at query time for graph traversal.

## Outputs
- Combined context: unstructured passages from vector search plus structured relationship facts from graph traversal.
- A graph store that must be kept in sync with document updates via an incremental extraction job.
