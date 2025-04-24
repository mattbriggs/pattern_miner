## About Pattern Miner

*Architectural style*. The app follows a **Clean Architecture** layered layout:

* `extractor` (Infrastructure) — pulls raw Markdown and yields candidate fragments.
* `patterns` (Domain) — entities: `Pattern`, `PatternRepository`.
* `miner` (Application) — orchestrates the workflow via the **Facade** pattern.
* `cli` (Interface) — *Adapter* exposing a Click CLI.

*Design patterns employed*
| Purpose | Pattern |
|---------|---------|
| Single shared logger | Singleton |
| Interchangeable parsing strategies | Strategy |
| Persist pattern formats (YAML, JSON) | Factory Method |
| One‑stop workflow call | Facade |

*Mining algorithm* (simplified):
1. Parse Markdown into an AST (markdown-it-py).
2. Slide a window over heading‑delimited chunks.
3. Hash the `Problem` block; count duplicates.
4. When frequency ≥ *min_support* (default = 3) create/merge a `Pattern` atom.
5. Emit YAML & validate against JSON Schema.

*Extending*: implement a new `ExtractorStrategy` subclass and register it in `cli.py`.
