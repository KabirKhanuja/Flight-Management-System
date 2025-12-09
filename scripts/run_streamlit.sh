set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ -f "$ROOT/.venv/bin/activate" ]; then
  echo "Activating venv..."
  source "$ROOT/.venv/bin/activate"
fi

export PYTHONPATH="$ROOT/python_package:$ROOT/cpp_bindings:$PYTHONPATH"
echo "PYTHONPATH set to: $PYTHONPATH"

streamlit run "$ROOT/web/app.py"