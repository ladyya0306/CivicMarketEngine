# Minimal Public Smoke

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
