param([switch]$Quiet)

$pass = 0; $warn = 0; $fail = 0

function Check-Required($Name, $Command, $InstallUrl) {
    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        $ver = & $Command --version 2>&1 | Select-Object -First 1
        if (-not $Quiet) { Write-Host "  OK $Name found: $ver" -ForegroundColor Green }
        $script:pass++
    } else {
        Write-Host "  MISSING $Name — install: $InstallUrl" -ForegroundColor Red
        $script:fail++
    }
}

function Check-Optional($Name, $Command, $InstallUrl) {
    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        $ver = & $Command --version 2>&1 | Select-Object -First 1
        if (-not $Quiet) { Write-Host "  OK $Name found: $ver" -ForegroundColor Green }
        $script:pass++
    } else {
        Write-Host "  WARN $Name not found (optional) — install: $InstallUrl" -ForegroundColor Yellow
        $script:warn++
    }
}

Write-Host "Validating academic workflow setup..." -ForegroundColor Cyan

Write-Host "Required tools:" -ForegroundColor White
Check-Required "OpenCode"    "opencode" "https://opencode.ai/download"
Check-Required "XeLaTeX"     "xelatex"  "https://tug.org/texlive/"
Check-Required "Quarto"      "quarto"   "https://quarto.org/docs/get-started/"
Check-Required "git"         "git"      "https://git-scm.com/downloads"
Check-Required "Python 3"    "python"   "https://python.org"

Write-Host "Recommended tools:" -ForegroundColor White
Check-Optional "R"           "R"        "https://www.r-project.org/"
Check-Optional "GitHub CLI"  "gh"       "https://cli.github.com/"

Write-Host "Git configuration:" -ForegroundColor White
$gitName = git config user.name 2>$null
$gitEmail = git config user.email 2>$null
if ($gitName -and $gitEmail) {
    Write-Host "  OK git user: $gitName <$gitEmail>" -ForegroundColor Green; $pass++
} else {
    Write-Host "  WARN git user.name / user.email not set" -ForegroundColor Yellow
    Write-Host "    Run: git config --global user.name `"Your Name`""
    Write-Host "    Run: git config --global user.email `"you@example.com`""
    $warn++
}

Write-Host ""
Write-Host "Summary: $pass passed, $warn warnings, $fail failed" -ForegroundColor Cyan

if ($fail -gt 0) { exit 1 }
Write-Host "Setup looks good!" -ForegroundColor Green
exit 0