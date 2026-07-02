#!/usr/bin/env bash
#
# install.sh
# Creates a Python virtual environment (.venv) and installs
# dependencies from requirements.txt, retrying once on failure.

set -uo pipefail

# ---- Config ----
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"
MAX_ATTEMPTS=2
PYTHON_BIN="${PYTHON_BIN:-python3.14}"

# Always run relative to this script's own location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ---- Helper: retry a command up to MAX_ATTEMPTS times ----
run_with_retry() {
    local description="$1"
    shift
    local attempt=1

    while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
        echo ">> $description (attempt $attempt/$MAX_ATTEMPTS)"
        if "$@"; then
            return 0
        fi
        echo "!! Attempt $attempt failed."
        attempt=$((attempt + 1))
        if [ "$attempt" -le "$MAX_ATTEMPTS" ]; then
            echo "   Retrying..."
            sleep 2
        fi
    done
    return 1
}

echo "=============================================="
echo " Python venv setup"
echo "=============================================="

# 1. Make sure python3 is available
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "ERROR: '$PYTHON_BIN' not found. Install Python 3 first." >&2
    exit 1
fi

# 2. Create the virtual environment (skip if it already exists)
if [ -d "$VENV_DIR" ]; then
    echo "'$VENV_DIR' already exists, skipping creation."
else
    if ! run_with_retry "Creating virtual environment" "$PYTHON_BIN" -m venv "$VENV_DIR"; then
        echo "ERROR: Failed to create the virtual environment after $MAX_ATTEMPTS attempts." >&2
        exit 1
    fi
fi

# 3. Activate it (only affects this script's process)
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
echo "Activated: $(python -V) -> $(command -v python)"

# 4. Upgrade pip (best effort)
run_with_retry "Upgrading pip" pip install --upgrade pip

# 5. Make sure requirements.txt exists
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "ERROR: '$REQUIREMENTS_FILE' not found in $SCRIPT_DIR." >&2
    exit 1
fi

# 6. Install requirements, retrying once on failure
echo "=============================================="
echo " Installing packages from $REQUIREMENTS_FILE"
echo "=============================================="

if run_with_retry "Installing requirements" pip install -r "$REQUIREMENTS_FILE"; then
    echo "=============================================="
    echo " Done. Activate with: source $VENV_DIR/bin/activate"
    echo "=============================================="
else
    echo "=============================================="
    echo " ERROR: pip install failed after $MAX_ATTEMPTS attempts." >&2
    echo " Check the output above for details." >&2
    echo "=============================================="
    exit 1
fi