# CivicMarketEngine

Source-visible, noncommercial real-estate market simulation demo.

This public package is a sanitized demo package. It is not the private research
workspace and it does not contain the private LLM prompts, internal stage
reports, formal reproduction harnesses, live LLM artifacts, or AGENTS.md
boundary contract.

## What is included

- A small offline smoke demo: `python scripts/public_smoke_test.py --rounds 1 --seed 42`
- Public licensing and attribution material.
- A snapshot checker that blocks runtime artifacts, secrets, local paths, and
  private prompt / formal reproduction files.
- A small set of safe model and finance helper source files for inspection.

## What is intentionally excluded

- Private prompt assets and prompt tuning strategy.
- `AGENTS.md` and internal LLM/code boundary instructions.
- Formal reproduction harnesses, staged gate reports, and long-run matrices.
- Live LLM outputs, `.env` files, databases, spreadsheets, logs, caches, and
  local result folders.
- The private full simulation runtime.

## Quick check

```bash
python scripts/check_public_snapshot.py .
python scripts/public_smoke_test.py --rounds 1 --seed 42
```

The public smoke is offline and deterministic. It demonstrates artifact shape
only; it is not a formal reproduction result and it is not investment advice.

## License

This public package is distributed under the PolyForm Noncommercial License
1.0.0. Commercial use requires separate permission.
