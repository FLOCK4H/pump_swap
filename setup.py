from setuptools import setup, find_packages

setup(
    name="pump_swap",
    version="0.7.0",
    description="A Python module for interacting with Solana's Pump.fun tokens",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Flock4h",
    author_email="flock4h@gmail.com",  # Replace with your email
    url="https://github.com/FLOCK4H/pump_swap",
    packages=find_packages(),
    install_requires=[
        "solders>=0.21.0",
        "solana>=0.35.1",
        "borsh-construct",
        "aiohttp",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)