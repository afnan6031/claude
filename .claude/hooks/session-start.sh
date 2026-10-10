#!/bin/bash
# Prepare HyperFrames rendering in Claude Code cloud sessions.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR/video"
# Downloads Chrome Headless Shell (cached in ~/.cache/hyperframes) for local rendering.
npx --yes hyperframes@0.8.144 browser ensure
