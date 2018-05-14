import pytest

from astropy import units as u
from astropy.table import Table

import matching_utils


@pytest.fixture()
def galaxies():
    return Table([
        {
            'name': 'a',
            'ra': 10.,
            'dec': 10.,
            'z': 0.05,
            'galaxy_data': 14.
        },

        {
            'name': 'b',
            'ra': 20.,
            'dec': 10.,
            'z': 0.05,
            'galaxy_data': 14.
        }
    ])


@pytest.fixture()
def catalog():
    return Table([
        {
            'name': 'a',
            'ra': 10.,
            'dec': 10.,
            'z': 0.05,
            'table_data': 12.
        },

        {
            'name': 'c',
            'ra': 100.,
            'dec': 80.,
            'z': 0.05,
            'table_data': 12.
        },
    ])


def test_match_galaxies_to_catalog_table(galaxies, catalog):

    matched, unmatched = matching_utils.match_galaxies_to_catalog_table(galaxies, catalog)

    assert matched['name'] == ['a']
    assert unmatched['name'] == ['b']

    assert set(matched.colnames) == {'dec_subject',  'galaxy_data', 'name_subject', 'ra_subject', 'z_subject', 'best_match', 'sky_separation', 'dec', 'name', 'ra', 'table_data', 'z'}
    assert set(unmatched.colnames) == {'dec', 'name', 'ra', 'z', 'best_match', 'sky_separation', 'galaxy_data'}


def test_match_galaxies_to_catalog_table_awkward_units(galaxies, catalog):
    galaxies['ra'] = galaxies['ra'] * u.deg
    catalog['dec'] = catalog['dec'] * u.deg

    matched, unmatched = matching_utils.match_galaxies_to_catalog_table(galaxies, catalog)

    assert matched['name'] == ['a']
    assert unmatched['name'] == ['b']

    assert set(matched.colnames) == {'dec_subject',  'galaxy_data', 'name_subject', 'ra_subject', 'z_subject', 'best_match', 'sky_separation', 'dec', 'name', 'ra', 'table_data', 'z'}
    assert set(unmatched.colnames) == {'dec', 'name', 'ra', 'z', 'best_match', 'sky_separation', 'galaxy_data'}