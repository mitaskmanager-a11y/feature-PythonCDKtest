param()
Write-Host "Running black + isort (if installed)..."

$black = (Get-Command black -ErrorAction SilentlyContinue)
$isort = (Get-Command isort -ErrorAction SilentlyContinue)

if ($black) { black . } else { Write-Host "black not found (optional)" }
if ($isort) { isort . } else { Write-Host "isort not found (optional)" }

Write-Host "Basic flake8-like checks via pyflakes (if available)"
$pyflakes = (Get-Command pyflakes -ErrorAction SilentlyContinue)
if ($pyflakes) { pyflakes . } else { Write-Host "pyflakes not found (optional)" }
