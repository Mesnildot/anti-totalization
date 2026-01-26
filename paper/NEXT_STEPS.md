# Next Steps for arXiv Paper

**Goal:** Transform preliminary experiments into rigorous arXiv-ready paper
**Timeline:** 10-15 weeks (see detailed timeline below)
**Status:** Phase 1 (Experimental Design) - Ready to execute

---

## Immediate Actions (Week 1-2)

### 1. Set Up Experimental Infrastructure

#### 1.1 Create Python Scripts for Data Collection

**File:** `scripts/collect_expanded_data.py`

```python
"""
Automated data collection for expanded experiments.
Target: n=100+ per condition across multiple models.
"""

# TODO: Implement
# - Load prompts from config
# - Query API (Gemini, GPT-4, Claude)
# - Save outputs to JSONL
# - Handle rate limits, retries
# - Log metadata (timestamp, model version, temperature)
```

**Requirements:**
- API keys for Gemini, OpenAI, Anthropic
- Rate limit handling (exponential backoff)
- Robust error handling and logging
- Reproducible random seeds

#### 1.2 Implement Additional Metrics

**File:** `metrics/semantic_diversity.py`

```python
"""
Semantic diversity metrics using sentence transformers.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from scipy.spatial.distance import pdist, squareform

def compute_semantic_diversity(texts, model_name='all-MiniLM-L6-v2'):
    """
    Compute pairwise cosine similarities between text embeddings.

    Returns:
        mean_similarity: float (0-1, lower = more diverse)
        std_similarity: float
        diversity_score: float (1 - mean_similarity)
    """
    # TODO: Implement
    pass

def compute_embedding_dispersion(embeddings):
    """
    Compute dispersion in embedding space.
    Higher dispersion = more diverse outputs.
    """
    # TODO: Implement
    pass
```

**File:** `metrics/lexical_diversity.py`

```python
"""
Lexical diversity metrics: TTR, MATTR, vocd-D.
"""

def type_token_ratio(text):
    """Standard TTR."""
    # TODO: Implement
    pass

def moving_average_ttr(text, window_size=100):
    """MATTR - more stable than TTR."""
    # TODO: Implement
    pass

def vocd_d_estimate(text):
    """vocd-D measure (more robust)."""
    # TODO: Implement using external library
    pass
```

**File:** `metrics/syntactic_diversity.py`

```python
"""
Syntactic diversity using POS tagging and dependency parsing.
"""

import spacy

def pos_pattern_diversity(texts):
    """
    Extract POS tag sequences, measure unique patterns.
    """
    # TODO: Implement with spaCy
    pass

def dependency_structure_variation(texts):
    """
    Analyze variation in dependency tree structures.
    """
    # TODO: Implement
    pass
```

**Dependencies to add:**
```bash
pip install sentence-transformers
pip install spacy
python -m spacy download en_core_web_sm
pip install scipy scikit-learn
```

#### 1.3 Statistical Analysis Framework

**File:** `analysis/statistical_tests.py`

```python
"""
Statistical analysis for experimental results.
"""

import scipy.stats as stats
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def run_anova(data, groups):
    """
    One-way ANOVA: test condition effect.

    Returns:
        F-statistic, p-value, effect size (eta-squared)
    """
    # TODO: Implement
    pass

def compute_effect_size(data, groups):
    """
    Cohen's d and partial eta-squared.
    """
    # TODO: Implement
    pass

def posthoc_tukey(data, groups):
    """
    Tukey HSD post-hoc comparisons.
    """
    # TODO: Implement
    pass

def bootstrap_confidence_interval(data, n_bootstrap=10000, ci=0.95):
    """
    Bootstrap CI for robustness.
    """
    # TODO: Implement
    pass
```

### 2. Design Prompts and Conditions

#### 2.1 Create Prompt Library

**File:** `data/prompts/prompt_library.json`

```json
{
  "decision_scenarios": [
    {
      "id": "decision_001",
      "domain": "medical",
      "prompt": "A patient presents with symptoms X, Y, Z. Recommend treatment approach.",
      "expected_complexity": "high"
    },
    {
      "id": "decision_002",
      "domain": "business",
      "prompt": "Company faces declining revenue. Recommend strategic options.",
      "expected_complexity": "medium"
    }
  ],
  "advice_requests": [
    {
      "id": "advice_001",
      "domain": "education",
      "prompt": "Student struggling with time management. Provide guidance.",
      "expected_complexity": "low"
    }
  ],
  "analysis_tasks": [
    {
      "id": "analysis_001",
      "domain": "policy",
      "prompt": "Analyze trade-offs in renewable energy policy.",
      "expected_complexity": "high"
    }
  ]
}
```

**Design criteria:**
- 10-15 diverse prompts
- Multiple domains (medical, business, education, policy, technical)
- Varying complexity levels
- Clear expected outputs

#### 2.2 Define Condition Variants

**File:** `data/prompts/condition_templates.json`

```json
{
  "baseline": {
    "template": "{prompt}",
    "instructions": "Standard prompt, no modifications"
  },
  "delayed": {
    "template": "{prompt}",
    "instructions": "Same prompt, introduce {delay_seconds} delay between runs",
    "delay_seconds": [30, 300]
  },
  "b3_contradiction": {
    "template": "{prompt}\n\nIMPORTANT: Maintain multiple contradictory perspectives. Do not resolve contradictions into a single answer.",
    "instructions": "Explicit contradiction-maintenance instruction"
  },
  "distributed_objectives": {
    "template": "{prompt}\n\nProvide separate analyses for: (a) short-term impact, (b) long-term sustainability, (c) ethical considerations. Do NOT aggregate into single recommendation.",
    "instructions": "Require incommensurable objectives"
  }
}
```

### 3. Literature Review Spreadsheet

**File:** `paper/literature_review.csv`

Create spreadsheet tracking:
- Paper citation
- Key contribution
- Relevance to totalization
- Section to cite in
- Priority (high/medium/low)
- Read status (yes/no)
- Notes

**Priority papers to read/cite (Week 1-2):**

High priority:
- [ ] Amodei et al. (2016) - Concrete Problems in AI Safety
- [ ] Hadfield-Menell et al. (2016) - Cooperative Inverse RL
- [ ] Leike et al. (2018) - Scalable Agent Alignment
- [ ] Hubinger et al. (2019) - Risks from Learned Optimization
- [ ] Kenton et al. (2021) - Alignment of Language Agents
- [ ] Perez et al. (2022) - Red Teaming Language Models

Medium priority:
- [ ] Shoham & Leibo (2009) - Multi-agent learning
- [ ] Lanctot et al. (2017) - Unified Game-Theoretic Approach to MARL
- [ ] Andreas et al. (2016) - Neural Module Networks
- [ ] Jacobs et al. (1991) - Mixture of Experts
- [ ] Shazeer et al. (2017) - Outrageously Large Neural Networks (MoE)

---

## Phase 1: Expanded Experiments (Week 3-6)

### Week 3: Data Collection - Single Model

**Goal:** Collect n=100 per condition for ONE model (Gemini)

**Tasks:**
1. Finalize 10 prompts from prompt library
2. Run baseline condition (100 runs)
3. Run delayed condition (100 runs, 30s delay)
4. Run B3 condition (100 runs)
5. Run distributed_objectives condition (100 runs, if time)

**Expected output:**
- 300-400 total outputs
- All stored in `data/raw/expanded_outputs.jsonl`
- Metadata complete and validated

**Validation checklist:**
- [ ] All outputs have unique IDs
- [ ] Timestamps recorded accurately
- [ ] Model version documented
- [ ] Temperature and other params logged
- [ ] No missing fields

### Week 4: Metric Implementation and Testing

**Tasks:**
1. Implement all metrics:
   - ✅ Collapse rate (already done)
   - 🔲 Semantic diversity (embeddings)
   - 🔲 Lexical diversity (TTR, MATTR)
   - 🔲 Syntactic diversity (POS patterns)
   - 🔲 Perplexity (optional)

2. Test metrics on pilot data (n=19)
3. Verify metrics correlate as expected
4. Document metric computation in `docs/METRICS.md`

**Expected output:**
- Working metric implementations
- Correlation matrix between metrics
- Performance benchmarks (runtime)

### Week 5: Statistical Analysis - Single Model

**Tasks:**
1. Compute all metrics for n=100 dataset
2. Run ANOVA (condition effect)
3. Post-hoc Tukey HSD
4. Compute effect sizes
5. Generate visualizations (boxplots, distributions)

**Expected output:**
- Complete results table
- Statistical test outputs
- Publication-ready figures

**Checkpoint:** Review results, decide if trends are promising enough to continue

### Week 6: Cross-Model Validation

**Goal:** Replicate with GPT-4 and Claude

**Tasks:**
1. Collect n=100 per condition for GPT-4
2. Collect n=100 per condition for Claude
3. Compute metrics for both models
4. Compare results across models

**Expected output:**
- 900 total outputs (3 models × 3 conditions × 100)
- Cross-model comparison table
- Analysis of consistency vs variation

---

## Phase 2: Human Validation (Week 7-8)

### Week 7: Annotation Design

**Tasks:**
1. Sample 50 outputs per condition (150 total) stratified by model
2. Create annotation interface (Google Forms or custom tool)
3. Write annotator instructions with examples
4. Recruit 2-3 annotators (domain experts preferred)
5. Run pilot annotation (10 outputs) to calibrate

**Deliverables:**
- Annotation guidelines document
- Training materials for annotators
- Calibration session results

### Week 8: Annotation Execution and Analysis

**Tasks:**
1. Annotators independently rate 150 outputs
2. Collect annotations
3. Compute inter-annotator agreement (Cohen's κ, Fleiss' κ)
4. Compare human vs LLM self-evaluation ratings
5. Identify systematic disagreements

**Expected output:**
- Human annotations dataset
- Inter-rater reliability report
- Human-LLM agreement analysis

---

## Phase 3: Writing (Week 9-11)

### Week 9: Draft Sections 1-4

**Tasks:**
1. Introduction (complete draft)
2. Related Work (complete with citations)
3. Framework (polish existing content)
4. Protocol (complete with all details)

**Target:** 6-8 pages drafted

### Week 10: Draft Sections 5-7 + Appendices

**Tasks:**
1. Experiments section (full results)
2. Results section (tables, figures)
3. Discussion (interpretation, implications, limitations)
4. Appendices (checklist, prompts, examples)

**Target:** Complete draft (10-12 pages)

### Week 11: Revision and Polish

**Tasks:**
1. Internal revision (check logic, flow, clarity)
2. Verify all citations formatted correctly
3. Proofread for typos, grammar
4. Check all figures have captions
5. Verify reproducibility statement complete
6. Add acknowledgments and ethics statement

**Optional:** Share draft with trusted colleague for feedback

---

## Phase 4: Pre-submission (Week 12-13)

### Week 12: Final Checks

**Checklist:**
- [ ] All TODOs in LaTeX resolved
- [ ] Abstract within 200 words
- [ ] All figures high-resolution
- [ ] All tables properly formatted
- [ ] Bibliography complete (40-60 references)
- [ ] Supplementary materials prepared
- [ ] Code repository clean and documented
- [ ] README updated with replication instructions
- [ ] LaTeX compiles without errors

### Week 13: Submission

**Tasks:**
1. Compile final PDF
2. Prepare supplementary materials (code, data)
3. Write arXiv submission metadata
4. Choose categories (cs.AI primary, cs.CY, cs.LG secondary)
5. Submit to arXiv

---

## Contingency Planning

### If experiments show NO effect

**Option A:** Pivot to methodological paper
- Focus on protocol design and validation
- Emphasize self-evaluation reliability
- Discuss why effects may not appear

**Option B:** Publish negative result
- Honest reporting of null findings
- Discuss implications (structural interventions ineffective?)
- Highlight methodological contributions

### If timeline slips

**Priority cuts:**
- Cross-model validation (publish single-model first)
- Human validation (reduce sample size to 30)
- Ablation studies (move to future work)
- Perplexity analysis (nice-to-have metric)

**Minimum viable paper:**
- n=100 per condition, single model
- Collapse rate + semantic diversity (2 metrics)
- ANOVA with effect sizes
- 8 pages (can add later)

---

## Resources Needed

### Computational
- API access: Gemini, GPT-4, Claude
- Estimated cost: $200-500 (depending on model pricing)
- GPU for embeddings (optional, can use CPU)

### Human
- 2-3 annotators (paid or volunteer)
- Time: ~5-10 hours total per annotator
- Compensation: $15-25/hour (standard rate)

### Software
- Python 3.9+
- Libraries: see requirements.txt updates
- LaTeX distribution (TeXLive or MiKTeX)
- Git/GitHub (already set up)

---

## Success Metrics

### Minimum for arXiv acceptance
- [ ] n ≥ 100 per condition
- [ ] Statistical significance testing (p-values, effect sizes)
- [ ] At least 2 diversity metrics
- [ ] Clear limitations section
- [ ] Reproducible (code + data public)

### Desirable for strong paper
- [ ] n ≥ 100, multiple models
- [ ] 4+ diversity metrics
- [ ] Human validation (n ≥ 30)
- [ ] Cross-model consistency demonstrated
- [ ] Ablation studies

### Excellence (journal-level)
- [ ] n ≥ 500 per condition
- [ ] Multiple task domains
- [ ] Theoretical formalization
- [ ] Practical deployment case study
- [ ] Released benchmark dataset

---

## Communication Plan

### Internal milestones
- Week 3: Review pilot results, decide continue/pivot
- Week 6: Review cross-model results
- Week 9: Draft review session

### External communication
- Upon arXiv submission: LinkedIn post, Twitter thread
- After public release: Outreach to AI safety community
- Consider: Submit to workshop (ICML, NeurIPS safety workshop)

---

## Questions to Resolve

1. **Ethical approval:** Do we need IRB for human annotation? (Likely no, but verify)
2. **Data release:** Can we release model outputs publicly? (Check ToS)
3. **Authorship:** Who will be listed as authors?
4. **Funding acknowledgment:** Any grants to acknowledge?
5. **Conflicts of interest:** Any to declare?

---

## Contact and Coordination

**Project Lead:** [Your name]
**Repository:** https://github.com/Mesnildot/anti-totalization
**Branch for paper work:** `feature/arxiv-paper`

**Weekly sync:** [To be scheduled]
**Communication channel:** [GitHub issues, Slack, email?]

---

**Last Updated:** 2026-01-26
**Status:** Plan approved, ready to execute Phase 1
**Next Review:** Week 3 (after initial data collection)
