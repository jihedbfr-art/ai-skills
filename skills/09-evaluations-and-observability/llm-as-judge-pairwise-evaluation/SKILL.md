---
format: "v2"
name: "llm-as-judge-pairwise-evaluation"
title: "LLM As Judge Pairwise Evaluation"
title_fr: "LLM-Juge en Évaluation Comparative"
description: "Using an LLM to compare two candidate outputs (A/B) against a rubric instead of scoring each in isolation, to reduce judge score variance."
description_fr: "Utiliser un LLM pour comparer deux sorties candidates (A/B) selon une grille plutôt que de les noter isolément, afin de réduire la variance du jugement."
domain: "09-evaluations-and-observability"
tags: [evaluation, llm-judge, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["bash", "python"]
updated: "2026-08-25"
---



## Prerequisites
- At least two candidate outputs to compare per input (two model versions, two prompts, or two RAG configs).
- A written rubric — pairwise judging without a rubric degenerates into "which one sounds nicer."

## Usage
### Architectural Purpose
Absolute scoring ("rate this answer 1-10") suffers from severe judge drift: the same LLM scores the same answer differently across runs, and score distributions cluster near the top (leniency bias). Pairwise comparison ("which of A or B better satisfies the rubric") is a much easier and more stable judgment task for an LLM, and directly answers the question that matters in practice: did the change make things better or worse.

---

### 1. Pairwise Judge Protocol

```text
+----------+     +----------+
| Output A |     | Output B |
+----+-----+     +-----+----+
     |                 |
     +--------+--------+
              |
       +------v------+
       |   Judge LLM  |  <- rubric + input + A + B, order randomized
       +------+------+
              |
      {"winner": "A"|"B"|"tie", "reason": str}
```

1. **Randomize position**: always shuffle which output is labeled A vs B per call — LLM judges exhibit measurable position bias (first-listed option wins more often, all else equal). Run each pair twice with positions swapped and require agreement to accept the verdict, or split the difference on disagreement.
2. **Rubric, not vibes**: the rubric lists concrete, checkable criteria (e.g. "cites a source for every numeric claim", "does not use APIs deprecated after v2.0"), not subjective adjectives.
3. **Force a reason**: require the judge to justify the winner in one sentence referencing the rubric. Verdicts without a rubric-grounded reason are discarded as noise, not counted.

---

### 2. Minimal Implementation

```python
def judge_pair(input_text: str, output_a: str, output_b: str, rubric: str) -> dict:
    prompt = f"""RUBRIC:\n{rubric}\n\nINPUT:\n{input_text}\n\n
OUTPUT A:\n{output_a}\n\nOUTPUT B:\n{output_b}\n\n
Return JSON: {{"winner": "A"|"B"|"tie", "reason": "<one sentence citing the rubric>"}}"""
    resp = client.messages.create(model=JUDGE_MODEL, max_tokens=200,
                                   messages=[{"role": "user", "content": prompt}])
    return json.loads(resp.content[0].text)

def judge_pair_debiased(input_text, output_a, output_b, rubric) -> str:
    r1 = judge_pair(input_text, output_a, output_b, rubric)
    r2 = judge_pair(input_text, output_b, output_a, rubric)  # swapped
    w1 = r1["winner"]
    w2 = {"A": "B", "B": "A", "tie": "tie"}[r2["winner"]]  # normalize back to A/B space
    return w1 if w1 == w2 else "tie"  # disagreement across swap -> treat as tie
```

---

### 3. Aggregating Pairwise Results into a Ranking

For more than two candidates, run all-pairs comparisons and convert win/loss counts into a ranking (Bradley-Terry model or simple win-rate) rather than trying to get the judge to rank N items in one call — LLMs handle binary comparisons far more reliably than simultaneous N-way ranking, especially past 3-4 items.

## Inputs
- The original task input.
- Two candidate outputs and a rubric describing what "better" means for this task.

## Outputs
- A winner label (`A`, `B`, or `tie`) with a rubric-grounded justification, position-debiased via the swap-and-compare protocol.
- Aggregate win-rate deltas usable as a regression gate in CI (e.g. "reject if new prompt loses >55% of pairwise comparisons against the current production prompt").
