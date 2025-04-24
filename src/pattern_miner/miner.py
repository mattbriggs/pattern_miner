from pathlib import Path
from jsonschema import validate
import yaml, json, shutil
from pattern_miner.patterns import PatternRepository
from pattern_miner.extractor import HeadingBlockStrategy
from pattern_miner.utils.logger import _Logger

log = _Logger.get()

SCHEMA_PATH = Path(__file__).parent / "schemas" / "pattern.schema.json"
with SCHEMA_PATH.open() as f:
    PATTERN_SCHEMA = json.load(f)

class PatternMiner:
    def __init__(self, extractor=None):
        self.extractor = extractor or HeadingBlockStrategy()
        self.repo = PatternRepository()

    def mine(self, docs_path: Path):
        docs_path = Path(docs_path)
        for md in docs_path.rglob("*.md"):
            log.info(f"Parsing {md}")
            for pattern in self.extractor.extract(md):
                self.repo.add_or_merge(pattern)

    def export(self, out_dir: Path):
        out_dir = Path(out_dir)
        if out_dir.exists():
            shutil.rmtree(out_dir)
        (out_dir / "patterns").mkdir(parents=True)

        for p in self.repo.all():
            validate(instance=json.loads(json.dumps(p.__dict__)), schema=PATTERN_SCHEMA)
            (out_dir / "patterns" / f"{p.id}.yaml").write_text(p.to_yaml())

        # human catalogue
        with (out_dir / "instructions.md").open("w") as cat:
            for p in self.repo.all():
                cat.write(f"## {p.title}\n")
                cat.write(f"**Context**: {p.context}\n\n")
                cat.write(f"**Problem**: {p.problem}\n\n")
                cat.write(f"**Forces**: {p.forces}\n\n")
                cat.write(f"**Solution**: {p.solution}\n\n---\n")
