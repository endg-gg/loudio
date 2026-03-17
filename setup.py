from setuptools import setup, find_packages

setup(
    name="loudio",
    version="0.1.0",
    description="Cross-platform audio streaming over UDP with Opus encoding",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "sounddevice",
        "numpy",
        "opuslib",
    ],
    entry_points={
        "console_scripts": [
            "loudio=main:main",
        ],
    },
    python_requires=">=3.8",
)
