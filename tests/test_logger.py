from pattern_miner.utils.logger import get_logger

def test_logger_returns_singleton():
    l1 = get_logger()
    l2 = get_logger()
    assert l1 is l2