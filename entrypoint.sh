#!/bin/sh
# Strix entrypoint script

# Ensure /opt/agent is in the Python path so "agent" imports work
export PYTHONPATH=/opt/agent

echo "[*] Launching Strix Recon Agent..."
exec python3 /opt/agent/main.py "$@"
