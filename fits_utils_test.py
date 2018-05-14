import pytest

import os

from shared_astro_utilities import fits_utils

# path relative to this file, regardless of working directory
CURRENT_DIR = os.path.dirname(__file__)
TEST_EXAMPLES_DIR = os.path.join(CURRENT_DIR, 'test_examples')


def test_fits_are_identical():
    fits_a_loc = '{}/example_a.fits'.format(TEST_EXAMPLES_DIR)
    fits_b_loc = '{}/example_b.fits'.format(TEST_EXAMPLES_DIR)
    assert fits_utils.fits_are_identical(fits_a_loc, fits_a_loc)
    assert not fits_utils.fits_are_identical(fits_a_loc, fits_b_loc)
