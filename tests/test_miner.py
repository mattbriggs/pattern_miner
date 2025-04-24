from pattern_miner.miner import PatternMiner
from pathlib import Path

def test_end_to_end(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("""### Context
    C
    ### Problem
    P
    ### Forces
    F
    ### Solution
    S""")
    out_dir = tmp_path / "out"
    miner = PatternMiner()
    miner.mine(docs)
    miner.export(out_dir)
    assert (out_dir / "patterns").exists()
    assert any(out_dir.joinpath("patterns").iterdir())
