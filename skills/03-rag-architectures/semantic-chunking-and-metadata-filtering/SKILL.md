---
name: semantic-chunking-and-metadata-filtering
description: Advanced RAG strategies using semantic document chunking and exact-match metadata filtering to improve retrieval precision.
version: 1.0.0
---

# Semantic Chunking & Metadata Filtering

## Architectural Purpose
Naive RAG chunks documents using fixed character counts (e.g., 1000 characters), which often slices sentences or code blocks in half, destroying context. Semantic chunking respects structural boundaries (paragraphs, markdown headers, JSON objects). Metadata filtering allows hard-filtering (e.g., `date > 2024`) before running expensive vector searches.

---

## 1. Core Pattern / Implementation

### Semantic Chunking (Markdown/HTML)
Instead of arbitrary splits, chunk by HTML headers or Markdown hierarchy (`#`, `##`):

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_document = "# Chapter 1\nSome text...\n## Section 1\nMore text..."
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
splits = splitter.split_text(markdown_document)
# Each chunk retains its header hierarchy in metadata:
# splits[0].metadata -> {"Header 1": "Chapter 1", "Header 2": "Section 1"}
```

### Pre-Filtering Vectors (PostgreSQL / PGVector)
Filter by exact criteria (tenant ID, date) *before* vector distance calculation:

```sql
SELECT document_id, content
FROM knowledge_chunks
WHERE tenant_id = 'org_123'             -- Exact match hard-filter
  AND doc_type = 'API_SPEC'
ORDER BY embedding <=> '[0.1, 0.2...]'::vector
LIMIT 5;
```

---

## 2. Cost, Latency & Trade-offs
- **Token Math**: Better chunking reduces the need to inject huge overlaps into the LLM context, saving input tokens.
- **Latency Penalty**: Metadata filtering with standard B-Tree indexes on `tenant_id` massively speeds up PGVector queries by restricting the vector scan surface area.
- **Trade-off**: Requires rigorous ingestion pipelines to accurately tag documents with metadata prior to embedding.

---

## 3. Verification Checklist
- [ ] Multi-tenant RAG systems strictly enforce `tenant_id` filtering in the SQL WHERE clause to prevent cross-tenant data leakage.
- [ ] Chunks have an overlap parameter (e.g., 100 tokens) to catch edge-case semantic bridges.
- [ ] Code snippets are never split mid-block; use language-aware splitters for source code.
