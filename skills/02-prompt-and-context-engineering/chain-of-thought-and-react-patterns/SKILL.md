---
name: chain-of-thought-and-react-patterns
description: Implementation guidelines for structural reasoning using Chain-of-Thought (CoT) and ReAct (Reasoning and Acting) prompting techniques.
version: 1.0.0
---

# Chain-of-Thought & ReAct Prompting

## Architectural Purpose
Zero-shot prompting often fails on complex reasoning tasks because the LLM lacks a "scratchpad" to work out intermediate steps. Forcing the model to emit a reasoning chain before outputting the final answer significantly improves accuracy in math, logic, and multi-step tool orchestration.

---

## 1. Core Pattern / Implementation

### Zero-Shot CoT
Simply appending `"Let's think step by step"` or enforcing XML thought blocks:

```xml
<system_instructions>
Before providing your final answer, you MUST write out your reasoning step-by-step inside <thought> tags. 
Only output the final answer inside <answer> tags.
</system_instructions>
```

### ReAct (Reasoning + Acting)
Used for agentic tool calling loops. The model loops through: `Thought -> Action -> Observation -> Thought -> Final Answer`.

```text
Thought: I need to find the customer's current balance to calculate the refund. I will use the get_balance tool.
Action: get_balance({"customer_id": "123"})
Observation: 450.00
Thought: The balance is 450.00. The requested refund is 100.00. I can process it.
Action: process_refund({"customer_id": "123", "amount": 100.00})
Observation: Success
Thought: The refund is processed. I can now inform the user.
Final Answer: I have successfully processed your refund of $100.00.
```

---

## 2. Cost, Latency & Trade-offs
- **Token Math**: CoT heavily inflates output token consumption. A 50-token answer might require 300 tokens of intermediate reasoning.
- **Latency Penalty**: TTFT (Time-To-First-Token) for the final answer is delayed because the model must stream the entire `<thought>` block first.
- **Trade-off**: Do not use CoT for simple extraction or classification tasks where low latency is critical. Reserve it for complex routing or math.

---

## 3. Verification Checklist
- [ ] UI frontend strips out `<thought>` blocks so the end-user only sees the final `<answer>`.
- [ ] System prompt strictly enforces the structure to prevent the model from leaking thoughts into the final answer.
- [ ] ReAct agents have a strict `max_iterations` limit to prevent infinite Action/Observation loops.
