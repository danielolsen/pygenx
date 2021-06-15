from setuptools import find_packages, setup

setup(
    name="pygenx",
    version="0.1.0",
    author="Daniel Olsen",
    description="A thin python wrapper around GenX",
    license="MIT License",
    url="https://github.com/danielolsen/pygenx",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    install_requires=[
        "julia~=0.5.6",
        "pyyaml~=5.4.1",
    ],
    package_data={"pygenx": ["config.yml", "Run.jl"],},
)
