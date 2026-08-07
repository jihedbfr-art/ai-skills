---
name: quantization-gguf-awq-tuning
description: Architectural guidelines for running local LLMs using GGUF and AWQ quantization formats to balance VRAM usage and model precision.
version: 1.0.0
---

# LLM Quantization: GGUF & AWQ

## Architectural Purpose
Running unquantized LLMs (FP16/FP32) requires massive VRAM, making local deployment prohibitively expensive. Quantization reduces the precision of model weights (e.g., to 4-bit or 8-bit), drastically lowering VRAM requirements while maintaining near-original reasoning capabilities.

---

## 1. Quantization Formats Comparison

| Format | Execution Target | Use Case |
| :--- | :--- | :--- |
| **GGUF** (llama.cpp) | CPU & Apple Silicon (Metal) | Best for local development on MacBooks or servers lacking high-end GPUs. Supports offloading partial layers to GPU. |
| **AWQ / EXL2** | NVIDIA GPU (CUDA) | Best for production inference servers (vLLM) with dedicated NVIDIA hardware. Extremely fast token generation. |
| **FP16** | Unquantized | Baseline model precision. Highest VRAM requirement. |

---

## 2. VRAM Calculation Math (Rule of Thumb)

- **Formula**: `(Model Params in Billions) * (Bit Precision / 8) * 1.2 (Overhead)`
- **Example**: Llama-3 8B at 4-bit (Q4_K_M GGUF):
  - $8 \times (4 / 8) \times 1.2 = 4.8 \text{ GB VRAM}$
  - A standard 8GB RTX GPU or M1 Mac can easily run it.

---

## 3. Cost, Latency & Trade-offs
- **Token Math**: Quantization does not affect token pricing (if self-hosted), but heavily impacts generation speed (tokens/sec).
- **Latency Penalty**: CPU-only GGUF inference is slow (5-15 tok/s). AWQ on GPU can hit 100+ tok/s.
- **Trade-off (Perplexity)**: Going below 4-bit (e.g., 2-bit or 3-bit) severely degrades the model's ability to follow complex JSON schemas or write accurate code. 4-bit (Q4_K_M) is the universally accepted sweet spot.

---

## 4. Verification Checklist
- [ ] Ensure local inference server (Ollama, vLLM, text-generation-webui) matches the hardware architecture (CUDA vs Metal).
- [ ] Monitor VRAM spikes during context processing to prevent Out Of Memory (OOM) crashes.
- [ ] Validate structured JSON output reliability; heavy quantization can break formatting compliance.
