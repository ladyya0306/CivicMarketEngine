#!/usr/bin/env python
"""Build a sanitized source-visible noncommercial public package.

The public package is intentionally not a raw copy of the private research
workspace. It contains a small offline demo, licensing material, and disclosure
boundaries while excluding private prompts, formal reproduction harnesses,
live-run artifacts, internal reports, and AGENTS.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_NAME = "CivicMarketEngine"
PUBLIC_PACKAGE = "civic-market-engine-public"
DEFAULT_NAME = f"civic_market_engine_public_snapshot_{dt.datetime.now().strftime('%Y%m%d')}"


ROOT_COPY_FILES = [
    ".gitignore",
    "ATTRIBUTION.md",
    "LICENSE",
    "NOTICE",
]

SAFE_SOURCE_FILES = [
    "database.py",
    "models.py",
    "mortgage_system.py",
    "property_initializer.py",
]

SCRIPT_FILES = [
    "scripts/build_public_snapshot.py",
    "scripts/check_public_snapshot.py",
    "scripts/public_smoke_test.py",
]

TEST_FILES = [
    "tests/test_public_package.py",
]

TREE_RULES = [
    (".container", {".example", ".md", ".ps1", ".yaml", ".yml", ""}),
    ("licenses", {".txt"}),
]

PRIVATE_BOUNDARIES = [
    "AGENTS.md",
    "prompts/",
    "agent_behavior.py",
    "transaction_engine.py",
    "simulation_runner.py",
    "formal_reproduction/",
    "reports/",
    "results/",
    "live LLM run outputs",
    "stage gate reports",
    "formal reproduction matrices",
    "internal prompt and boundary documents",
]

EXCLUDED_PARTS = {
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
    "venv",
}

EXCLUDED_NAMES = {
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

EXCLUDED_PREFIXES = (
    "autopilot_release_loop",
    "continue_formal_medium_matrix",
    "night_run_",
    "rebuild_proof_matrix_",
    "run_formal_medium_matrix",
    "run_night",
)


README_TEXT = """# CivicMarketEngine

## 中文

`CivicMarketEngine` 是一个非商业、脱敏的房地产市场模拟演示包。

它想回答的不是“明天房价涨不涨”，也不是“你该买哪套房”。它更像一个复盘工具，帮我们把一句很笼统的话拆开：市场到底冷不冷，为什么你看中的那套房还是不便宜，为什么有些房子能成交，有些房子谈着谈着就停住了。

现实里买房、卖房，很容易被一句“市场冷”或“市场热”带走。但真正落到一套房上，还是要回到几个笨问题：

- 谁会来买？
- 这些人的预算够不够？
- 同地段、同价位、同户型的替代房多不多？
- 卖家愿不愿意让价？
- 谈判最后有没有真的走到交割？

这个公开仓库保留的是可以公开看的外壳、说明、离线演示和少量安全源码。完整私有研究工作区、真实提示词、内部报告、长时间运行结果和关键边界材料没有放进来。

## English

`CivicMarketEngine` is a source-visible, noncommercial, sanitized demo package for a real-estate market simulation project.

It is not here to tell you whether prices will rise tomorrow, and it does not tell anyone which home to buy. Think of it more as a review tool: it breaks a vague market sentence into concrete questions. Is the market really cold? Why is one home still hard to bargain down? Why do some deals close while others stop halfway?

In real housing decisions, it is easy to get pulled around by big labels like "hot market" or "cold market". For one specific home, the better questions are simpler:

- Who might actually buy it?
- Can those buyers afford it?
- How many similar homes can replace it?
- Is the seller willing to move on price?
- Does the negotiation reach a real closing step?

This public repository keeps the parts that are safe to share: public-facing notes, an offline demo, packaging checks, and a small set of non-sensitive helper files. The private research workspace, real prompts, internal reports, long-run outputs, and key boundary materials are intentionally left out.

## 快速运行 / Quick Check

```bash
python scripts/check_public_snapshot.py .
python scripts/public_smoke_test.py --rounds 1 --seed 42
```

中文：这个 smoke 是离线的，只检查公开包能不能跑通，以及能不能生成临时的 `simulation.db` 和 `01_result_bundle.xlsx` 形态文件。它不是正式实验结果，也不是投资建议。

English: This smoke test is offline. It only checks that the public package can run and create temporary `simulation.db` and `01_result_bundle.xlsx` shaped artifacts. It is not a formal experiment result and it is not investment advice.

## 这个公开版包含什么 / What Is Included

- 中文：离线演示、公开说明、非商业许可、归属说明、脱敏检查器，以及少量安全源码。
- English: An offline demo, public documentation, noncommercial licensing, attribution notes, a redaction checker, and a small set of safe source files.

## 这个公开版不包含什么 / What Is Not Included

- 中文：真实提示词、内部边界文档、完整私有运行时、长时间运行结果、数据库、表格、日志、密钥和本地结果目录。
- English: Real prompts, internal boundary documents, the full private runtime, long-run outputs, databases, spreadsheets, logs, secrets, and local result folders.

## 许可 / License

中文：本公开包使用 PolyForm Noncommercial License 1.0.0。商业使用需要单独授权。

English: This public package is distributed under the PolyForm Noncommercial License 1.0.0. Commercial use requires separate permission.
"""


BOUNDARY_TEXT = """# Public Release Boundary / 公开版边界

## 中文

`CivicMarketEngine` 是非商业、可公开查看的脱敏演示包。它不是私有研究工作区的原样复制。

公开版可以放：

- 离线演示。
- 公开说明、许可、归属和最小示例。
- 不暴露真实提示词、内部边界材料和完整私有运行时的安全源码。

公开版不能放：

- 真实提示词和提示词调试策略。
- `AGENTS.md` 以及内部 LLM/代码边界说明。
- 内部实验入口、阶段报告和长时间运行矩阵。
- LLM 运行输出、结果数据库、表格、日志、缓存和本地结果目录。
- 密钥、完整本机路径和任何只适合私有仓库保存的材料。

一句话理解：这个仓库能让外部读者看懂项目想解决什么问题、能跑一个离线小演示，但不会公开私有决策口径和正式实验证据链。

## English

`CivicMarketEngine` is the noncommercial, source-visible, sanitized public demo package. It is not a full copy of the private research workspace.

The public package may include:

- Offline demos.
- Public documentation, licensing, attribution, and minimal examples.
- Safe source files that do not expose real prompts, internal boundary material, or the full private runtime.

The public package must not include:

- Real prompts or prompt tuning strategy.
- `AGENTS.md` or internal LLM/code boundary notes.
- Internal experiment entrypoints, stage reports, or long-run matrices.
- LLM run outputs, result databases, spreadsheets, logs, caches, or local result folders.
- Secrets, full local machine paths, or anything that belongs only in the private repository.

In plain terms: this repository should help outside readers understand the idea and run a small offline demo, without exposing the private decision boundary or formal experiment evidence chain.
"""


REQUIREMENTS_TEXT = """openpyxl>=3.1
pytest>=7.4.0
"""


EXAMPLE_README_TEXT = """# Minimal Public Smoke

This example runs the offline public demo only. It does not call live LLMs and
does not import the private full simulation runtime.

From the public package root:

```powershell
powershell -ExecutionPolicy Bypass -File ./examples/cli_minimal_repro/run_mock_smoke.ps1
```

Equivalent direct command:

```powershell
python ./scripts/public_smoke_test.py --rounds 1 --seed 42
```

The smoke creates temporary `simulation.db` and `01_result_bundle.xlsx` files
and deletes them automatically unless `--keep-output` is passed to the Python
script. This is an artifact-shape check, not formal reproduction evidence.
"""


EXAMPLE_PS1_TEXT = """Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

python ./scripts/public_smoke_test.py --rounds 1 --seed 42
"""


CONTAINER_README_TEXT = """# CivicMarketEngine Development Container

This folder contains an optional local development container for the public
noncommercial demo package. It is intended for repeatable local checks and
does not include private credentials, private prompt material, or generated
run results.

## Prerequisites

- Docker: https://docs.docker.com/engine/install/
- Docker Compose: https://docs.docker.com/compose/install/

## Configure Environment

Create a local `.env` file from the public template only when needed. Do not
commit `.env`.

```bash
cd .container
cp .env.example .env
```

The offline public smoke test does not require external service credentials.

## Start Container

```bash
docker compose up -d
```

## Enter the Container

```bash
docker compose exec atlas-market-engine bash
```

Typical public checks:

```bash
python scripts/check_public_snapshot.py .
python scripts/public_smoke_test.py --rounds 1 --seed 42
python -m pytest tests/test_public_package.py -q
```

## Stop and Remove

```bash
docker compose down
```

## Public Package Boundary

The container setup is a development aid only. Public snapshots must still
exclude local `.env` files, result folders, logs, databases, spreadsheets,
caches, and any private research workspace material.
"""


def _as_rel(path: str) -> Path:
    return Path(path.replace("/", "\\"))


def _assert_safe_output(output_dir: Path) -> Path:
    output_dir = output_dir.resolve()
    source_root = ROOT.resolve()
    if output_dir == source_root or source_root in output_dir.parents:
        raise RuntimeError(f"Refuse to build a snapshot inside the source tree: {output_dir}")
    if output_dir.anchor == str(output_dir):
        raise RuntimeError(f"Refuse to use a drive root as output: {output_dir}")
    return output_dir


def _reset_output_dir(output_dir: Path, *, force: bool) -> None:
    if output_dir.exists():
        if not force:
            raise RuntimeError(f"Output directory already exists. Pass --force to replace it: {output_dir}")
        if not output_dir.is_dir():
            raise RuntimeError(f"Output path exists but is not a directory: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def _should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if set(rel.parts) & EXCLUDED_PARTS:
        return True
    if path.name in EXCLUDED_NAMES:
        return True
    if path.suffix.lower() in {".db", ".db-journal", ".sqlite", ".xlsx", ".pyc", ".log", ".tmp"}:
        return True
    return any(path.name.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def _copy_file(rel_path: Path, output_dir: Path, copied: list[str], *, required: bool = True) -> None:
    src = ROOT / rel_path
    if not src.exists():
        if required:
            raise FileNotFoundError(f"Required public package file is missing: {rel_path.as_posix()}")
        return
    if _should_skip(src):
        return
    dst = output_dir / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    rel_posix = rel_path.as_posix()
    if rel_posix not in copied:
        copied.append(rel_posix)


def _copy_tree(rel_dir: Path, suffixes: set[str], output_dir: Path, copied: list[str]) -> None:
    src_dir = ROOT / rel_dir
    if not src_dir.exists():
        return
    for src in sorted(src_dir.rglob("*")):
        if not src.is_file() or _should_skip(src):
            continue
        suffix = src.suffix.lower()
        if suffix not in suffixes and "" not in suffixes:
            continue
        rel_path = src.relative_to(ROOT)
        _copy_file(rel_path, output_dir, copied)


def _write_text_file(output_dir: Path, rel_path: str, text: str, copied: list[str]) -> None:
    rel = _as_rel(rel_path)
    dst = output_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text.rstrip() + "\n", encoding="utf-8")
    rel_posix = rel.as_posix()
    if rel_posix not in copied:
        copied.append(rel_posix)


def _write_json_file(output_dir: Path, rel_path: str, payload: dict, copied: list[str]) -> None:
    rel = _as_rel(rel_path)
    dst = output_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rel_posix = rel.as_posix()
    if rel_posix not in copied:
        copied.append(rel_posix)


def _write_generated_public_files(output_dir: Path, copied: list[str]) -> None:
    _write_text_file(output_dir, "README.md", README_TEXT, copied)
    _write_text_file(output_dir, ".container/README.md", CONTAINER_README_TEXT, copied)
    _write_text_file(output_dir, "docs/PUBLIC_RELEASE_BOUNDARY.md", BOUNDARY_TEXT, copied)
    _write_text_file(output_dir, "examples/cli_minimal_repro/README.md", EXAMPLE_README_TEXT, copied)
    _write_text_file(output_dir, "examples/cli_minimal_repro/run_mock_smoke.ps1", EXAMPLE_PS1_TEXT, copied)
    _write_text_file(output_dir, "requirements.txt", REQUIREMENTS_TEXT, copied)
    _write_json_file(
        output_dir,
        "package.json",
        {
            "name": PUBLIC_PACKAGE,
            "version": "1.0.0",
            "description": "Source-visible noncommercial public demo for CivicMarketEngine.",
            "scripts": {
                "test:public": "python -m pytest tests/test_public_package.py -q",
                "smoke:public": "python scripts/public_smoke_test.py --rounds 1 --seed 42",
                "check:public": "python scripts/check_public_snapshot.py .",
            },
            "license": "SEE LICENSE IN LICENSE",
        },
        copied,
    )
    _write_json_file(
        output_dir,
        "package-lock.json",
        {
            "name": PUBLIC_PACKAGE,
            "version": "1.0.0",
            "lockfileVersion": 3,
            "requires": True,
            "packages": {
                "": {
                    "name": PUBLIC_PACKAGE,
                    "version": "1.0.0",
                    "license": "SEE LICENSE IN LICENSE",
                }
            },
        },
        copied,
    )


def _write_manifest(output_dir: Path, copied: list[str]) -> Path:
    manifest = {
        "name": DEFAULT_NAME,
        "public_name": PUBLIC_NAME,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "profile": "source-visible-noncommercial-sanitized",
        "license": "PolyForm Noncommercial License 1.0.0",
        "copied_file_count": len(copied),
        "copied_files": sorted(set(copied)),
        "private_boundaries_excluded": PRIVATE_BOUNDARIES,
        "excluded_boundaries": sorted(EXCLUDED_PARTS | EXCLUDED_NAMES),
        "notes": [
            "This package is generated by whitelist copying plus generated public files.",
            "It intentionally excludes private prompts, AGENTS.md, formal reproduction harnesses, internal reports, live LLM outputs, local run results, logs, caches, databases, spreadsheets, and secrets.",
        ],
    }
    manifest_path = output_dir / "SNAPSHOT_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def _scan_snapshot(output_dir: Path) -> list[dict[str, str]]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from scripts.check_public_snapshot import scan_snapshot

    return scan_snapshot(output_dir)


def _make_zip(output_dir: Path, *, force: bool) -> Path:
    zip_path = output_dir.with_suffix(".zip")
    if zip_path.exists():
        if not force:
            raise RuntimeError(f"Zip already exists. Pass --force to replace it: {zip_path}")
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(output_dir).as_posix())
    return zip_path


def build_snapshot(output_dir: Path, *, force: bool = False, make_zip: bool = False) -> dict[str, object]:
    output_dir = _assert_safe_output(output_dir)
    _reset_output_dir(output_dir, force=force)

    copied: list[str] = []
    for item in ROOT_COPY_FILES + SAFE_SOURCE_FILES + SCRIPT_FILES + TEST_FILES:
        _copy_file(_as_rel(item), output_dir, copied)
    for rel_dir, suffixes in TREE_RULES:
        _copy_tree(_as_rel(rel_dir), suffixes, output_dir, copied)
    _write_generated_public_files(output_dir, copied)

    manifest_path = _write_manifest(output_dir, copied)
    findings = _scan_snapshot(output_dir)
    if findings:
        raise RuntimeError("Snapshot checker failed:\n" + json.dumps(findings, ensure_ascii=False, indent=2))

    zip_path = _make_zip(output_dir, force=force) if make_zip else None
    return {
        "ok": True,
        "public_name": PUBLIC_NAME,
        "snapshot_dir": str(output_dir),
        "manifest": str(manifest_path),
        "copied_file_count": len(set(copied)),
        "zip": str(zip_path) if zip_path else "",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Build a clean {PUBLIC_NAME} public snapshot.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT.parent / DEFAULT_NAME,
        help="Output directory. Defaults to a sibling of the current repository.",
    )
    parser.add_argument("--force", action="store_true", help="Replace the output directory if it already exists.")
    parser.add_argument("--zip", action="store_true", help="Also create a .zip next to the output directory.")
    args = parser.parse_args(argv)

    try:
        result = build_snapshot(args.output, force=bool(args.force), make_zip=bool(args.zip))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
