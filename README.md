## Quick Start (How to Run)

Open a terminal in the project root:

1. (Optional) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies

```bash
pip install -r requirements.txt
pip install pybind11
```

3. Build the C++ extension with pybind11

```bash
cd cpp_bindings
python3 setup.py build_ext --inplace
cd ..
```

4. Run a quick import test (optional, but good to verify)

```bash
PYTHONPATH="$(pwd)/python_package:$(pwd)/cpp_bindings:${PYTHONPATH:-}" \
	python3 -c "import flight_fms_cpp; print('OK:', [n for n in dir(flight_fms_cpp) if not n.startswith('_')])"
```

5. Run the Streamlit web app

```bash
PYTHONPATH="$(pwd)/python_package:$(pwd)/cpp_bindings:${PYTHONPATH:-}" \
	streamlit run web/app.py
```

---

The C++ CLI version (menu-based console app) can be built and run separately from the `cpp` folder:

```bash
cd cpp
g++ FMS.cpp -o FMS -std=c++17
./FMS
```

