[![Build Status](https://travis-ci.org/RustyPanda/shared-astro-utilities.svg?branch=master)](https://travis-ci.org/RustyPanda/shared-astro-utilities)
[![Maintainability](https://api.codeclimate.com/v1/badges/e822f36412a4cbb5badc/maintainability)](https://codeclimate.com/github/RustyPanda/shared-astro-utilities/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e822f36412a4cbb5badc/test_coverage)](https://codeclimate.com/github/RustyPanda/shared-astro-utilities/test_coverage)

# shared-astro-utilities
Convience functions for astrophysics/zooniverse. Intended for personal use by Mike Walmsley, but public. Contributions welcome.




### Installation

This is packaged with [PyPI](https://test.pypi.org/project/shared-astro-utils) here, but only available from the **test** server.


1. From the target environment, run `pip install -i https://test.pypi.org/simple/ shared-astro-utils` to install the package. If already installed, add the argument `--upgrade`.
2. Import as `import shared_astro_utils` or e.g. `from shared_astro_utils import matching_utils`.

### Features

- astropy_utils to save a Table column subset or safely convert a nested Table to pandas
- fits_utils to check if two fits files are identical
- matching_utils for in-memory skymatching
- object_utils for converting a Python object to a dict
- panoptes_utils to parse a Panoptes classification export
- plotting_utils for plotting a grid of images without whitespace
- time_utils for getting the current time/data easily
- upload_utils for uploading new galaxies to Galaxy Zoo, and to convert pandas catalogs to Panoptes-suitable manifests

### Creating Distributions

The root folder `shared-astro-utilities` is the usual repo folder, and should contain a `setup.py`, `requirements.txt`, `README.MD`, `LICENSE`, and the usual CI configurations. This is the location for unit tests to run from. 

The package itself is in `shared_astro_utils`. 

The package is renamed by PyPI to `shared-astro-utils` by convention, but imported according to the folder name `shared_astro_utils`.

Building is done following [these](https://packaging.python.org/tutorials/packaging-projects/) instructions.

1. Ensure setuptools and twine are installed
2. Delete any leftover `/build` or `/dist` folders.
3. Increment the setup.py version number. Files may not be duplicated/overwritten, so this is required.
4. Run `python setup.py sdist bdist_wheel` to create the package, wrapped as `/build` and `/dist` folders.
5. Run `twine upload --repository-url https://test.pypi.org/legacy/ dist/* --skip-existing` to upload the package to the PyPI **test** server.

My own username is mikewalmsley.
