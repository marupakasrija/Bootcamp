"""
my_package/
├── mypkg/
│   ├── __init__.py
│   └── cli.py
├── pyproject.toml
└── README.md


[project]
name = "mypkg"
version = "0.1.0"
authors = [
  { name="Your Name", email="your.email@example.com" },
]
description = "A sample package"
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
"""