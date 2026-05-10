# check-surface-sync.ps1 — runs both pre-commit gates
$ScriptDir = Split-Path -Parent $PSCommandPath
$syncRC = 0; $integrityRC = 0

Write-Host "── check-surface-sync ──"
python (Join-Path $ScriptDir "check-surface-sync.py") @args
$syncRC = $LASTEXITCODE

Write-Host ""
Write-Host "── check-skill-integrity ──"
python (Join-Path $ScriptDir "check-skill-integrity.py") @args
$integrityRC = $LASTEXITCODE

if ($syncRC -gt $integrityRC) { exit $syncRC } else { exit $integrityRC }