"""
Setup configuration for the SkyRun package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="skyrun",
    version="0.1.0",
    author="SkyRun Team",
    author_email="team@skyrun.ai",
    description="A decentralized AI creative platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/SkyRun",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "numpy>=1.24.0",
        "pillow>=9.5.0",
        "transformers>=4.30.0",
        "accelerate>=0.20.0",
        "safetensors>=0.3.1",
        "opencv-python>=4.7.0",
        "gradio>=3.40.0",
        "web3>=6.0.0",
        "pydantic>=2.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "black>=23.3.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "skyrun=skyrun.__main__:main",
        ],
    },
) 