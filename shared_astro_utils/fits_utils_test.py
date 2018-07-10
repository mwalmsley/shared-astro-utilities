import pytest

from shared_astro_utils import fits_utils

TEST_EXAMPLES_DIR = 'shared_astro_utils/test_examples'


def test_fits_are_identical():
    fits_a_loc = '{}/example_a.fits'.format(TEST_EXAMPLES_DIR)
    fits_b_loc = '{}/example_b.fits'.format(TEST_EXAMPLES_DIR)
    assert fits_utils.fits_are_identical(fits_a_loc, fits_a_loc)
    assert not fits_utils.fits_are_identical(fits_a_loc, fits_b_loc)
