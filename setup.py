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
    package_data={
        "molutils": [
            "_ui/fy_rules.fyr", "_ui/fy_help.fyh",
        ],
    },
    install_requires=["freyacli==0.2.0"],
    entry_points={
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
