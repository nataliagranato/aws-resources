from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aws-resources-cli",
    version="0.2.0",
    author="Natália Granato",
    author_email="",
    description="A command-line tool and web UI for managing AWS resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nataliagranato/aws-resources",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements + ['Flask>=2.0', 'rich>=10.0.0'],
    entry_points={
        "console_scripts": [
            "aws-resources=aws_cli.main:main",
            "aws-resources-web=aws_ui.app:main",
        ],
    },
)