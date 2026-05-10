param([string]$LectureN)

$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$QuartoDir = Join-Path $RepoRoot "Quarto"
$DocsDir = Join-Path $RepoRoot "docs"

Write-Host "=== Syncing Quarto slides to docs/ ==="
Write-Host "Repo root: $RepoRoot"

Set-Location -Path $QuartoDir

if ($LectureN) {
    Write-Host "Rendering $LectureN..."
    $matchedQmd = Get-ChildItem -Filter "${LectureN}_*.qmd", "${LectureN}.qmd" | Select-Object -First 1
    if (-not $matchedQmd) {
        Write-Host "Error: No QMD file found matching '$LectureN'" -ForegroundColor Red
        exit 1
    }
    quarto render $matchedQmd.Name
    if (-not $?) { Write-Host "Warning: Failed to render $($matchedQmd.Name)" -ForegroundColor Yellow }
} else {
    Write-Host "Rendering all Quarto files..."
    foreach ($qmd in Get-ChildItem -Filter "*.qmd") {
        if ($qmd.Name -notlike "*_backup*") {
            Write-Host "  Rendering $($qmd.Name)..."
            quarto render $qmd.Name
            if (-not $?) { Write-Host "  Warning: Failed to render $($qmd.Name)" -ForegroundColor Yellow }
        }
    }
}

Write-Host "Syncing HTML and assets to docs/slides/..."
$SlidesDir = Join-Path $DocsDir "slides"
New-Item -ItemType Directory -Path $SlidesDir -Force | Out-Null

foreach ($html in Get-ChildItem -Filter "*.html") {
    Write-Host "  Copying $($html.Name)..."
    Copy-Item $html.FullName (Join-Path $SlidesDir $html.Name) -Force
    $filesDir = $html.Name -replace '\.html$', '_files'
    $filesPath = Join-Path $QuartoDir $filesDir
    if (Test-Path $filesPath) {
        $dest = Join-Path $SlidesDir $filesDir
        if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
        Copy-Item $filesPath $dest -Recurse -Force
    }
}

Write-Host "Syncing Beamer PDFs..."
$SlidesSource = Join-Path $RepoRoot "Slides"
foreach ($pdf in Get-ChildItem -Path $SlidesSource -Filter "*.pdf") {
    Write-Host "  Copying $($pdf.Name)..."
    Copy-Item $pdf.FullName (Join-Path $SlidesDir $pdf.Name) -Force
}

Write-Host "Syncing R scripts..."
$CodeDir = Join-Path $DocsDir "files" "code"
New-Item -ItemType Directory -Path $CodeDir -Force | Out-Null
foreach ($rScript in Get-ChildItem -Path (Join-Path $RepoRoot "scripts" "R") -Filter "*.R") {
    Write-Host "  Copying $($rScript.Name)..."
    Copy-Item $rScript.FullName (Join-Path $CodeDir $rScript.Name) -Force
}

Write-Host "Syncing Figures/..."
$FiguresSource = Join-Path $RepoRoot "Figures"
$FiguresDest = Join-Path $DocsDir "Figures"
if (Test-Path $FiguresDest) { Remove-Item $FiguresDest -Recurse -Force }
if (Test-Path $FiguresSource) { Copy-Item $FiguresSource $FiguresDest -Recurse -Force }

Write-Host ""
Write-Host "=== Sync complete! ==="
Write-Host "Files synced to: $SlidesDir"