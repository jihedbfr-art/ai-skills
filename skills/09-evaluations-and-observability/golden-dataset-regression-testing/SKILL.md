---
format: "v2"
name: "golden-dataset-regression-testing"
title: "Golden Dataset Regression Testing"
title_fr: "Tests de Non-Régression sur Jeu de Données Étalon"
description: "Maintaining a versioned, curated set of input/expected-output pairs to catch quality regressions on every prompt or model change before deployment."
description_fr: "Maintenir un ensemble versionné et curé de paires entrée/sortie attendue pour détecter les régressions de qualité à chaque changement de prompt ou de modèle avant déploiement."
domain: "09-evaluations-and-observability"
tags: [evaluation, testing, engineering, ci-cd]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "qa-engineer"]
requires: ["bash", "git", "python"]
updated: "2026-08-25"
---



## Prerequisites
- A CI pipeline capable of running a batch script and failing the build on a threshold breach.
- Production or synthetic examples covering the system's known edge cases, not just the happy path.

## Usage
### Architectural Purpose
Unlike deterministic software, an LLM-backed feature has no fixed correct output to diff against. A golden dataset substitutes a curated set of representative (input, expected-behavior) pairs with per-case assertions, so that a prompt tweak, model upgrade, or RAG index rebuild cannot silently degrade quality between merges — the same role unit tests play for deterministic code, adapted to probabilistic outputs.

---

### 1. Dataset Composition

```text
golden-set.jsonl
├── 40% happy path        (typical, well-formed user requests)
├── 30% edge cases         (empty input, contradictory instructions, huge input)
├── 20% known past failures (every production incident becomes a permanent case)
└── 10% adversarial        (prompt injection attempts, off-topic requests)
```

Every production incident that reaches a postmortem gets a corresponding golden case added in the same PR that fixes it — this is what prevents fixed bugs from silently reappearing after unrelated changes.

---

### 2. Per-Case Assertion Types

Not every case needs an LLM judge — cheaper, deterministic assertions should be preferred whenever the property is checkable in code:

```python
@dataclass
class GoldenCase:
    id: str
    input: str
    assertion_type: Literal["exact", "contains", "regex", "schema", "llm_judge"]
    expected: str | dict
    severity: Literal["blocker", "warning"]

def evaluate_case(case: GoldenCase, actual_output: str) -> bool:
    match case.assertion_type:
        case "exact":   return actual_output.strip() == case.expected
        case "contains":return case.expected in actual_output
        case "regex":   return bool(re.search(case.expected, actual_output))
        case "schema":  return validate_json_schema(actual_output, case.expected)
        case "llm_judge": return llm_judge_pass(case.input, actual_output, case.expected)
```

Reserve `llm_judge` for genuinely subjective properties (tone, helpfulness); prefer `schema`/`regex`/`contains` for anything with a checkable structural property — they are free, instant, and have zero judge variance.

---

### 3. CI Gate Policy

- **`blocker` cases**: any failure fails the build — reserved for regressions that reached production before (prevents recurrence).
- **`warning` cases**: aggregate pass-rate must stay within a tolerance band (e.g. no more than 2 percentage points below the baseline on `main`) — catches gradual drift without blocking on single-case noise inherent to LLM outputs.
- **Baseline tracking**: store the last-known-good pass rate per case category in the repo (`golden-baseline.json`) and diff against it on every run, rather than hard-coding a static threshold that goes stale as the dataset grows.

## Inputs
- Versioned golden dataset file (`golden-set.jsonl`) checked into the repository.
- The candidate prompt/model/pipeline configuration under test.

## Outputs
- Pass/fail per case plus an aggregate pass-rate delta against the stored baseline.
- A CI status check that blocks merge on `blocker` regressions and flags `warning` drift for review.
