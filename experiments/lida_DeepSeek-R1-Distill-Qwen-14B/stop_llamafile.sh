#!/bin/bash

set -euo pipefail

PID_FILE="${LLAMAFILE_PID_FILE:-.llamafile.pid}"

if [[ ! -f "$PID_FILE" ]]; then
  echo "No $PID_FILE found. Nothing to stop."
  exit 0
fi

PID="$(cat "$PID_FILE")"

if [[ -z "$PID" ]]; then
  echo "Empty PID file. Removing stale $PID_FILE"
  rm -f "$PID_FILE"
  exit 0
fi

if kill -0 "$PID" 2>/dev/null; then
  echo "Stopping llamafile (PID $PID)..."
  kill "$PID"
else
  echo "Process $PID not running. Cleaning stale PID file."
fi

rm -f "$PID_FILE"
echo "Done."
