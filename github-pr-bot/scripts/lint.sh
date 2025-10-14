#!/usr/bin/env bash
set -euo pipefail
echo "Running black + isort (if installed)..."
if command -v black >/dev/null 2>&1; then black .; else echo "black not found (optional)"; fi
if command -v isort >/dev/null 2>&1; then isort .; else echo "isort not found (optional)"; fi

echo "Basic flake8-like checks via pyflakes (if available)"
if command -v pyflakes >/dev/null 2>&1; then pyflakes .; else echo "pyflakes not found (optional)"; fi
