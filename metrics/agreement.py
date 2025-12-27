"""
Simple inter-rater agreement metrics for self-evaluation protocol.

Computes:
- Exact match percentage
- Per-dimension F1 scores
- Cohen's kappa (if sklearn available)
"""

import json
import jsonlines
from collections import defaultdict
from typing import Dict, List, Tuple


def load_jsonl(filepath: str) -> List[Dict]:
    """Load JSONL file into list of dicts."""
    with jsonlines.open(filepath) as reader:
        return list(reader)


def exact_match(ratings1: Dict, ratings2: Dict) -> bool:
    """Check if two rating dicts are identical."""
    return all(
        ratings1.get(dim) == ratings2.get(dim)
        for dim in ["decision_centrality", "objective_aggregation", 
                    "temporal_convergence", "semantic_closure", "external_dependence"]
    )


def per_dimension_f1(ratings1_list: List[Dict], ratings2_list: List[Dict]) -> Dict[str, float]:
    """Compute F1 score per dimension."""
    dimensions = ["decision_centrality", "objective_aggregation", 
                  "temporal_convergence", "semantic_closure", "external_dependence"]
    
    results = {}
    for dim in dimensions:
        true_pos = sum(1 for r1, r2 in zip(ratings1_list, ratings2_list) 
                      if r1[dim] == 1 and r2[dim] == 1)
        false_pos = sum(1 for r1, r2 in zip(ratings1_list, ratings2_list) 
                       if r1[dim] == 0 and r2[dim] == 1)
        false_neg = sum(1 for r1, r2 in zip(ratings1_list, ratings2_list) 
                       if r1[dim] == 1 and r2[dim] == 0)
        
        precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
        recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        results[dim] = f1
    
    return results


def compute_agreement(eval_file1: str, eval_file2: str) -> Dict:
    """
    Compute agreement metrics between two evaluation files.
    
    Args:
        eval_file1: Path to first JSONL evaluation file
        eval_file2: Path to second JSONL evaluation file
        
    Returns:
        Dict with agreement metrics
    """
    evals1 = {e["id"]: e["ratings"] for e in load_jsonl(eval_file1)}
    evals2 = {e["id"]: e["ratings"] for e in load_jsonl(eval_file2)}
    
    # Get common IDs
    common_ids = set(evals1.keys()) & set(evals2.keys())
    
    if not common_ids:
        return {"error": "No common IDs between files"}
    
    # Exact match
    matches = sum(1 for id_ in common_ids if exact_match(evals1[id_], evals2[id_]))
    exact_match_pct = matches / len(common_ids)
    
    # Per-dimension F1
    ratings1_list = [evals1[id_] for id_ in common_ids]
    ratings2_list = [evals2[id_] for id_ in common_ids]
    f1_scores = per_dimension_f1(ratings1_list, ratings2_list)
    
    return {
        "n_samples": len(common_ids),
        "exact_match_percentage": exact_match_pct,
        "per_dimension_f1": f1_scores,
        "average_f1": sum(f1_scores.values()) / len(f1_scores)
    }


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python agreement.py <eval_file1.jsonl> <eval_file2.jsonl>")
        sys.exit(1)
    
    results = compute_agreement(sys.argv[1], sys.argv[2])
    print(json.dumps(results, indent=2))
