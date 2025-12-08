"""
Setup configuration for PyMeter
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pymeter",
    version="0.1.0",
    author="Dr. Pedro E. Colla (LU7DZ)",
    description="Python based generic meter for ham radio stations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lu7did/PyMeter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Ham Radio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'pymeter=pymeter.cli:main',
        ],
    },
)
