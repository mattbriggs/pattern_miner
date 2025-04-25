# src/pattern_miner/aggregator.py
from collections import defaultdict
import hashlib

class PatternAggregator:
    """
    Groups patterns whose *problem* statements are sufficiently similar.
    Default implementation: exact-hash merge; you can swap in an
    embedding-based similarity test later.
    """
    def __init__(self):
        self._clusters = defaultdict(list)

    def add(self, pattern) -> str:
        """
        Add a Pattern instance.  
        Returns the cluster-id it ended up in.
        """
        cluster_id = hashlib.sha1(pattern.problem.encode()).hexdigest()[:8]
        self._clusters[cluster_id].append(pattern)
        return cluster_id

    # --- API used by miner.py ---------------------------------------------

    @property
    def clusters(self):
        return self._clusters