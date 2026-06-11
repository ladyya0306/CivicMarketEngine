#!/usr/bin/env python
"""Run a deterministic offline smoke test for the public package.

This script deliberately avoids importing the private LLM decision layer or the
private full simulation runtime. It validates the public package shape by
creating a tiny local market artifact set in a temporary directory.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import tempfile
from pathlib import Path


def _bounded_int(value: int, *, low: int, high: int) -> int:
    return max(low, min(high, int(value)))


def _write_demo_db(db_path: Path, *, rounds: int, seed: int) -> dict[str, int]:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE agents (agent_id INTEGER PRIMARY KEY, role TEXT, cash REAL)")
        cur.execute(
            "CREATE TABLE properties (property_id INTEGER PRIMARY KEY, zone TEXT, listed_price REAL, status TEXT)"
        )
        cur.execute(
            "CREATE TABLE transaction_orders (order_id INTEGER PRIMARY KEY, round INTEGER, buyer_id INTEGER, property_id INTEGER, offer_price REAL, status TEXT)"
        )
        cur.execute(
            "CREATE TABLE transactions (transaction_id INTEGER PRIMARY KEY, round INTEGER, buyer_id INTEGER, property_id INTEGER, price REAL)"
        )

        base_cash = 600000 + (int(seed) % 1000)
        agents = [
            (1, "BUYER", base_cash),
            (2, "SELLER", base_cash + 200000),
            (3, "OBSERVER", base_cash // 2),
        ]
        properties = [
            (101, "A", 1800000.0, "for_sale"),
            (102, "B", 980000.0, "for_sale"),
        ]
        cur.executemany("INSERT INTO agents VALUES (?, ?, ?)", agents)
        cur.executemany("INSERT INTO properties VALUES (?, ?, ?, ?)", properties)

        orders = []
        transactions = []
        for round_no in range(1, int(rounds) + 1):
            offer = 960000.0 + round_no * 1000
            status = "accepted" if round_no == int(rounds) else "pending"
            orders.append((round_no, round_no, 1, 102, offer, status))
            if status == "accepted":
                transactions.append((round_no, round_no, 1, 102, offer))
        cur.executemany("INSERT INTO transaction_orders VALUES (?, ?, ?, ?, ?, ?)", orders)
        cur.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", transactions)
        conn.commit()
        return {
            "agents": len(agents),
            "properties": len(properties),
            "orders": len(orders),
            "transactions": len(transactions),
        }
    finally:
        conn.close()


def _write_demo_workbook(path: Path, payload: dict[str, object]) -> bool:
    try:
        from openpyxl import Workbook
    except Exception:
        return False

    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    ws.append(["CivicMarketEngine public smoke"])
    ws.append(["offline_only", True])
    ws.append(["official_reproduction_evidence", False])
    ws.append(["not_investment_advice", True])

    ws2 = wb.create_sheet("summary")
    ws2.append(["key", "value"])
    for key, value in payload.items():
        ws2.append([key, value])
    wb.save(path)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the CivicMarketEngine public offline smoke test.")
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--keep-output", action="store_true")
    args = parser.parse_args(argv)

    rounds = _bounded_int(args.rounds, low=1, high=3)
    seed = int(args.seed)
    temp_ctx = tempfile.TemporaryDirectory(prefix="civic_market_public_smoke_")
    out_dir = Path(temp_ctx.name)

    try:
        db_path = out_dir / "simulation.db"
        workbook_path = out_dir / "01_result_bundle.xlsx"
        counts = _write_demo_db(db_path, rounds=rounds, seed=seed)
        workbook_written = _write_demo_workbook(
            workbook_path,
            {
                "rounds": rounds,
                "seed": seed,
                **counts,
            },
        )
        payload = {
            "ok": db_path.exists() and (workbook_path.exists() if workbook_written else True),
            "mode": "offline_public_demo",
            "rounds": rounds,
            "seed": seed,
            "db_exists": db_path.exists(),
            "result_bundle_exists": workbook_path.exists(),
            "counts": counts,
            "output_dir": str(out_dir),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["ok"] else 1
    finally:
        if args.keep_output:
            print(f"Kept smoke output: {out_dir}")
        else:
            temp_ctx.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
