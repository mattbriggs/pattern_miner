# tests/test_miner.py
import textwrap
from pattern_miner.miner import PatternMiner
from pattern_miner.extractor import HeadingBlockStrategy   # enforce old extractor

def test_end_to_end(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    markdown = textwrap.dedent("""\
        ### Context
        C
        ### Problem
        P
        ### Forces
        F
        ### Solution
        S
    """)
    (docs / "a.md").write_text(markdown)

    out_dir = tmp_path / "out"
    miner = PatternMiner(extractor=HeadingBlockStrategy())   # <— explicit
    miner.mine(docs)
    miner.export(out_dir)

    assert (out_dir / "patterns").exists()
    assert any((out_dir / "patterns").iterdir())