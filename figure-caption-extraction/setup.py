from setuptools import setup, find_namespace_packages

setup(
    name="figure-caption-extraction",
    version="0.1",
    packages=find_namespace_packages(include=["src.*"]),
    package_dir={"":"."},
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
)