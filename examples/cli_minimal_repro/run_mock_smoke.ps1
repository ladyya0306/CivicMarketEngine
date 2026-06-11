Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

python ./scripts/public_smoke_test.py --rounds 1 --seed 42
