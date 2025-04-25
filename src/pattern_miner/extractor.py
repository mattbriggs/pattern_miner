import re, hashlib
from pathlib import Path
from .patterns import Pattern
from .utils.logger import _Logger

log = _Logger.get()

class ExtractorStrategy:
    def extract(self, md_path: Path):
        raise NotImplementedError


class HeadingBlockStrategy(ExtractorStrategy):
    """Heuristic extractor using H3 headings (###). 
       Allows leading spaces before the hashes."""
    
    RE_FIELDS = re.compile(
        r'(?s)^\s*###\s*Context\s*(.*?)^\s*###\s*Problem\s*(.*?)'
        r'^\s*###\s*Forces\s*(.*?)^\s*###\s*Solution\s*(.*?)(?:$|^\s*###)',
        re.IGNORECASE | re.MULTILINE,
    )

    def extract(self, md_path: Path):
        text = md_path.read_text(encoding="utf-8")
        for match in self.RE_FIELDS.finditer(text):
            ctx, prob, forces, sol = match.groups()          # ← four vars
            uid = hashlib.sha1(prob.strip().encode()).hexdigest()[:8]
            yield Pattern(
                id=uid,
                title=prob.strip().split('\n')[0][:60],
                context=ctx.strip(),
                problem=prob.strip(),
                forces=forces.strip(),
                solution=sol.strip(),
            )