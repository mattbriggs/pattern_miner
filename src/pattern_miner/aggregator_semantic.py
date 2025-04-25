from collections import defaultdict
from sentence_transformers import SentenceTransformer, util

class SemanticAggregator:
    """Merge patterns whose *Problem* sentences are semantically close."""
    def __init__(self, similarity=0.75):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.sim   = similarity
        self.clusters = defaultdict(list)

    def add(self, pattern):
        emb = self.model.encode(pattern.problem, convert_to_tensor=True)
        # find best existing cluster
        best_id, best_sim = None, 0.0
        for cid, plist in self.clusters.items():
            ref_emb = plist[0]["emb"]
            sim = util.cos_sim(emb, ref_emb).item()
            if sim > best_sim:
                best_id, best_sim = cid, sim
        if best_sim >= self.sim:
            self.clusters[best_id].append({"pat": pattern, "emb": emb})
        else:
            self.clusters[pattern.id].append({"pat": pattern, "emb": emb})