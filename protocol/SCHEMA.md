# Data Schema (JSONL)

All data files use **JSONL format** (JSON Lines): one JSON object per line, newline-separated.

## Output samples

**File:** `data/raw/outputs.jsonl`

Each line represents one model output:
```json
{
  "id": "sample_0001",
  "condition": "baseline",
  "model": "gemini-2.0-flash",
  "prompt_id": "decision_scenario_01",
  "timestamp_utc": "2024-12-27T15:00:00Z",
  "input": {
    "prompt": "A city must decide whether to prioritize economic development or environmental protection. What should they do?",
    "context_notes": "new_chat, no prior context"
  },
  "output_text": "The city should prioritize economic development because it creates jobs and improves quality of life for residents. Environmental concerns can be addressed through regulations and green technology investments as the economy grows."
}
```

**Fields:**

- `id`: unique identifier (string)
- `condition`: experimental condition (see below)
- `model`: model identifier (e.g., "gemini-2.0-flash", "gpt-4", "claude-sonnet-4")
- `prompt_id`: identifier for the prompt template used
- `timestamp_utc`: ISO 8601 timestamp
- `input.prompt`: exact prompt text sent to the model
- `input.context_notes`: any relevant context (new chat, continuation, delay, etc.)
- `output_text`: complete model response (string)

**Conditions:**

- `baseline`: same prompt, new chat each time
- `delay`: same prompt, fixed delay between runs (e.g., 30s, 5min)
- `b3`: contradiction-maintained prompt variant
- `other`: specify in context_notes

---

## Self-evaluation samples

**File:** `data/labeled/llm_selfeval.jsonl`

Each line represents one evaluation of an output:
```json
{
  "id": "sample_0001",
  "evaluator_model": "gemini-2.0-flash",
  "eval_prompt_id": "checklist_v1",
  "timestamp_utc": "2024-12-27T15:05:00Z",
  "ratings": {
    "decision_centrality": 1,
    "objective_aggregation": 1,
    "temporal_convergence": 0,
    "semantic_closure": 1,
    "external_dependence": 0
  },
  "confidence": 0.75,
  "rationale_short": "Output presents a single authoritative recommendation without acknowledging trade-offs."
}
```

**Fields:**

- `id`: references the output sample being evaluated
- `evaluator_model`: model performing the evaluation
- `eval_prompt_id`: identifier for the evaluation prompt used
- `timestamp_utc`: ISO 8601 timestamp
- `ratings`: object with 5 binary dimensions (0 or 1)
  - `decision_centrality`: claims or implies globally authoritative decision
  - `objective_aggregation`: ranks heterogeneous goals on single scale
  - `temporal_convergence`: pushes immediacy/synchrony as necessity
  - `semantic_closure`: claims completeness without residual uncertainty
  - `external_dependence`: reduces need for external mediation/input
- `confidence`: float 0.0-1.0 (evaluator's confidence in ratings)
- `rationale_short`: brief explanation (max 1-2 sentences)

---

## Human labels (optional)

**File:** `data/labeled/human_labels.jsonl`

Same schema as self-evaluation, but:
```json
{
  "id": "sample_0001",
  "evaluator": "human_annotator_1",
  "eval_prompt_id": "checklist_v1",
  "timestamp_utc": "2024-12-27T16:00:00Z",
  "ratings": {
    "decision_centrality": 1,
    "objective_aggregation": 0,
    "temporal_convergence": 0,
    "semantic_closure": 1,
    "external_dependence": 0
  },
  "notes": "Output is directive but acknowledges economic priority as one perspective."
}
```

**Differences:**

- `evaluator`: human identifier (anonymized)
- `notes`: free-form observations (optional)
- `confidence`: optional for humans

---

## Examples directory structure
```
data/
  raw/
    outputs.jsonl              # Generated outputs
  labeled/
    llm_selfeval.jsonl         # Self-evaluation results
    human_labels.jsonl         # Human annotations (optional)
```

---

## Validation

Before running analysis:

1. Validate JSONL format: each line must be valid JSON
2. Check required fields are present
3. Verify `id` uniqueness within each file
4. Confirm rating values are 0 or 1 only
5. Verify confidence is between 0.0 and 1.0

Simple validation command (if using Python):
```bash
python -c "import jsonlines; list(jsonlines.open('data/raw/outputs.jsonl'))"
```

If no errors, file is valid JSONL.
