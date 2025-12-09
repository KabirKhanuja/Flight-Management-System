set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/cpp_bindings"

if [ -f "$ROOT/.venv/bin/activate" ]; then
  echo "Activating venv..."
  source "$ROOT/.venv/bin/activate"
fi

echo "Installing build deps..."
python3 -m pip install --upgrade pip setuptools wheel pybind11

echo "Building extension in-place..."
python3 setup.py build_ext --inplace

echo "Build finished. The compiled module should be in cpp_bindings/ (flight_fms_cpp*.so)"