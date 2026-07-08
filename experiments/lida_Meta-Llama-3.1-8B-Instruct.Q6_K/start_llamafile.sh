#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODEL_URL="${LLAMAFILE_MODEL_URL:-}"
MODEL_PATH="${LLAMAFILE_MODEL_PATH:-$SCRIPT_DIR/models/Meta-Llama-3.1-8B-Instruct.Q6_K.llamafile}"
SERVED_MODEL="${LIDA_MODEL:-Meta-Llama-3.1-8B-Instruct}"
HOST="${LLAMAFILE_HOST:-0.0.0.0}"
PORT="${LLAMAFILE_PORT:-8000}"
API_KEY="${LLAMAFILE_API_KEY:-}"
API_PREFIX="${LLAMAFILE_API_PREFIX:-/v1}"
N_GPU_LAYERS="${LLAMAFILE_N_GPU_LAYERS:-999}"
CTX_SIZE="${LLAMAFILE_CTX_SIZE:-20000}"
CHAT_TEMPLATE="${LLAMAFILE_CHAT_TEMPLATE:-}" # chatml
LOG_FILE="${LLAMAFILE_LOG_FILE:-llamafile.log}"
PID_FILE="${LLAMAFILE_PID_FILE:-.llamafile.pid}"

if [[ -f "$PID_FILE" ]]; then
  EXISTING_PID="$(cat "$PID_FILE")"
  if [[ -n "$EXISTING_PID" ]] && kill -0 "$EXISTING_PID" 2>/dev/null; then
    echo "llamafile is already running with PID $EXISTING_PID"
    echo "If this is stale, run: LLAMAFILE_PID_FILE=$PID_FILE bash stop_llamafile.sh"
    exit 0
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
echo "Chat template: $CHAT_TEMPLATE"
echo "GPU layers (raw): $N_GPU_LAYERS"

CMD=(
  "$MODEL_PATH"
  --server
  --host "$HOST"
  --port "$PORT"
  -a "$SERVED_MODEL"
  -c "$CTX_SIZE"
)

if [[ "$N_GPU_LAYERS" =~ ^-?[0-9]+$ ]]; then
  CMD+=(-ngl "$N_GPU_LAYERS")
else
  echo "Warning: LLAMAFILE_N_GPU_LAYERS must be an integer, got '$N_GPU_LAYERS'. Skipping -ngl."
fi

if [[ -n "$CHAT_TEMPLATE" ]]; then
  CMD+=(--chat-template "$CHAT_TEMPLATE")
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