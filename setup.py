from setuptools import setup

setup(
    name="trine",
    version="0.1-pre",
    license="BSD",
    description="Generate DB structures for WoW emulators with YAML.",
    packages=["trine", "trine.models"],
    install_requires=[
        "pyyaml",
        "schema",
        "sqlalchemy",
        "sweet",
        "tarjan",
    ],
    entry_points={
        "console_scripts": ["trine = trine:main"]
    }
)