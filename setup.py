import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shared_astro_utils",
    version="0.0.5",
    author="Mike Walmsley",
    author_email="walmsleymk1@gmail.com",
    description="Shared astronomy utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rustypanda/shared-astro-utilities",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)