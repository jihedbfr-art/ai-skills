---
format: "v2"
name: "chromadb-persistent-collections"
title: "ChromaDB: Persistent Collections and Distance Metrics"
title_fr: "ChromaDB : collections persistantes et métriques de distance"
description: "Running ChromaDB with storage that survives a restart, choosing the distance metric deliberately, and knowing the point where an embedded store stops being the right answer."
description_fr: "Faire tourner ChromaDB avec un stockage qui survit au redémarrage, choisir la métrique de distance en connaissance de cause, et savoir à quel moment un store embarqué cesse d'être la bonne réponse."
domain: "07-vector-databases-and-embeddings"
tags: [vector-db, chroma, embeddings, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["python"]
updated: "2026-09-02"
---

## Prerequisites
- Python 3.9 or later with chromadb 0.5 or later.
- A writable directory for persistence: the default client keeps everything in memory and loses it on exit.

## Usage

### Architectural Context

In a Retrieval-Augmented Generation (RAG) architecture, LLMs need a way to search through enterprise documents based on meaning (semantics) rather than exact keywords. ChromaDB is an open-source, AI-native vector database that stores text alongside its mathematical representation (embeddings). It is incredibly popular because it can run in-memory or as a local persistent database, avoiding the latency and cost of cloud-hosted vector databases like Pinecone.

### 1. Execution Directives (Agent Instructions)

- **Embedding Models:** Never store raw text without an embedding model. Use `text-embedding-3-small` (OpenAI) or `nomic-embed-text` (Ollama) to convert text into vectors before insertion.
- **Distance Metrics:** By default, Chroma uses L2 (Squared Euclidean) distance. For cosine similarity (often preferred by OpenAI embeddings), configure the collection explicitly: `metadata={"hnsw:space": "cosine"}`.

### 2. Python Hook: Persistent Storage

```python
import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize persistent storage (keeps data across reboots)
client = chromadb.PersistentClient(path="./chroma_db_storage")

# 2. Define the embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="sk-...",
    model_name="text-embedding-3-small"
)

# 3. Create or Get a Collection (with Cosine Similarity)
collection = client.get_or_create_collection(
    name="enterprise_documents",
    embedding_function=openai_ef,
    metadata={"hnsw:space": "cosine"}
)

# 4. Ingestion (Upsert)
collection.upsert(
    documents=[
        "The transactional outbox pattern prevents dual-write failures.",
        "Saga orchestration is preferred over choreography in complex telecom BSS."
    ],
    metadatas=[{"source": "adr-003"}, {"source": "adr-004"}],
    ids=["doc1", "doc2"]
)

# 5. Semantic Query
results = collection.query(
    query_texts=["How do I avoid dual write issues in telecom?"],
    n_results=1
)

print(results["documents"])
```

## Inputs
- The documents to index, the embedding function, and the distance metric.

## Outputs
- A persistent collection on disk, and similarity results ordered by the chosen metric.
