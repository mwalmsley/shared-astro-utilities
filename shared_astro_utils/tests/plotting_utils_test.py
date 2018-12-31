import pytest

import os

import numpy as np

from shared_astro_utils.tests import TEST_FIGURE_DIR
from shared_astro_utils import plotting_utils


@pytest.fixture
def galaxies():
    return np.random.rand(28, 128, 128, 3) * 256.


def test_plot_galaxy_grid(galaxies):
    plotting_utils.plot_galaxy_grid(galaxies, 9, 3, os.path.join(TEST_FIGURE_DIR, 'galaxy_grid.png'))
