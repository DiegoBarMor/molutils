from setuptools import setup, find_packages
from pathlib import Path

__version__: str
exec(Path("molutils/_version.py").read_text())

setup(
    name="molutils",
    version=__version__,
    description="",
    keywords="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DiegoBarMor",
    author_email="diegobarmor42@gmail.com",
    url="https://github.com/diegobarmor/molutils",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    entry_points={ # comment out if package is intended to be used only via imports
        "console_scripts": [
            "molutils=molutils.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
