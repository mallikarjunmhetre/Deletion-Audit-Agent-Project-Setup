# Deletion-Audit-Agent-Project-Setup
Ghost-Audit — Northstar Shop Deletion Audit Agent
# Ghost-Audit — Northstar Shop Deletion Audit Agent

## Overview
Deterministic, LLM-assisted pipeline that audits customer deletion requests.
For each case it outputs:
```
case_id, deletion_status, steps_json
```
`deletion_status` ∈ `{COMPLETE | INCOMPLETE | NOT_APPLICABLE}`

## Setup
```bash
pip install -r requirements.txt
# Set your Anthropic API key (never stored in config.yaml)
export ANTHROPIC_API_KEY=sk-ant-...
```

## Quick Start
```bash
# Audit all 518 cases
python src/main.py --input dataset/deletion_requests.csv --output output.csv

# Single case
python src/main.py --input dataset/deletion_requests.csv --output output.csv --case-id CASE_001

# First 10 cases only
python src/main.py --input dataset/deletion_requests.csv --output output.csv --limit 10

# Explore dataset schemas before running
python src/explore.py --dataset dataset/
```

## Architecture
```
load_data → intent → identity → evidence → state → rules → steps → validate → CSV
                                                                  ↑
                                              llm.py (cached, logged)
```

| Module | Purpose |
|---|---|
| `load_data.py` | Load & normalise all CSVs; parse timestamps |
| `intent.py` | Detect deletion intent (regex + LLM fallback) |
| `identity.py` | Resolve current & historical identifiers |
| `evidence.py` | Parse PDF/image/JSON/SQL evidence files |
| `state.py` | Reconstruct record state at audit_at |
| `rules.py` | Apply deletion_rules.csv; classify gaps |
| `steps.py` | Build ordered FINDING/REMEDIATION/VERIFICATION steps |
| `validate.py` | Assert output schema & ordering rules |
| `llm.py` | Anthropic wrapper with disk cache & token logging |

## Where the LLM is Used (and Why)
1. **Intent classification** — only when keyword rules return confidence < 0.80 (free-text edge cases).
2. **Evidence extraction** — only for unstructured PDF/image content that OCR cannot structure.

All LLM calls are cached by `sha256(model+prompt+system)` → `.cache/llm/`.
Token usage is logged to `evaluation/llm_calls.jsonl`.

## Evaluation
```bash
python evaluation/evaluate.py --pred output.csv --gold dataset/sample_output.csv
python evaluation/make_usage_report.py   # reads evaluation/llm_calls.jsonl
```

## Config
Edit `config.yaml` for model, paths, and pricing. **Never put API keys in config.yaml.**

## Package for Submission
```bash
bash package.sh   # produces code.zip (secrets scan included)
```
