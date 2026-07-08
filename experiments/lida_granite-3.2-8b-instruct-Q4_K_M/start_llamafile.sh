#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODEL_URL="${LLAMAFILE_MODEL_URL:-}"
MODEL_PATH="${LLAMAFILE_MODEL_PATH:-$SCRIPT_DIR/models/granite-3.2-8b-instruct-Q4_K_M.llamafile}"
SERVED_MODEL="${LIDA_MODEL:-granite-3.2-8b-instruct-Q4_K_M}"
HOST="${LLAMAFILE_HOST:-0.0.0.0}"
PORT="${LLAMAFILE_PORT:-8000}"
API_KEY="${LLAMAFILE_API_KEY:-}"
API_PREFIX="${LLAMAFILE_API_PREFIX:-/v1}"
N_GPU_LAYERS="${LLAMAFILE_N_GPU_LAYERS:-999}"
CTX_SIZE="${LLAMAFILE_CTX_SIZE:-8000}"
# N_PREDICT="${LLAMAFILE_N_PREDICT:-256}"
CHAT_TEMPLATE="${LLAMAFILE_CHAT_TEMPLATE:-}" # chatml
REQUEST_TIMEOUT="${LLAMAFILE_TIMEOUT:-60}"
LOG_FILE="${LLAMAFILE_LOG_FILE:-llamafile.log}"
PID_FILE="${LLAMAFILE_PID_FILE:-.llamafile.pid}"

if [[ -f "$PID_FILE" ]]; then
  EXISTING_PID="$(cat "$PID_FILE")"
  if [[ -n "$EXISTING_PID" ]] && kill -0 "$EXISTING_PID" 2>/dev/null; then
    echo "llamafile is already running with PID $EXISTING_PID"
    echo "If this is stale, run: LLAMAFILE_PID_FILE=$PID_FILE bash stop_llamafile.sh"
    exit 0
  else
    echo "Removing stale PID file: $PID_FILE"
    rm -f "$PID_FILE"
  fi
fi

mkdir -p "$(dirname "$MODEL_PATH")"

if [[ -f "$MODEL_PATH" ]]; then
  echo "Using local model file: $MODEL_PATH"
else
  echo "Model file not found: $MODEL_PATH"
  echo "Set LLAMAFILE_MODEL_PATH to an existing file."
  exit 1
fi

chmod +x "$MODEL_PATH"

echo "Starting llamafile server"
echo "Model file: $MODEL_PATH"
echo "Served model name: $SERVED_MODEL"
echo "Endpoint: http://$HOST:$PORT$API_PREFIX"
echo "GPU layers: $N_GPU_LAYERS"
echo "Context size: $CTX_SIZE"
# echo "Max generated tokens per request: $N_PREDICT"
echo "Chat template: $CHAT_TEMPLATE"
echo "Request timeout: $REQUEST_TIMEOUT"
echo "GPU layers (raw): $N_GPU_LAYERS"
echo "Tip: Increase LLAMAFILE_N_GPU_LAYERS gradually (e.g. 10, 20, 30) if you have free VRAM."

CMD=(
  "$MODEL_PATH"
  --server
  --host "$HOST"
  --port "$PORT"
  -a "$SERVED_MODEL"
  -c "$CTX_SIZE"
  # -n "$N_PREDICT"
)

if [[ "$N_GPU_LAYERS" =~ ^-?[0-9]+$ ]]; then
  CMD+=(-ngl "$N_GPU_LAYERS")
else
  echo "Warning: LLAMAFILE_N_GPU_LAYERS must be an integer, got '$N_GPU_LAYERS'. Skipping -ngl."
fi

if [[ -n "$CHAT_TEMPLATE" ]]; then
  CMD+=(--chat-template "$CHAT_TEMPLATE")
fi

if "$MODEL_PATH" --help 2>&1 | grep -q -- '--timeout'; then
  CMD+=(--timeout "$REQUEST_TIMEOUT")
else
  echo "Warning: This llamafile build does not expose --timeout; keeping default behavior."
fi

if [[ -n "$API_KEY" ]] && [[ "$API_KEY" != "EMPTY" ]]; then
  CMD+=(--api-key "$API_KEY")
fi

nohup "${CMD[@]}" > "$LOG_FILE" 2>&1 &

PID=$!
echo "$PID" > "$PID_FILE"

echo "llamafile PID: $PID"
echo "Waiting for server readiness..."

for i in $(seq 1 120); do
  if [[ -n "$API_KEY" ]] && [[ "$API_KEY" != "EMPTY" ]]; then
    if curl -fsS -H "Authorization: Bearer $API_KEY" "http://127.0.0.1:${PORT}${API_PREFIX}/models" >/dev/null 2>&1; then
      echo "llamafile is ready at http://127.0.0.1:${PORT}${API_PREFIX}"
      exit 0
    fi
  else
    if curl -fsS "http://127.0.0.1:${PORT}${API_PREFIX}/models" >/dev/null 2>&1; then
      echo "llamafile is ready at http://127.0.0.1:${PORT}${API_PREFIX}"
      exit 0
    fi
  fi

  if ! kill -0 "$PID" 2>/dev/null; then
    echo "llamafile exited before becoming ready. Check $LOG_FILE"
    tail -n 60 "$LOG_FILE" || true
    rm -f "$PID_FILE"
    exit 1
  fi

  sleep 1
done

echo "Timed out waiting for llamafile readiness. Check $LOG_FILE"
rm -f "$PID_FILE"
exit 1