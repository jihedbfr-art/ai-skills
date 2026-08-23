---
format: "v2"
name: "ragas-evaluation-metrics"
title: "Ragas Evaluation Metrics"
title_fr: "RAGAS Evaluation Metrics"
description: "Quantitative evaluation framework for RAG systems using Faithfulness, Answer Relevancy, and Context Precision metrics."
description_fr: "Cadre d'évaluation quantitative pour les systèmes RAG basé sur les métriques Faithfulness, Answer Relevancy et Context Precision."
domain: "09-evaluations-and-observability"
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
Evaluating RAG systems using subjective human inspection is non-scalable and prone to bias. The RAGAS framework provides continuous automated scoring of RAG pipelines across 4 core dimensions.

---

### 1. The RAG Triad Metrics

```text
               +-------------------+
               |    User Query     |
               +---------+---------+
                         |
           +-------------+-------------+
           |                           |
+----------v----------+     +----------v----------+
|  Retrieved Context  |     | Generated Response  |
+---------------------+     +---------------------+
```

### 1. Context Precision
Measures whether all ground-truth relevant items are ranked at the top of retrieved chunks.

### 2. Context Recall
Measures whether the retrieved context contains all information required to answer the query.

### 3. Faithfulness (Factuality)
Measures if the generated answer is strictly grounded in the retrieved context (detects hallucinations).

### 4. Answer Relevancy
Measures how directly the generated answer addresses the user's initial question.

---

### 2. Python RAGAS Execution Example

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

data_sample = {
    'question': ['How do I configure Spring AI PGVector store?'],
    'contexts': [['Spring AI provides SpringBoot starter for PGVector with HNSW index support...']],
    'answer': ['Include the spring-ai-pgvector-store dependency and configure jdbc url.'],
    'ground_truth': ['Use spring-ai-pgvector-store-spring-boot-starter with PGVector database URL.']
}

dataset = Dataset.from_dict(data_sample)
score = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
print(score)
```

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.