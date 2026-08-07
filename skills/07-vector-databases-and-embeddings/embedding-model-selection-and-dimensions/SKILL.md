---
name: embedding-model-selection-and-dimensions
description: Architectural guidelines for selecting embedding models based on vector dimensionality, multilingual support, and storage constraints.
version: 1.0.0
---

# Embedding Model Selection & Dimensions

## Architectural Purpose
The choice of an embedding model dictates the retrieval accuracy of a RAG system and the storage cost in the vector database. High-dimensional vectors offer better semantic nuance but require significantly more RAM/Storage and increase distance calculation latency.

---

## 1. Core Model Comparison

| Model | Dimensions | Target Use Case | Pros | Cons |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI `text-embedding-3-small`** | 1536 (configurable down to 256) | General purpose English RAG. | Cheap, highly performant. | Cloud API dependency. |
| **OpenAI `text-embedding-3-large`** | 3072 | Complex legal/medical corpus. | High precision. | Massive storage bloat (3072 dims). |
| **Cohere `embed-multilingual-v3.0`** | 1024 | Multilingual RAG (French, Arabic, EN). | Natively supports 100+ languages. | Proprietary API. |
| **BGE-M3 (BAAI)** | 1024 | Self-hosted Multilingual. | Open weights, runs locally. | Requires GPU for fast encoding. |
| **MiniLM-L6-v2** | 384 | Edge devices / Extreme cost constraints. | Tiny footprint, blazingly fast. | Poor on complex/long contexts. |

---

## 2. Cost, Latency & Trade-offs
- **Storage Math**: 1 million vectors at 1536 dimensions (FLOAT32) = $1,000,000 \times 1536 \times 4 \text{ bytes} \approx 6.14 \text{ GB}$ of RAM/Disk just for the embeddings.
- **Latency Penalty**: Cosine similarity calculations scale linearly with vector dimensions. A 3072-dimensional vector takes 2x longer to compare than a 1536-dimensional vector.
- **Trade-off (Matryoshka Representation)**: Models like `text-embedding-3` support truncation (e.g., slicing the 1536 vector to 512 dimensions). This saves 66% storage at the cost of only ~2% retrieval accuracy drop.

---

## 3. Verification Checklist
- [ ] Multilingual RAG projects strictly use models trained on multiple languages (e.g., Cohere or BGE-M3), not English-only models.
- [ ] PGVector table column types explicitly match the embedding model dimensions (e.g., `vector(1536)`).
- [ ] Avoid changing embedding models post-launch; doing so requires re-embedding the entire document database.
