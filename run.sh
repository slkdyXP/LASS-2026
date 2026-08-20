#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ -f .c2r.env ]]; then
  set -a
  source .c2r.env
  set +a
fi

if [[ -z "${C2R_API_KEY:-}" || "${C2R_API_KEY}" == "PASTE_YOUR_REAL_KEY_HERE" ]]; then
  echo "Missing C2R_API_KEY. Create .c2r.env from .c2r.env.example and place your real key there." >&2
  exit 2
fi

if [[ "$#" -eq 0 ]]; then
  set -- --config config.voting.json
fi

python3 -m social_base.run "$@"
