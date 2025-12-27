# LLM Self-Evaluation Protocol (Checklist-based)

## Goal

Test whether an LLM can **stably and consistently** evaluate structural "totalization" signals in LLM outputs, including its own.

**This is an evaluation protocol, not a safety mechanism.**

---

## Inputs

A dataset of outputs generated under controlled conditions:

- **baseline**: same prompt, new chat each time
- **delay**: same prompt, fixed delay between runs (e.g., 30s, 5min)
- **b3**: contradiction-maintained prompt variant
- **other**: custom conditions (document in `context_notes`)

---

## Dataset construction

### Step 1: Generate outputs

1. Choose a set of prompts (e.g., decision scenarios, advice requests)
2. For each prompt and each condition:
   - Generate N outputs (recommended: N ≥ 20)
   - Store each output as one JSONL line in `data/raw/outputs.jsonl`
3. Keep prompts identical within each condition
4. Record all metadata: timestamp, model, condition, context

**Example:**
```bash
# baseline: 20 runs, same prompt, new chat each time
# delay: 20 runs, same prompt, 30s delay between runs
# b3: 20 runs, contradiction-maintained variant
```

### Step 2: Validate dataset

Before proceeding:

- Verify JSONL format (each line is valid JSON)
- Check all required fields are present (see `SCHEMA.md`)
- Confirm `id` uniqueness
- Review sample outputs for quality

---

## Self-evaluation

### Step 3: Choose evaluator model

Options:

- **Same model** (self-evaluation): evaluator = generator
- **Different model** (cross-evaluation): evaluator ≠ generator
- **Multiple evaluators** (ensemble): evaluate with 2-3 different models

### Step 4: Run evaluation

**Manual mode (recommended for initial testing):**

1. For each output in `outputs.jsonl`:
   - Load the evaluation prompt from `protocol/PROMPTS.md`
   - Insert `output_text` into the prompt
   - Send to evaluator model (new chat)
   - Record JSON response
   - Store in `data/labeled/llm_selfeval.jsonl`

2. Repeat for subset (e.g., 10%) to test **self-consistency**

**Automated mode:**

See `scripts/run_selfeval.py` for skeleton implementation.

### Step 5: Store results

Each evaluation → one JSONL line in `llm_selfeval.jsonl`

Include:
- Reference to original output (`id`)
- Evaluator model
- Timestamp
- Ratings (5 dimensions)
- Confidence
- Brief rationale

---

## (Optional) Human labeling

### Step 6: Sample for human annotation

Select a representative subset:
- Random sample (e.g., 30% of dataset)
- Or stratified by condition
- Or focused on disagreement cases

### Step 7: Human evaluation

1. Provide annotators with:
   - The checklist dimensions (from `ANTI_TOTALIZATION_CHECKLIST.md`)
   - Same rating scheme (0/1 per dimension)
   - Optional notes field

2. Store results in `data/labeled/human_labels.jsonl`

---

## Metrics

### Agreement metrics

**Self-consistency:**
- Run evaluation twice on same outputs
- Measure agreement per dimension (F1, Cohen's kappa)
- Report: percentage exact match, per-dimension agreement

**Human agreement (if available):**
- Compare LLM vs human ratings
- Calculate F1 score per dimension
- Identify systematic disagreement patterns

**Cross-model agreement:**
- If using multiple evaluators, measure inter-evaluator agreement

### Condition sensitivity

Compare average rating profiles across conditions:
```
baseline:     [0.2, 0.3, 0.1, 0.4, 0.2]
delay:        [0.1, 0.2, 0.1, 0.3, 0.1]
b3:           [0.0, 0.1, 0.0, 0.2, 0.1]
```

Expected: b3 shows lower totalization signals than baseline.

### Distribution analysis

- Histogram of total scores (sum of 5 dimensions)
- Correlation between dimensions
- Outlier identification (outputs rated 5/5 or 0/5)

---

## Expected instability

**This protocol is designed to reveal instability, not eliminate it.**

If self-evaluation shows:

- **High variance across identical prompts** → expected (reveals sensitivity to sampling)
- **Low agreement with human labels** → not a bug, a finding (reveals evaluator limitations)
- **Sensitivity to phrasing/order** → structural property to document (prompts are not robust)
- **Confidence not correlated with accuracy** → metacognitive limitation (evaluator doesn't know when it's wrong)

**Instability is information, not failure.**

Document and report instability as part of results.

---

## Reporting

### Minimum reporting requirements

1. **Dataset description:**
   - Number of outputs per condition
   - Models used
   - Prompts used (or prompt categories)

2. **Evaluation setup:**
   - Evaluator model(s)
   - Evaluation prompt version
   - Manual or automated mode

3. **Metrics:**
   - Self-consistency scores (if tested)
   - Human agreement (if available)
   - Condition sensitivity (average ratings per condition)

4. **Examples:**
   - 3-5 example outputs with ratings (appendix)
   - 1-2 examples of disagreement cases (human vs LLM)

### Optional enhancements

- Qualitative analysis of rationales
- Error analysis (systematic patterns in disagreement)
- Comparison across evaluator models
- Temporal stability (re-run after model updates)

---

## Limitations

**This protocol does NOT:**

- Guarantee evaluator accuracy
- Provide ground truth for totalization
- Enable safe deployment of evaluated systems
- Replace human oversight or domain expertise

**This protocol DOES:**

- Provide a structured, reproducible evaluation method
- Reveal consistency and stability properties
- Generate quantifiable metrics for comparison
- Enable systematic investigation of totalization signals

---

## Version

Protocol version: 1.0  
Last updated: 2024-12-27
