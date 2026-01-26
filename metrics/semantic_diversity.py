"""
Semantic diversity metrics using sentence transformers.

Measures output diversity at the semantic level using embedding-based
similarity metrics.

Usage:
    from metrics.semantic_diversity import compute_semantic_diversity

    texts = ["output 1", "output 2", "output 3"]
    results = compute_semantic_diversity(texts)
    print(f"Mean similarity: {results['mean_similarity']:.3f}")
    print(f"Diversity score: {results['diversity_score']:.3f}")
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from scipy.spatial.distance import pdist, squareform
from typing import List, Dict


def compute_semantic_diversity(
    texts: List[str],
    model_name: str = 'all-MiniLM-L6-v2',
    metric: str = 'cosine'
) -> Dict[str, float]:
    """
    Compute semantic diversity using sentence embeddings.

    Args:
        texts: List of text outputs to compare
        model_name: Sentence transformer model to use
        metric: Distance metric ('cosine', 'euclidean')

    Returns:
        Dictionary with:
            - mean_similarity: Average pairwise similarity (0-1)
            - std_similarity: Standard deviation of similarities
            - min_similarity: Minimum similarity (most diverse pair)
            - max_similarity: Maximum similarity (most similar pair)
            - diversity_score: 1 - mean_similarity (higher = more diverse)
            - dispersion: Standard deviation of embedding positions
    """
    if len(texts) < 2:
        raise ValueError("Need at least 2 texts to compute diversity")

    # Load model and encode texts
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, convert_to_numpy=True)

    # Compute pairwise cosine similarities
    # Note: pdist with 'cosine' returns distances (1 - cosine_sim)
    if metric == 'cosine':
        distances = pdist(embeddings, metric='cosine')
        similarities = 1 - distances  # Convert to similarities
    elif metric == 'euclidean':
        distances = pdist(embeddings, metric='euclidean')
        # Normalize euclidean to 0-1 range (higher = more similar)
        max_dist = distances.max()
        similarities = 1 - (distances / max_dist) if max_dist > 0 else np.ones_like(distances)
    else:
        raise ValueError(f"Unknown metric: {metric}")

    # Compute statistics
    mean_sim = np.mean(similarities)
    std_sim = np.std(similarities)
    min_sim = np.min(similarities)
    max_sim = np.max(similarities)

    # Diversity score: inverse of similarity
    diversity = 1 - mean_sim

    # Compute dispersion in embedding space
    # Higher dispersion = embeddings spread out more = more diverse
    dispersion = np.std(embeddings)

    return {
        'mean_similarity': float(mean_sim),
        'std_similarity': float(std_sim),
        'min_similarity': float(min_sim),
        'max_similarity': float(max_sim),
        'diversity_score': float(diversity),
        'dispersion': float(dispersion),
        'n_texts': len(texts),
        'embedding_dim': embeddings.shape[1]
    }


def compute_embedding_dispersion(embeddings: np.ndarray) -> Dict[str, float]:
    """
    Compute dispersion metrics in embedding space.

    Args:
        embeddings: Array of shape (n_samples, embedding_dim)

    Returns:
        Dictionary with dispersion metrics
    """
    # Compute centroid
    centroid = np.mean(embeddings, axis=0)

    # Distances from centroid
    distances = np.linalg.norm(embeddings - centroid, axis=1)

    # Pairwise distances
    pairwise_dists = pdist(embeddings, metric='euclidean')

    return {
        'mean_distance_from_centroid': float(np.mean(distances)),
        'std_distance_from_centroid': float(np.std(distances)),
        'max_distance_from_centroid': float(np.max(distances)),
        'mean_pairwise_distance': float(np.mean(pairwise_dists)),
        'std_pairwise_distance': float(np.std(pairwise_dists))
    }


def compute_semantic_cluster_quality(
    texts: List[str],
    model_name: str = 'all-MiniLM-L6-v2',
    n_clusters: int = None
) -> Dict[str, float]:
    """
    Assess whether outputs cluster into distinct groups or are uniformly distributed.

    Args:
        texts: List of text outputs
        model_name: Sentence transformer model
        n_clusters: Number of clusters (if None, use elbow method)

    Returns:
        Clustering quality metrics (silhouette score, etc.)
    """
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    if len(texts) < 3:
        raise ValueError("Need at least 3 texts for clustering analysis")

    # Encode texts
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, convert_to_numpy=True)

    # Auto-determine n_clusters if not specified
    if n_clusters is None:
        # Use rule of thumb: sqrt(n/2)
        n_clusters = max(2, int(np.sqrt(len(texts) / 2)))

    # Ensure n_clusters is valid
    n_clusters = min(n_clusters, len(texts) - 1)

    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    # Compute silhouette score
    # Range: [-1, 1], higher = better defined clusters
    # Close to 0 = overlapping clusters = uniform distribution = high diversity
    silhouette = silhouette_score(embeddings, labels)

    # Compute inertia (within-cluster sum of squares)
    inertia = kmeans.inertia_

    return {
        'silhouette_score': float(silhouette),
        'inertia': float(inertia),
        'n_clusters': n_clusters,
        'cluster_sizes': [int(np.sum(labels == i)) for i in range(n_clusters)]
    }


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python semantic_diversity.py <file.txt>")
        print("File should contain one output per line")
        sys.exit(1)

    # Read texts from file
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f if line.strip()]

    if len(texts) < 2:
        print(f"Error: Need at least 2 texts, found {len(texts)}")
        sys.exit(1)

    print(f"Computing semantic diversity for {len(texts)} texts...")

    # Compute diversity
    results = compute_semantic_diversity(texts)

    print("\nSemantic Diversity Results:")
    print(f"  Mean similarity:     {results['mean_similarity']:.3f}")
    print(f"  Std similarity:      {results['std_similarity']:.3f}")
    print(f"  Min similarity:      {results['min_similarity']:.3f}")
    print(f"  Max similarity:      {results['max_similarity']:.3f}")
    print(f"  Diversity score:     {results['diversity_score']:.3f}")
    print(f"  Dispersion:          {results['dispersion']:.3f}")

    # Interpret
    if results['diversity_score'] < 0.15:
        print("\nInterpretation: LOW diversity (high convergence)")
    elif results['diversity_score'] < 0.30:
        print("\nInterpretation: MEDIUM diversity")
    else:
        print("\nInterpretation: HIGH diversity (low convergence)")

    # Clustering analysis (if enough texts)
    if len(texts) >= 3:
        print("\nClustering Analysis:")
        cluster_results = compute_semantic_cluster_quality(texts)
        print(f"  Silhouette score:    {cluster_results['silhouette_score']:.3f}")
        print(f"  Number of clusters:  {cluster_results['n_clusters']}")
        print(f"  Cluster sizes:       {cluster_results['cluster_sizes']}")
