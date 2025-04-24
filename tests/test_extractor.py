from pathlib import Path
from pattern_miner.extractor import HeadingBlockStrategy

def test_basic_extraction(tmp_path):
    sample = tmp_path / "doc.md"
    sample.write_text("""### Context
    A situation
    ### Problem
    Something is wrong
    ### Forces
    X vs Y
    ### Solution
    Do Z""")
    strat = HeadingBlockStrategy()
    patterns = list(strat.extract(sample))
    assert len(patterns) == 1
    assert patterns[0].problem.startswith("Something is wrong")
