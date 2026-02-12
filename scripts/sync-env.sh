#!/bin/bash
# Copy NEXT_PUBLIC_* vars from root .env to frontend/.env.local
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$ROOT/.env"
TARGET="$ROOT/frontend/.env.local"

if [ -f "$ENV_FILE" ]; then
  grep '^NEXT_PUBLIC_' "$ENV_FILE" > "$TARGET" 2>/dev/null || true
  echo "Synced NEXT_PUBLIC_* vars to frontend/.env.local"
else
  echo "No .env found at $ENV_FILE"
fi
