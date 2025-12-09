from setuptools import setup, Extension
import pybind11
import sysconfig
import os

pybind_includes = pybind11.get_include()
pybind_user_includes = pybind11.get_include(user=True)
python_include = sysconfig.get_path("include")

extra_pybind_path = "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/pybind11/include"

include_dirs = [
    pybind_includes,
    pybind_user_includes,
    extra_pybind_path,
    python_include,
    os.path.abspath("../cpp"),
]

ext_modules = [
    Extension(
        "flight_fms_cpp",
        sources=["bindings.cpp", "../cpp/fms_core.cpp"],
        include_dirs=include_dirs,
        language="c++",
        extra_compile_args=["-std=c++17", "-O3"],
    )
]

setup(
    name="flight_fms_cpp",
    version="0.1.0",
    author="Kabir",
    ext_modules=ext_modules,
    zip_safe=False,
)