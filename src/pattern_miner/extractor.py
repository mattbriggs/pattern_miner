import re, hashlib
from pathlib import Path
from markdown_it import MarkdownIt
from pattern_miner.patterns import Pattern
from pattern_miner.utils.logger import _Logger

log = _Logger.get()

class ExtractorStrategy:
    def extract(self, md_path: Path):
        raise NotImplementedError

class HeadingBlockStrategy(ExtractorStrategy):
    """Simple heuristic extractor using H2–H3 headings."""
    RE_FIELDS = re.compile(r'(?s)###\s*Context\s*(.*?)###\s*Problem\s*(.*?)###\s*Forces\s*(.*?)###\s*Solution\s*(.*?)($|###)', re.IGNORECASE)

    def extract(self, md_path: Path):
        text = md_path.read_text()
        for match in self.RE_FIELDS.finditer(text):
            ctx, prob, forces, sol, _ = match.groups()
            uid = hashlib.sha1(prob.strip().encode()).hexdigest()[:8]
            yield Pattern(
                id=uid,
                title=prob.strip().split('\n')[0][:60],
                context=ctx.strip(),
                problem=prob.strip(),
                forces=forces.strip(),
                solution=sol.strip()
            )
