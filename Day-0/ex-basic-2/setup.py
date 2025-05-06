from setuptools import setup, find_packages

setup(
    name="srija-hello",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'srija-hello = srija_hello.hello:main',
        ],
    },
    install_requires=[
        'rich',
    ],
)
