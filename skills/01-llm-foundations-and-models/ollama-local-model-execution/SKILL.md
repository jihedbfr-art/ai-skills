---
format: "v2"
name: "ollama-local-model-execution"
title: "Ollama: Local Model Execution"
title_fr: "Ollama : exécution de modèles en local"
description: "Running models on your own hardware with Ollama: installation, model pulling, and the memory arithmetic that decides which quantization actually fits."
description_fr: "Faire tourner des modèles sur sa propre machine avec Ollama : installation, récupération des modèles, et le calcul mémoire qui décide de la quantification qui tient réellement."
domain: "01-llm-foundations-and-models"
tags: [ollama, local-ai, on-premise, engineering]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["bash", "ollama"]
updated: "2026-09-02"
---

## Prerequisites
- Linux, macOS, or WSL2, with enough free RAM or VRAM for the target model.
- Data that must not leave the machine. Otherwise a hosted API is cheaper and faster.

## Usage

### Architectural Context

Enterprise AI adoption is frequently blocked by data sovereignty, GDPR constraints, and air-gapped network requirements. Ollama resolves these blockers by providing a lightweight, extensible runtime for executing Large Language Models entirely locally (on-premise). 

Ollama abstracts away the complex C++ and CUDA bindings required to run models on GPUs, providing a clean REST API (running by default on `http://localhost:11434`) that is perfectly compatible with the OpenAI SDK.

### 1. Execution Directives (Agent Instructions)

1. **Security First:** Local models guarantee zero data exfiltration. If a task involves PII (Personally Identifiable Information) or proprietary source code, the agent MUST route the task to an Ollama-hosted model rather than a Cloud API.
2. **Hardware Profiling:** Before invoking a local model, an agent must assess the host's VRAM. Attempting to load a 70B parameter model on a 16GB VRAM machine will result in extreme Out-Of-Memory (OOM) errors or agonizingly slow CPU offloading.

### 2. Bash Hook: Installation & Model Pulling

```bash
# examples/install_ollama.sh

# 1. Install Ollama (Linux/WSL2)
curl -fsSL https://ollama.com/install.sh | sh

# 2. Start the daemon in the background (if not running as a systemd service)
# ollama serve &

# 3. Pull a highly capable, lightweight model (e.g., Llama 3 8B or Gemma 2 9B)
ollama pull llama3
ollama pull gemma2

# 4. Verify API is running
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

### 3. The `Modelfile` Standard

Ollama uses a `Modelfile` (similar to a `Dockerfile`) to bake system prompts, temperature settings, and context window limits directly into a custom model artifact. This prevents agents from having to inject the same system prompt repeatedly.

```text
# examples/Modelfile.secure_coder
FROM llama3

# Set parameters
PARAMETER temperature 0.1
PARAMETER num_ctx 8192

# Set the system prompt
SYSTEM """
You are a senior DevSecOps engineer. 
Analyze the following code strictly for security vulnerabilities (SQL injection, XSS). 
Do not output conversational text. Output only a JSON array of vulnerabilities.
"""
```

To build and run:
```bash
ollama create devsecops-agent -f Modelfile.secure_coder
ollama run devsecops-agent
```

### 4. Integration with the OpenAI SDK

Ollama's REST API is drop-in compatible with the OpenAI standard. This means you do not need a custom SDK to query local models.

```python
# examples/ollama_openai_compat.py
from openai import OpenAI

# Point the client to the local Ollama instance
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama', # Required field, but ignored by Ollama
)

response = client.chat.completions.create(
    model="llama3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in one sentence."}
    ]
)

print(response.choices[0].message.content)
```

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The model and quantization to run, and the memory budget available.

## Outputs
- A local inference endpoint on port 11434, and the served model.
