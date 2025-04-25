# src/pattern_miner/extractor_ner.py  (new)
import re, itertools, hashlib
from pathlib import Path
from sentence_transformers import SentenceTransformer
from .patterns import Pattern
from .utils.logger import get_logger

log = get_logger()
_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

HEADING_RE = re.compile(r"^#{1,6}\s*(.+)", re.MULTILINE)

KEYWORDS = {
    "context": {"context", "background"},
    "problem": {"problem", "issue", "challenge"},
    "forces":  {"forces", "constraints", "trade-offs"},
    "solution":{"solution", "resolution", "approach", "proposal"},
}

def _heading_type(text):
    token = text.lower().strip(":")
    for t, kws in KEYWORDS.items():
        if token in kws:
            return t
    return None

class NLPExtractor:
    """
    1. Split the doc into heading-delimited sections.
    2. Label each heading as context/problem/… if keyword matches.
    3. Slide a window over 4 successive sections; when we hit C-P-F-S in order,
       emit a Pattern candidate.
    """
    def extract(self, md_path: Path):
        text = md_path.read_text(encoding="utf-8")
        indices = [(m.start(), m.group(1)) for m in HEADING_RE.finditer(text)]
        chunks = []
        for (start, head), (end, _) in itertools.pairwise(indices + [(len(text), None)]):
            chunks.append((head, text[start:end]))

        typed = [( _heading_type(h), body) for h, body in chunks if _heading_type(h)]
        for i in range(len(typed) - 3):
            types = [typed[i+k][0] for k in range(4)]
            if types == ["context", "problem", "forces", "solution"]:
                ctx, prob, frc, sol = (typed[i+k][1].strip() for k in range(4))
                pid = hashlib.sha1(prob.encode()).hexdigest()[:8]
                yield Pattern(
                    id=pid,
                    title=prob.splitlines()[0][:60],
                    context=ctx,
                    problem=prob,
                    forces=frc,
                    solution=sol,
                )

                