# Pattern Miner

Pattern Miner scans a repository of Markdown documentation, discovers recurring **Context–Problem–Forces–Solution** snippets and distills them into a machine‑readable pattern language.

```bash
# install
pip install -r requirements.txt

# mine patterns

Run from the root folder.

```
python3 -m src.pattern_miner.cli /path/to/docs /path/to/output
```

Output:
* `patterns/` – one **YAML** file per mined pattern
* `schemas/pattern.schema.json` – JSON Schema definition
* `instructions.md` – human‑readable pattern catalogue
