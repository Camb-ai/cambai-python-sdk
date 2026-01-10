from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="camb-sdk",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="1.5.3",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        "httpx>=0.21.2",
        "pydantic>=1.10.0",
        "typing_extensions>=4.0.0",
        "websockets>=11.0.3",
        "websocket-client>=1.6.0",
    ],
    package_data={"camb": ["py.typed"]},
    include_package_data=True,
    python_requires=">=3.8",
)
