from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_license_and_package_metadata_are_noncommercial() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    package_lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))

    assert "PolyForm Noncommercial License 1.0.0" in license_text
    assert "Apache License" not in license_text
    assert package_json["name"] == "civic-market-engine-public"
    assert package_json["license"] == "SEE LICENSE IN LICENSE"
    assert package_lock["name"] == "civic-market-engine-public"
    assert package_lock["packages"][""]["license"] == "SEE LICENSE IN LICENSE"


def test_container_template_has_no_oasis_or_key_like_secret() -> None:
    files = [
        ROOT / ".container" / "README.md",
        ROOT / ".container" / "Dockerfile",
        ROOT / ".container" / "docker-compose.yaml",
        ROOT / ".container" / ".env.example",
    ]
    joined = "\n".join(path.read_text(encoding="utf-8") for path in files)

    assert "OASIS" not in joined
    assert "oasis" not in joined
    assert "sk-" not in joined
    assert "OPENAI_API_KEY=replace-with-your-openai-api-key" in joined


def test_public_snapshot_checker_blocks_generated_artifacts(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# demo\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_public_snapshot.py"), str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0

    forbidden = tmp_path / "results" / "run_1"
    forbidden.mkdir(parents=True)
    (forbidden / "simulation.db").write_text("not a real db", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_public_snapshot.py"), str(tmp_path), "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["findings"][0]["path"].startswith("results/")


def test_public_snapshot_checker_blocks_private_boundaries(tmp_path: Path) -> None:
    private_files = [
        tmp_path / "AGENTS.md",
        tmp_path / "prompts" / "buyer_prompts.py",
        tmp_path / "formal_reproduction" / "command_builder.py",
        tmp_path / "reports" / "g18_post_upload_live_smoke_20260611.md",
        tmp_path / "agent_behavior.py",
        tmp_path / "transaction_engine.py",
    ]
    for path in private_files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_public_snapshot.py"), str(tmp_path), "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    paths = {item["path"] for item in payload["findings"]}
    assert "AGENTS.md" in paths
    assert "prompts/buyer_prompts.py" in paths
    assert "formal_reproduction/command_builder.py" in paths
    assert "reports/g18_post_upload_live_smoke_20260611.md" in paths
    assert "agent_behavior.py" in paths
    assert "transaction_engine.py" in paths


def test_public_snapshot_checker_blocks_secret_like_content(tmp_path: Path) -> None:
    fake_key = "sk-" + "your-real-key-here"
    (tmp_path / "README.md").write_text(f"OPENAI_API_KEY={fake_key}\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_public_snapshot.py"), str(tmp_path), "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["findings"][0]["reason"].startswith("sensitive content pattern:")


def test_public_snapshot_checker_blocks_prompt_constant_content(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text('BUYER_PREFERENCE_TEMPLATE = """private prompt"""\n', encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_public_snapshot.py"), str(tmp_path), "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["findings"][0]["reason"].startswith("sensitive content pattern:")


def test_public_snapshot_builder_creates_clean_snapshot(tmp_path: Path) -> None:
    snapshot_dir = tmp_path / "civic_public_snapshot"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_public_snapshot.py"),
            "--output",
            str(snapshot_dir),
            "--force",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["public_name"] == "CivicMarketEngine"
    assert (snapshot_dir / "SNAPSHOT_MANIFEST.json").exists()
    assert (snapshot_dir / "scripts" / "public_smoke_test.py").exists()
    assert (snapshot_dir / "docs" / "PUBLIC_RELEASE_BOUNDARY.md").exists()
    assert not (snapshot_dir / ".git").exists()
    assert not (snapshot_dir / "results").exists()
    assert not (snapshot_dir / "output").exists()
    assert not (snapshot_dir / "logs").exists()
    assert not (snapshot_dir / "node_modules").exists()
    assert not (snapshot_dir / "AGENTS.md").exists()
    assert not (snapshot_dir / "NIGHT_RUN.md").exists()
    assert not (snapshot_dir / "prompts").exists()
    assert not (snapshot_dir / "formal_reproduction").exists()
    assert not (snapshot_dir / "reports").exists()
    assert not (snapshot_dir / "agent_behavior.py").exists()
    assert not (snapshot_dir / "transaction_engine.py").exists()
    assert not (snapshot_dir / "simulation_runner.py").exists()
    assert not (snapshot_dir / ".env.deepseek.example").exists()
    assert not (snapshot_dir / "scripts" / "run_formal_medium_matrix.py").exists()
    assert not (snapshot_dir / "scripts" / "run_night_simulation.ps1").exists()
    smoke = subprocess.run(
        [sys.executable, str(snapshot_dir / "scripts" / "public_smoke_test.py"), "--rounds", "1", "--seed", "42"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert smoke.returncode == 0, smoke.stderr
    smoke_payload = json.loads(smoke.stdout)
    assert smoke_payload["ok"] is True
    assert smoke_payload["mode"] == "offline_public_demo"


def test_public_release_text_is_clean() -> None:
    targets = [
        ROOT / ".container",
    ]
    forbidden_terms = ["库存厚度", "承接结构", "07_PPT母版_20260503/output", "07_PPT母版_20260503\\output"]
    checked_suffixes = {".md", ".txt", ".json", ".cjs", ".py", ".ps1"}
    hits: list[str] = []
    for target in targets:
        for path in target.rglob("*"):
            if path.is_file() and path.suffix in checked_suffixes:
                text = path.read_text(encoding="utf-8", errors="ignore")
                for term in forbidden_terms:
                    if term in text:
                        hits.append(f"{path.relative_to(ROOT)}: {term}")
    assert hits == []
