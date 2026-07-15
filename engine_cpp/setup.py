from setuptools import setup, Extension
import pybind11

# Define the extension module
ext_modules = [
    Extension(
        "image_engine_cpp",  # Name of the module
        ["engine_cpp/pipeline.cpp"],  # Source file
        include_dirs=[pybind11.get_include()],  # Where to find pybind11 headers
        language="c++",
        extra_compile_args=["/O2", "/openmp"],  # Windows/MSVC optimization flag
    ),
]

setup(
    name="image_engine_cpp",
    version="1.0",
    ext_modules=ext_modules,
)
