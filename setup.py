from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pdf2html-converter",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Convert PDF to HTML with support for scanned and text-based PDFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pdf2html-converter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pdfplumber>=0.10.0",
        "pymupdf>=1.23.0",
        "pillow>=10.0.0",
        "playwright>=1.40.0",
    ],
    entry_points={
        "console_scripts": [
            "wenpdf=convert:main",
        ],
    },
)