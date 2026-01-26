"""
Lexical diversity metrics.

Measures vocabulary richness and variation in text outputs.

Common metrics:
- TTR (Type-Token Ratio): simple but sensitive to text length
- MATTR (Moving Average TTR): more robust to length variation
- MTLD (Measure of Textual Lexical Diversity): length-independent

Usage:
    from metrics.lexical_diversity import compute_lexical_diversity

    text = "This is a sample text with some repeated words and words."
    results = compute_lexical_diversity(text)
    print(f"TTR: {results['ttr']:.3f}")
"""

import re
from typing import Dict, List
import numpy as np


def tokenize(text: str, lowercase: bool = True) -> List[str]:
    """
    Simple word tokenization.

    Args:
        text: Input text
        lowercase: Convert to lowercase

    Returns:
        List of tokens
    """
    if lowercase:
        text = text.lower()
    # Split on whitespace and punctuation
    tokens = re.findall(r'\b\w+\b', text)
    return tokens


def type_token_ratio(text: str, lowercase: bool = True) -> float:
    """
    Compute Type-Token Ratio (TTR).

    TTR = (number of unique words) / (total number of words)

    Args:
        text: Input text
        lowercase: Convert to lowercase before counting

    Returns:
        TTR score (0-1), higher = more diverse
    """
    tokens = tokenize(text, lowercase)
    if len(tokens) == 0:
        return 0.0

    types = set(tokens)
    return len(types) / len(tokens)


def moving_average_ttr(
    text: str,
    window_size: int = 100,
    lowercase: bool = True
) -> float:
    """
    Moving Average Type-Token Ratio (MATTR).

    More stable than TTR for texts of varying length.
    Computes TTR over sliding windows and averages.

    Args:
        text: Input text
        window_size: Size of sliding window
        lowercase: Convert to lowercase

    Returns:
        MATTR score (0-1), higher = more diverse
    """
    tokens = tokenize(text, lowercase)

    if len(tokens) < window_size:
        # Fall back to standard TTR if text too short
        return type_token_ratio(text, lowercase)

    # Compute TTR for each window
    ttrs = []
    for i in range(len(tokens) - window_size + 1):
        window = tokens[i:i + window_size]
        window_ttr = len(set(window)) / len(window)
        ttrs.append(window_ttr)

    return np.mean(ttrs)


def root_ttr(text: str, lowercase: bool = True) -> float:
    """
    Root TTR (RTTR).

    RTTR = types / sqrt(tokens)

    Attempts to correct for text length effect.

    Args:
        text: Input text
        lowercase: Convert to lowercase

    Returns:
        RTTR score, higher = more diverse
    """
    tokens = tokenize(text, lowercase)
    if len(tokens) == 0:
        return 0.0

    types = set(tokens)
    return len(types) / np.sqrt(len(tokens))


def corrected_ttr(text: str, lowercase: bool = True) -> float:
    """
    Corrected TTR (CTTR).

    CTTR = types / sqrt(2 * tokens)

    Another length correction variant.

    Args:
        text: Input text
        lowercase: Convert to lowercase

    Returns:
        CTTR score
    """
    tokens = tokenize(text, lowercase)
    if len(tokens) == 0:
        return 0.0

    types = set(tokens)
    return len(types) / np.sqrt(2 * len(tokens))


def uber_index(text: str, lowercase: bool = True) -> float:
    """
    Uber Index.

    UI = (log(tokens))^2 / (log(tokens) - log(types))

    Args:
        text: Input text
        lowercase: Convert to lowercase

    Returns:
        Uber Index score
    """
    tokens = tokenize(text, lowercase)
    if len(tokens) < 2:
        return 0.0

    types = set(tokens)
    if len(types) == len(tokens):
        # All unique, avoid division by zero
        return float('inf')

    log_tokens = np.log(len(tokens))
    log_types = np.log(len(types))

    return (log_tokens ** 2) / (log_tokens - log_types)


def measure_of_textual_lexical_diversity(
    text: str,
    factor_size: float = 0.72,
    lowercase: bool = True
) -> float:
    """
    Measure of Textual Lexical Diversity (MTLD).

    Length-independent measure based on how quickly TTR drops
    as text length increases.

    Args:
        text: Input text
        factor_size: TTR threshold (default 0.72)
        lowercase: Convert to lowercase

    Returns:
        MTLD score, higher = more diverse
    """
    tokens = tokenize(text, lowercase)

    if len(tokens) < 10:
        # Text too short for meaningful MTLD
        return type_token_ratio(text, lowercase) * 10

    def compute_factors(tokens, factor_size):
        """Count factors (segments where TTR drops below threshold)."""
        factors = 0
        types_seen = set()
        token_count = 0

        for token in tokens:
            types_seen.add(token)
            token_count += 1

            ttr = len(types_seen) / token_count

            if ttr < factor_size:
                factors += 1
                types_seen = set()
                token_count = 0

        # Partial factor at end
        if token_count > 0:
            factors += (1 - (len(types_seen) / token_count - factor_size) / (1 - factor_size))

        return factors

    # Compute forward and backward
    factors_forward = compute_factors(tokens, factor_size)
    factors_backward = compute_factors(tokens[::-1], factor_size)

    # Average
    factors = (factors_forward + factors_backward) / 2

    if factors == 0:
        return len(tokens)  # Extremely diverse

    return len(tokens) / factors


def compute_lexical_diversity(text: str, lowercase: bool = True) -> Dict[str, float]:
    """
    Compute all lexical diversity metrics.

    Args:
        text: Input text
        lowercase: Convert to lowercase

    Returns:
        Dictionary with all metrics
    """
    tokens = tokenize(text, lowercase)
    types = set(tokens)

    return {
        'n_tokens': len(tokens),
        'n_types': len(types),
        'ttr': type_token_ratio(text, lowercase),
        'rttr': root_ttr(text, lowercase),
        'cttr': corrected_ttr(text, lowercase),
        'mattr_50': moving_average_ttr(text, window_size=50, lowercase=lowercase),
        'mattr_100': moving_average_ttr(text, window_size=100, lowercase=lowercase),
        'uber': uber_index(text, lowercase),
        'mtld': measure_of_textual_lexical_diversity(text, lowercase=lowercase)
    }


def compute_corpus_lexical_diversity(
    texts: List[str],
    lowercase: bool = True
) -> Dict[str, float]:
    """
    Compute lexical diversity across a corpus of texts.

    Args:
        texts: List of texts
        lowercase: Convert to lowercase

    Returns:
        Dictionary with corpus-level metrics
    """
    all_tokens = []
    for text in texts:
        all_tokens.extend(tokenize(text, lowercase))

    all_types = set(all_tokens)

    # Per-text metrics
    per_text_ttrs = [type_token_ratio(text, lowercase) for text in texts]

    return {
        'corpus_ttr': len(all_types) / len(all_tokens) if all_tokens else 0.0,
        'mean_text_ttr': np.mean(per_text_ttrs) if per_text_ttrs else 0.0,
        'std_text_ttr': np.std(per_text_ttrs) if per_text_ttrs else 0.0,
        'total_tokens': len(all_tokens),
        'total_types': len(all_types),
        'n_texts': len(texts)
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python lexical_diversity.py <file.txt>")
        print("File should contain text (single document or one per line)")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if multi-line (corpus) or single text
    lines = [line.strip() for line in content.split('\n') if line.strip()]

    if len(lines) > 1:
        print(f"Computing lexical diversity for corpus ({len(lines)} texts)...\n")

        # Corpus-level
        corpus_results = compute_corpus_lexical_diversity(lines)
        print("Corpus-level metrics:")
        print(f"  Corpus TTR:          {corpus_results['corpus_ttr']:.3f}")
        print(f"  Mean text TTR:       {corpus_results['mean_text_ttr']:.3f}")
        print(f"  Std text TTR:        {corpus_results['std_text_ttr']:.3f}")
        print(f"  Total tokens:        {corpus_results['total_tokens']}")
        print(f"  Total types:         {corpus_results['total_types']}")

        # Per-text statistics
        print("\nPer-text diversity distribution:")
        per_text = [compute_lexical_diversity(text) for text in lines]
        ttrs = [r['ttr'] for r in per_text]
        print(f"  Min TTR:             {min(ttrs):.3f}")
        print(f"  Max TTR:             {max(ttrs):.3f}")
        print(f"  Range:               {max(ttrs) - min(ttrs):.3f}")

    else:
        # Single text
        print(f"Computing lexical diversity for single text...\n")
        results = compute_lexical_diversity(content)

        print("Lexical Diversity Metrics:")
        print(f"  Tokens:              {results['n_tokens']}")
        print(f"  Types (unique):      {results['n_types']}")
        print(f"  TTR:                 {results['ttr']:.3f}")
        print(f"  Root TTR:            {results['rttr']:.3f}")
        print(f"  Corrected TTR:       {results['cttr']:.3f}")
        print(f"  MATTR (50):          {results['mattr_50']:.3f}")
        print(f"  MATTR (100):         {results['mattr_100']:.3f}")
        print(f"  Uber Index:          {results['uber']:.3f}")
        print(f"  MTLD:                {results['mtld']:.3f}")

        # Interpretation
        ttr = results['ttr']
        if ttr < 0.40:
            print("\nInterpretation: LOW lexical diversity (repetitive)")
        elif ttr < 0.60:
            print("\nInterpretation: MEDIUM lexical diversity")
        else:
            print("\nInterpretation: HIGH lexical diversity (rich vocabulary)")
