from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="apisix-python-client",
    version="0.1.0",
    author="amine bouhaik",
    author_email="aminebouhaik527@gmail.com",
    description="A Python client library for Apache APISIX Admin and Control APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/S1nju/apisix-python-client",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
