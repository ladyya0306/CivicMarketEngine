#!/usr/bin/env python
"""Check a public or registration snapshot for forbidden local artifacts."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path


FORBIDDEN_DIRS = {
    ".codex",
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "archive",
    "build",
    "dist",
    "env",
    "formal_reproduction",
    "logs",
    "node_modules",
    "output",
    "prompts",
    "reports",
    "results",
    "tmp_atlas_rebuild_backup",
    "venv",
}

FORBIDDEN_NAMES = {
    ".env",
    ".env.deepseek",
    ".env.deepseek.example",
    ".llm_exact_cache.sqlite3",
    "AGENTS.md",
    "NIGHT_RUN.md",
    "agent_behavior.py",
    "order_lifecycle.log",
    "simulation_run.log",
    "simulation_runner.py",
    "test_reporting.db",
    "transaction_engine.py",
}

FORBIDDEN_NAME_PATTERNS = {
    "autopilot_release_loop*.ps1",
    "continue_formal_medium_matrix_after_pid.ps1",
    "night_run_*",
    "rebuild_proof_matrix_*.ps1",
    "run_formal_medium_matrix.py",
    "run_night*",
}

FORBIDDEN_SUFFIXES = {
    ".db",
    ".db-journal",
    ".sqlite",
    ".xlsx",
    ".pyc",
    ".log",
    ".tmp",
}

TEXT_SUFFIXES = {
    ".cjs",
    ".css",
    ".example",
    ".html",
    ".js",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

TEXT_NAMES = {
    ".flake8",
    ".gitignore",
    "ATTRIBUTION.md",
    "LICENSE",
    "NOTICE",
    "README.md",
}

TOOLING_RULE_FILES = {
    "SNAPSHOT_MANIFEST.json",
    "scripts/build_public_snapshot.py",
    "scripts/check_public_snapshot.py",
    "tests/test_public_package.py",
}

SENSITIVE_CONTENT_PATTERNS = [
    ("OpenAI-style key-like token", re.compile(r"\bsk-[A-Za-z0-9][A-Za-z0-9_-]{7,}\b")),
    ("local Windows development path", re.compile(r"\b[A-Za-z]:\\(?:GitProj|Users\\[^\\\s]+)\\", re.IGNORECASE)),
    ("local Windows markdown path", re.compile(r"/[A-Za-z]:/[^)\s>]+", re.IGNORECASE)),
    ("local file URI", re.compile(r"file:///[A-Za-z]:/", re.IGNORECASE)),
    (
        "private prompt constant assignment",
        re.compile(
            r"\b("
            r"BATCH_ROLE_SYSTEM_PROMPT|BUYER_SELLER_CHAIN_SYSTEM_PROMPT|"
            r"BUYER_PREFERENCE_TEMPLATE|BUYER_MATCHING_TEMPLATE|"
            r"LISTING_STRATEGY_TEMPLATE|PRICE_ADJUSTMENT_TEMPLATE|"
            r"BUYER_NEGOTIATION_TEMPLATE|SELLER_NEGOTIATION_TEMPLATE"
            r")\s*=",
            re.IGNORECASE,
        ),
    ),
    (
        "formal reproduction internal material",
        re.compile(
            r"(formal_reproduction|run_formal_medium_matrix|force_raise_only|"
            r"阶段性方案_正式复现入口|G[0-9]+ .*gate|live LLM smoke)",
            re.IGNORECASE,
        ),
    ),
]


def _is_forbidden(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root)
    parts = set(rel.parts)
    matched_dirs = sorted(parts & FORBIDDEN_DIRS)
    if matched_dirs:
        return f"forbidden directory: {matched_dirs[0]}"
    if path.name in FORBIDDEN_NAMES:
        return f"forbidden file name: {path.name}"
    if path.name.startswith(".env.") and path.name != ".env.example":
        return f"forbidden env-like file name: {path.name}"
    for pattern in sorted(FORBIDDEN_NAME_PATTERNS):
        if fnmatch.fnmatch(path.name, pattern):
            return f"forbidden file pattern: {pattern}"
    for suffix in FORBIDDEN_SUFFIXES:
        if path.name.endswith(suffix):
            return f"forbidden suffix: {suffix}"
    return None


def _is_text_candidate(path: Path) -> bool:
    return path.name in TEXT_NAMES or path.suffix.lower() in TEXT_SUFFIXES


def _scan_sensitive_content(path: Path, root: Path) -> str | None:
    if not _is_text_candidate(path):
        return None
    rel_posix = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return f"cannot read text content: {exc}"
    for label, pattern in SENSITIVE_CONTENT_PATTERNS:
        if rel_posix in TOOLING_RULE_FILES and label in {
            "formal reproduction internal material",
            "private prompt constant assignment",
        }:
            continue
        if pattern.search(text):
            return f"sensitive content pattern: {label}"
    return None


def scan_snapshot(root: Path) -> list[dict[str, str]]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        reason = _is_forbidden(path, root)
        if reason:
            findings.append({"path": path.relative_to(root).as_posix(), "reason": reason})
            continue
        reason = _scan_sensitive_content(path, root)
        if reason:
            findings.append({"path": path.relative_to(root).as_posix(), "reason": reason})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify that a public or software-registration snapshot excludes local artifacts."
    )
    parser.add_argument(
        "snapshot_dir",
        type=Path,
        help="Directory to inspect. Run this against the clean snapshot, not the dirty development tree.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    root = args.snapshot_dir.resolve()
    if not root.exists() or not root.is_dir():
        print(f"Snapshot directory does not exist: {root}", file=sys.stderr)
        return 2

    findings = scan_snapshot(root)
    payload = {"snapshot_dir": str(root), "ok": not findings, "findings": findings}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif findings:
        print("Forbidden files were found in the snapshot:")
        for item in findings:
            print(f"- {item['path']}: {item['reason']}")
    else:
        print(f"OK: no forbidden local artifacts found in {root}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
