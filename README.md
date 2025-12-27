# Anti-Totalization

**Checklist, Anti-Pattern, and LLM Self-Evaluation Protocol**

This repository provides structural tools for identifying and evaluating risks of decision centrality ("totalization") in artificial intelligence systems.

---

## What this repository provides

1. **Anti-Totalization Checklist** — A design review tool for assessing structural concentration in AI systems
2. **Totalization Anti-Pattern** — Documentation of how totalization emerges as an architectural failure mode
3. **LLM Self-Evaluation Protocol** — An experimental methodology for testing whether LLMs can stably evaluate totalization signals in outputs

---

## What this is

- A **structural framing** for risks of perceived centrality and authority in AI systems
- A **reproducible evaluation protocol** using JSONL data format and model-agnostic prompts
- A set of **design review instruments** for system architects and researchers

---

## What this is NOT

See: [`docs/SCOPE_AND_NONCLAIMS.md`](docs/SCOPE_AND_NONCLAIMS.md)

**We do not claim:**
- Agency, intention, or consciousness in AI systems
- That self-evaluation provides safety guarantees
- That this solves alignment, governance, or ethical problems

**We do not propose:**
- Ethical frameworks or normative guidelines
- Safety mechanisms or automated controls
- Regulatory policies or certification standards

---

## Documents

### Core framework

- **Checklist:** [`docs/ANTI_TOTALIZATION_CHECKLIST.md`](docs/ANTI_TOTALIZATION_CHECKLIST.md)
- **Anti-pattern:** [`docs/ANTI_PATTERN_TOTALIZATION.md`](docs/ANTI_PATTERN_TOTALIZATION.md)
- **Scope & non-claims:** [`docs/SCOPE_AND_NONCLAIMS.md`](docs/SCOPE_AND_NONCLAIMS.md)

### Evaluation protocol

- **Protocol overview:** [`protocol/AUTOEVAL_PROTOCOL.md`](protocol/AUTOEVAL_PROTOCOL.md)
- **Evaluation prompts:** [`protocol/PROMPTS.md`](protocol/PROMPTS.md)
- **Data schema:** [`protocol/SCHEMA.md`](protocol/SCHEMA.md)

---

## Quick Start (Manual Mode)

### 1. Generate outputs dataset

Create model outputs under controlled conditions:

- **baseline**: Same prompt, new chat each time
- **delay**: Same prompt, with fixed delay between runs
- **b3**: Contradiction-maintained prompt variant

Store outputs in `data/raw/outputs.jsonl` following the schema in [`protocol/SCHEMA.md`](protocol/SCHEMA.md).

### 2. Self-evaluate outputs

For each output:

1. Load evaluation prompt from [`protocol/PROMPTS.md`](protocol/PROMPTS.md)
2. Insert output text into prompt
3. Send to evaluator model (new chat)
4. Store JSON response in `data/labeled/llm_selfeval.jsonl`

### 3. Analyze results

- Calculate self-consistency (run evaluation twice)
- Compare conditions (baseline vs delay vs b3)
- Optional: Add human labels for validation

See [`protocol/AUTOEVAL_PROTOCOL.md`](protocol/AUTOEVAL_PROTOCOL.md) for detailed instructions.

---

## Recommended Experiments

- **Self-consistency test**: Evaluate same outputs twice, measure agreement
- **Condition sensitivity**: Compare baseline vs delay vs b3
- **Cross-model evaluation**: Use different model as evaluator
- **Human agreement**: Annotate subset, compare with LLM ratings

---

## Repository Structure
```
anti-totalization/
├── README.md
├── LICENSE
├── CITATION.cff
├── docs/
│   ├── ANTI_TOTALIZATION_CHECKLIST.md
│   ├── ANTI_PATTERN_TOTALIZATION.md
│   └── SCOPE_AND_NONCLAIMS.md
├── protocol/
│   ├── AUTOEVAL_PROTOCOL.md
│   ├── PROMPTS.md
│   └── SCHEMA.md
├── data/
│   ├── raw/
│   │   └── outputs.jsonl
│   └── labeled/
│       ├── llm_selfeval.jsonl
│       └── human_labels.jsonl
├── scripts/
│   ├── make_dataset.py
│   ├── run_selfeval.py
│   └── score_selfeval.py
├── metrics/
│   └── agreement.py
└── experiments/
    └── runs/
        └── run_001/
            ├── config.json
            ├── outputs.jsonl
            └── scores.json
```

---

## Non-Goals

This repository does **NOT** aim to:

- Provide safety mechanisms or alignment techniques
- Propose behavioral rules or constraints
- Create self-correcting or self-regulating systems
- Define "good" or "bad" model behavior

We provide **evaluation instruments**, not solutions.

---

## Citation

If you use this checklist or protocol in your work, please cite:
```bibtex
@software{anti_totalization_2024,
  title = {Anti-Totalization: Checklist and LLM Self-Evaluation Protocol},
  author = {{ChatGPT-5.2} and {Claude Sonnet 4}},
  year = {2024},
  month = {12},
  url = {https://github.com/[YOUR-USERNAME]/anti-totalization},
  version = {1.0.0},
  license = {MIT}
}
```

Or use the "Cite this repository" button on GitHub.

---

## License

MIT License — See [`LICENSE`](LICENSE) for details.

---

## Contributing

This is an experimental framework. Contributions, critiques, and adaptations are welcome.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines (if you create this file).

---

## Authors

**Content Authors:**  
ChatGPT-5.2 (OpenAI) & Claude Sonnet 4 (Anthropic)

**Repository Maintainer:**  
B329 Pons Dumesnil

The maintainer provided direction and supervision but does not claim authorship of the conceptual framework.

---

## Version

Repository version: 1.0.0  
Last updated: 2024-12-27
```

---

## 10. requirements.txt
```
# Python dependencies for anti-totalization protocol
# Last updated: 2024-12-27

# Data handling
jsonlines>=3.1.0

# Analysis (optional, uncomment if needed)
# pandas>=2.0.0
# numpy>=1.24.0
# scikit-learn>=1.3.0

# Visualization (optional, uncomment if needed)
# matplotlib>=3.7.0
# seaborn>=0.12.0
