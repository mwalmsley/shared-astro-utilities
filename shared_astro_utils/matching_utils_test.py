import pytest

from astropy import units
from astropy.table import Table

from shared_astro_utils import matching_utils


@pytest.fixture()
def galaxies():
    print(__name__)
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


def test_match_galaxies_to_catalog_table_right_join(galaxies, catalog):

    matched, unmatched = matching_utils.match_galaxies_to_catalog_table(galaxies, catalog, join_type='right')

    assert set(matched['name']) == {'a', 'c'}  # should include both (right) catalog galaxies, but not the unmatched (left) galaxy
    assert unmatched['name'] == ['b']

    assert set(matched.colnames) == {'dec_subject',  'galaxy_data', 'name_subject', 'ra_subject', 'z_subject', 'best_match', 'sky_separation', 'dec', 'name', 'ra', 'table_data', 'z'}
    assert set(unmatched.colnames) == {'dec', 'name', 'ra', 'z', 'best_match', 'sky_separation', 'galaxy_data'}


def test_match_galaxies_to_catalog_table_awkward_units(galaxies, catalog):
    galaxies['ra'] = galaxies['ra'] * units.deg
    catalog['dec'] = catalog['dec'] * units.deg

    matched, unmatched = matching_utils.match_galaxies_to_catalog_table(galaxies, catalog)

    assert matched['name'] == ['a']
    assert unmatched['name'] == ['b']

    assert set(matched.colnames) == {'dec_subject',  'galaxy_data', 'name_subject', 'ra_subject', 'z_subject', 'best_match', 'sky_separation', 'dec', 'name', 'ra', 'table_data', 'z'}
    assert set(unmatched.colnames) == {'dec', 'name', 'ra', 'z', 'best_match', 'sky_separation', 'galaxy_data'}
