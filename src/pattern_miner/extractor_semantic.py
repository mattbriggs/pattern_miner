"""
Extractor that:
1. splits Markdown into sentences,
2. classifies each sentence (C / P / F / S),
3. assembles consecutive C-P-F-S runs into Pattern objects.
"""
# ------------------------------------------------------------------------
#  Ensure NLTK can find or fetch the Punkt sentence tokenizer
# ------------------------------------------------------------------------
import nltk, pathlib, logging, os

# 1.  Make sure ~/nltk_data is on the search list
DEFAULT_NLTK = pathlib.Path.home() / "nltk_data"
if str(DEFAULT_NLTK) not in nltk.data.path:
    nltk.data.path.insert(0, str(DEFAULT_NLTK))

# 2.  Make sure the punkt files are actually there; download if missing
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:                       # punkt or punkt_tab missing
    logging.info("Downloading NLTK punkt (one-time, ~50 kB)…")
    nltk.download("punkt", download_dir=str(DEFAULT_NLTK), quiet=True)
# ------------------------------------------------------------------------

from pathlib import Path
import itertools, uuid
import re, logging
import nltk  # safe to import again; same module instance
from sentence_transformers import SentenceTransformer, util
from .patterns import Pattern
from .utils.logger import get_logger

log = get_logger()

# ─── resources ──────────────────────────────────────────────────────────────

NLTK_OK = nltk.download("punkt", quiet=True)
MODEL   = SentenceTransformer("all-MiniLM-L6-v2")  # 384-d embeddings

LABELS = ["context", "problem", "forces", "solution"]

# Simple keyword baseline; swap with real classifier later  ────────────────
_KEYWORDS = {
    "context":  {"context", "background"},
    "problem":  {"problem", "issue", "challenge"},
    "forces":   {"forces", "constraints", "trade-off", "trade-offs"},
    "solution": {"solution", "approach", "resolution", "fix"},
}

def _keyword_label(sent):
    s = sent.lower()
    scores = {lab: max((s.count(k) for k in kws), default=0) for lab, kws in _KEYWORDS.items()}
    return max(scores, key=scores.get) if any(scores.values()) else None

class SemanticExtractor:
    def __init__(self, classifier=_keyword_label):
        self.classify = classifier

    def extract(self, md_path: Path):
        text = self._strip_code_blocks(md_path.read_text(encoding="utf-8"))
        sents = nltk.sent_tokenize(text)

        labelled = [(s, self.classify(s)) for s in sents]
        # slide a window of 4 consecutive sentences and test CPFS pattern
        for i in range(len(labelled) - 3):
            window = labelled[i : i + 4]
            if [lab for _, lab in window] == LABELS:
                ctx, prob, frc, sol = (s for s, _ in window)
                pid = uuid.uuid5(uuid.NAMESPACE_DNS, prob).hex[:8]
                yield Pattern(
                    id=pid,
                    title=prob[:60],
                    context=ctx,
                    problem=prob,
                    forces=frc,
                    solution=sol,
                )

    @staticmethod
    def _strip_code_blocks(md: str) -> str:
        return re.sub(r"```.*?```", "", md, flags=re.DOTALL)