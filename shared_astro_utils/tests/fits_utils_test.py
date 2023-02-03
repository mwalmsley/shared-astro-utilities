import pytest

from shared_astro_utils import fits_utils
from shared_astro_utils.tests import TEST_EXAMPLE_DIR


def test_fits_are_identical():
    fits_a_loc = '{}/example_a.fits'.format(TEST_EXAMPLE_DIR)
    fits_b_loc = '{}/example_b.fits'.format(TEST_EXAMPLE_DIR)
    assert fits_utils.fits_are_identical(fits_a_loc, fits_a_loc)
    assert not fits_utils.fits_are_identical(fits_a_loc, fits_b_loc)
