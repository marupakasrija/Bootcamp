from setuptools import setup, find_packages

setup(
    name='srija-hello',
    version='0.3.1',
    packages=find_packages(),
    install_requires=[
        'typer>=0.9.0',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'srija-hello = cli_app.main:app',
        ],
    },
    author="Srija",
    description="A CLI tool that greets you and gives a motivational quote",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
