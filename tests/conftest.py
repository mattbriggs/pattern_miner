# tests/conftest.py
"""
Make the src/ directory importable during test collection
so `from pattern_miner ...` works without an editable install.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))