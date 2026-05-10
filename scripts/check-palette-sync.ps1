# check-palette-sync.ps1 — thin wrapper around check-palette-sync.py
$ScriptDir = Split-Path -Parent $PSCommandPath
python (Join-Path $ScriptDir "check-palette-sync.py") @args
exit $LASTEXITCODE