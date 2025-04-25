from dataclasses import dataclass, asdict
import datetime, yaml

@dataclass
class Pattern:
    id: str
    title: str
    context: str
    problem: str
    forces: str
    solution: str

    def to_yaml(self):
        import yaml, datetime, uuid
        data = asdict(self)
        data["generated"] = datetime.datetime.now(datetime.UTC).isoformat()
        return yaml.dump(data, sort_keys=False)

class PatternRepository:
    """In-memory store; can be swapped for DB."""
    def __init__(self):
        self._patterns = {}

    def add_or_merge(self, pattern: Pattern):
        if pattern.id in self._patterns:
            return
        self._patterns[pattern.id] = pattern

    def all(self):
        return list(self._patterns.values())
