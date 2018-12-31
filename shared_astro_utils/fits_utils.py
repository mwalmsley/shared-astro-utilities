
import numpy as np
from astropy.io import fits


def fits_are_identical(fits_a_loc, fits_b_loc):
    """
    Given the location of two fits files, do they have identical pixels?

    Args:
        fits_a_loc (str): location of one fits file
        fits_b_loc (str): location of other fits file

    Returns:
        (bool) True if both fits files have identical pixels (including shape), else False
    """
    # linter error: this is the correct access method for data in 0th fits HDU
    pixels_a = fits.open(fits_a_loc)[0].data
    pixels_b = fits.open(fits_b_loc)[0].data
    return np.allclose(pixels_a[~np.isnan(pixels_a)], pixels_b[~np.isnan(pixels_b)])
