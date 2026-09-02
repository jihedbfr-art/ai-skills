---
format: "v2"
name: "deepseek-r1-reasoning-heuristics"
title: "DeepSeek-R1: Prompting a Reinforcement-Learned Reasoner"
title_fr: "DeepSeek-R1 : prompter un raisonneur entraîné par renforcement"
description: "R1 was trained by reinforcement learning to find its own reasoning path, which is why system prompts and few-shot examples degrade it. What to send instead, and what it costs to self-host."
description_fr: "R1 a été entraîné par renforcement pour trouver son propre chemin de raisonnement, et c'est pourquoi les prompts système et les exemples few-shot le dégradent. Ce qu'il faut envoyer à la place, et ce que coûte l'auto-hébergement."
domain: "15-frontier-models-and-trends"
tags: [frontier-models, reasoning, ollama, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["bash", "ollama"]
updated: "2026-09-02"
---

## Prerequisites
- Ollama 0.1.27 or later, and the VRAM the chosen distillation actually needs.
- Willingness to drop the prompt scaffolding that helps every other model.

## Usage

### Context

DeepSeek-R1 is fundamentally different from traditional Supervised Fine-Tuned (SFT) models. It was trained using massive Reinforcement Learning (RL) to develop autonomous reasoning paths. Standard prompting techniques (like system prompts or few-shot examples) disrupt its internal Chain of Thought (CoT), leading to hallucinations or logic bypass.

### 1. Execution Directives (Agent Instructions)

When invoking or orchestrating DeepSeek-R1, you **MUST** adhere to the following rules:

1. **NO System Prompt:** Do not provide a system prompt. Inject all instructions, context, and constraints exclusively into the user message.
2. **Strict Temperature:** Set the inference temperature strictly between `0.5` and `0.7` (Optimal: `0.6`). Setting it to `0.0` will cause infinite loops within the `<think>` tags.
3. **Top P:** Set `top_p` to `0.95`.
4. **Step-by-Step Enclosure:** For mathematical or formal logic queries, append the following directive to the user message:
   *"Please reason step by step, and put your final answer within \boxed{}."*

### 2. Ollama Deployment Hook

The following configuration enforces these heuristics at the runtime level.

```bash
# install_deepseek_r1_local.sh
cat << 'EOF' > Modelfile.r1
FROM deepseek-r1:14b
PARAMETER temperature 0.6
PARAMETER top_p 0.95
# System prompt is intentionally omitted
EOF

ollama create r1-optimized -f Modelfile.r1
ollama run r1-optimized
```

### 3. Financial & Hardware Considerations

For local edge deployments, select the distilled version based on available VRAM:
- **8B (Llama):** ~8GB VRAM (Edge AI)
- **14B (Qwen):** ~16GB VRAM (Optimal balance for coding)
- **32B (Qwen):** ~24GB VRAM (Advanced programming)
- **70B (Llama):** 48GB+ VRAM (Server-grade research)

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The question, stated plainly, with no system prompt and no few-shot examples.

## Outputs
- The model's reasoning trace and its answer, kept separable so only the answer reaches the user.
