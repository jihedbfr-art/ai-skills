---
format: "v2"
name: "langchain-lcel-chaining-patterns"
title: "LangChain Expression Language: Chaining Patterns"
title_fr: "LangChain Expression Language : patterns de chaînage"
description: "The Runnable protocol behind LCEL, and the composition patterns (sequential, parallel, branching) that make a pipeline streamable and debuggable rather than a nest of callbacks."
description_fr: "Le protocole Runnable derrière LCEL, et les patterns de composition (séquentiel, parallèle, branchement) qui rendent un pipeline streamable et débogable au lieu d'un nid de callbacks."
domain: "04-agentic-workflows"
tags: [langchain, pipelines, orchestration, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["python"]
updated: "2026-09-02"
---

## Prerequisites
- Python 3.9 or later with langchain 0.2 or later.
- A model provider already configured, since every example below ends in an actual call.

## Usage

### Architectural Context

Traditional LangChain relied heavily on pre-built monolithic classes (e.g., `LLMChain`, `ConversationalRetrievalChain`). These abstracted away too much logic, making debugging and customization exceptionally difficult. LangChain Expression Language (LCEL) completely replaced this paradigm. LCEL is a declarative methodology that relies on standard Python protocols (the `Runnable` interface) to pipe components together using the UNIX-like `|` operator. 

### 1. The Runnable Protocol

Every component in LCEL implements the `Runnable` protocol, exposing standard methods:
- `invoke()`: Synchronous execution.
- `ainvoke()`: Asynchronous execution.
- `stream()`: Stream the output chunks.
- `batch()`: Execute on a list of inputs in parallel.

### 2. Basic Pipeline Architecture

The most fundamental LCEL chain connects a Prompt Template, an LLM, and an Output Parser.

```python
# examples/lcel_basic.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Define the components
prompt = ChatPromptTemplate.from_template("Summarize the following incident report in {language}:\n\n{report}")
model = ChatOpenAI(model="gpt-4o")
parser = StrOutputParser()

# 2. Pipe them together using LCEL
chain = prompt | model | parser

# 3. Invoke the chain
result = chain.invoke({
    "language": "French",
    "report": "At 14:00 UTC, the primary database node failed due to a sudden spike in I/O..."
})

print(result)
```

### 3. Advanced Pattern: Parallel Execution (RunnableParallel)

When an agent needs to perform multiple tasks simultaneously before combining the results, use `RunnableParallel`. This is highly effective for tasks like generating a title and a summary concurrently from the same source text.

```python
# examples/lcel_parallel.py
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

title_prompt = ChatPromptTemplate.from_template("Write a clickbait title for this text: {text}")
summary_prompt = ChatPromptTemplate.from_template("Write a 2-sentence summary of this text: {text}")

# Two separate sub-chains
title_chain = title_prompt | model | parser
summary_chain = summary_prompt | model | parser

# Parallel execution map
map_chain = RunnableParallel(
    title=title_chain,
    summary=summary_chain
)

# Usage: 
# Using RunnablePassthrough allows the input string to be passed directly as the "text" variable
final_chain = {"text": RunnablePassthrough()} | map_chain

output = final_chain.invoke("The new quantum computer achieved supremacy in 3 minutes...")
# Output: {'title': 'You Won't Believe What This Quantum Computer Did In 3 Minutes!', 'summary': 'A new quantum computer has reached supremacy. It completed the benchmark in just 3 minutes.'}
```

### 4. Execution Directives (Agent Constraints)

When generating LangChain pipelines:
1. **Never use legacy chains:** Do not instantiate `LLMChain` or `SequentialChain`. Always construct the pipeline using LCEL (`|`).
2. **Streaming by Default:** For production interfaces, prefer `chain.astream()` over `chain.invoke()` to reduce perceived latency for the end user.
3. **Typing:** Ensure all output parsers are robust. If the pipeline extracts JSON, use `JsonOutputParser` and inject the Pydantic schema into the prompt template using partial variables.

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The steps of the pipeline: prompt, model, parser, and any retrieval in between.

## Outputs
- A composed Runnable that streams, batches, and reports which step failed.
