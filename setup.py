from setuptools import setup

setup(
    name="trine",
    version="0.1-pre",
    license="BSD",
    description="Generate DB structures for WoW emulators with YAML.",
    packages=["trine", "trine.models"],
    entry_points={
        "console_scripts": ["trine = trine:main"]
    }
)