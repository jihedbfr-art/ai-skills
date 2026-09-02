---
format: "v2"
name: "langsmith-tracing-and-evaluation"
title: "LangSmith: Tracing and LLM-as-a-Judge Evaluation"
title_fr: "LangSmith : traçage et évaluation LLM-as-a-judge"
description: "Instrumenting an LLM application with LangSmith traces, then turning a dataset of expected answers into a repeatable LLM-as-a-judge evaluation."
description_fr: "Instrumenter une application LLM avec les traces LangSmith, puis transformer un jeu de réponses attendues en évaluation LLM-as-a-judge reproductible."
domain: "09-evaluations-and-observability"
tags: [evaluation, observability, tracing, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "qa-engineer"]
requires: ["python"]
updated: "2026-09-02"
---

## Prerequisites
- Python 3.9 or later, with a LangSmith API key exported in the environment.
- An application whose calls you can wrap, and a handful of questions with known-good answers.

## Usage

### Architectural Context

You cannot manage what you cannot measure. In deterministic programming, unit tests are binary (Pass/Fail). In stochastic AI programming, output is probabilistic. LangSmith provides tracing (seeing exactly what the LLM thought and what tools it called) and evaluation (scoring the LLM's answers against a dataset using another LLM as a judge).

### 1. Execution Directives (Agent Instructions)

- **Always Trace in Production:** Never deploy an LCEL chain or an OpenAI Swarm without tracing enabled. If the agent hallucinates, you need the trace to debug the exact prompt that caused the failure.
- **LLM-as-a-Judge:** Use a highly capable, slow model (GPT-4o) to evaluate the outputs of a fast, cheap model (Gemini Flash) during CI/CD.

### 2. Python Hook: Tracing

Enable tracing globally by setting environment variables. No code changes are required if using LangChain or the native OpenAI SDK wrapped with LangSmith.

```bash
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="ls__..."
export LANGCHAIN_PROJECT="jihedailabs-billing-agent"
```

### 3. Python Hook: Evaluation (LLM-as-a-Judge)

```python
from langsmith.evaluation import evaluate, LangChainStringEvaluator

# 1. Define the dataset in LangSmith (Questions and Expected Answers)
dataset_name = "Telecom_BSS_QnA"

# 2. Define the agent/chain to test
def my_agent(inputs: dict) -> dict:
    # Calls your LLM logic here
    return {"output": "The Outbox pattern prevents dual-write failures."}

# 3. Define the Evaluator (GPT-4o grading the agent's answer)
qa_evaluator = LangChainStringEvaluator("qa")

# 4. Run the evaluation suite
experiment_results = evaluate(
    my_agent,
    data=dataset_name,
    evaluators=[qa_evaluator],
    experiment_prefix="test-outbox-agent"
)

print("Evaluation complete. View results in the LangSmith dashboard.")
```

## Inputs
- The chain or agent under test, and a dataset of questions with expected answers.

## Outputs
- Traces for every run, and a scored evaluation that can gate a pull request.
