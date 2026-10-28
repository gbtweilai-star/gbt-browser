#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_browser info
PYTHONPATH=src python -m gbt_browser check --payload '{"url": "https://example.com"}'
PYTHONPATH=src python -m gbt_browser run   --payload '{"url": "https://example.com"}'
