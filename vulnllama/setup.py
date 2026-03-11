from setuptools import setup

setup(
    name="vulnllama",
    version="0.1",
    packages=["vulnllama"],
    entry_points={
        "console_scripts": [
            "vulnllama=vulnllama.cli:main"
        ]
    },
)