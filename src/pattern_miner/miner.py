# src/pattern_miner/miner.py
"""
Mine a Markdown repository for recurring Context-Problem-Forces-Solution
(CPFS) quads, cluster similar problems into “atoms,” and export the resulting
pattern language (YAML files + human-readable catalogue).

This file is intentionally thin: it wires together three pluggable
components—

* **Extractor**  – yields individual `Pattern` objects from raw Markdown
* **Aggregator** – groups semantically-similar problems
* **Exporter**   – writes YAML + Markdown

Swap any of them without touching the CLI or tests.
"""

from pathlib import Path
import json
import shutil
from jsonschema import validate

from .utils.logger import get_logger
from .extractor_semantic import SemanticExtractor          # ← NLP extractor
from .aggregator_semantic import SemanticAggregator        # ← NLP aggregator
from .patterns import Pattern                              # dataclass

log = get_logger()

# --------------------------------------------------------------------------- #
#                               JSON-Schema setup                             #
# --------------------------------------------------------------------------- #
SCHEMA_PATH = Path(__file__).parent / "schemas" / "pattern.schema.json"
PATTERN_SCHEMA = json.loads(SCHEMA_PATH.read_text())


class PatternMiner:
    """
    Orchestrates the three high-level phases:

        1. mine()   – walk docs, extract CPFS candidates, cluster them
        2. export() – dump clusters to YAML + Markdown
    """

    def __init__(
        self,
        extractor=None,
        aggregator=None,
    ):
        # Allow dependency-injection for unit tests or alternative strategies
        self.extractor = extractor or SemanticExtractor()
        self.aggregator = aggregator or SemanticAggregator()

    # --------------------------------------------------------------------- #
    #                               MINING PHASE                             #
    # --------------------------------------------------------------------- #
    def mine(self, docs_root: Path) -> None:
        """
        Walk every *.md file under `docs_root`, extract candidate patterns,
        and push them into the aggregator.
        """
        docs_root = Path(docs_root)
        md_files = list(docs_root.rglob("*.md"))
        if not md_files:
            log.warning("No Markdown files found under %s", docs_root)

        for md in md_files:
            log.info("Scanning %s", md)
            try:
                for pattern in self.extractor.extract(md):
                    self.aggregator.add(pattern)
            except Exception as exc:
                log.error("Extractor failed on %s: %s", md, exc)

    # --------------------------------------------------------------------- #
    #                              EXPORT PHASE                              #
    # --------------------------------------------------------------------- #
    def export(self, out_dir: Path) -> None:
        """
        Write one YAML file per cluster + a catalogue `instructions.md`.
        """
        out_dir = Path(out_dir)
        if out_dir.exists():
            shutil.rmtree(out_dir)
        (out_dir / "patterns").mkdir(parents=True)

        # 1️⃣  YAML pattern files ------------------------------------------
        for cid, plist in self.aggregator.clusters.items():
            exemplar: Pattern = plist[0]["pat"]
            validate(exemplar.__dict__, PATTERN_SCHEMA)

            yaml_path = out_dir / "patterns" / f"{cid}.yaml"
            yaml_path.write_text(exemplar.to_yaml())
            log.debug("Wrote %s", yaml_path)

        # 2️⃣  Human-readable catalogue ------------------------------------
        with (out_dir / "instructions.md").open("w") as cat:
            for cid, plist in self.aggregator.clusters.items():
                p: Pattern = plist[0]["pat"]
                cat.write(f"## {p.title}\n\n")
                cat.write(f"**Occurrences**: {len(plist)}\n\n")
                cat.write(f"**Context**\n{p.context}\n\n")
                cat.write(f"**Problem**\n{p.problem}\n\n")
                cat.write(f"**Forces**\n{p.forces}\n\n")
                cat.write(f"**Solution**\n{p.solution}\n\n---\n")
        log.info("Export complete: %d clusters -> %s", len(self.aggregator.clusters), out_dir)