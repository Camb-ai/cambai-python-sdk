from setuptools import setup, find_packages

setup(
    name="cambai-sdk",
    version="1.5.0",
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
