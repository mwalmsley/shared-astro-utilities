import pytest

import pandas as pd

from shared_astro_utils import upload_utils

TEST_EXAMPLES_DIR = 'python/test_examples'


@pytest.fixture()
def joint_catalog():
    return pd.DataFrame(data=[
        {
            'nsa_id': 'example_nsa_id',
            'iauname': 'example_iauname',
            'ra': 147.45674,
            'dec': 1.09255,
            'petroth50': 50.,
            'petrotheta': 4.,
            'nsa_version': '1_0_0',
            'z': 0.1,
            'png_loc': 'jpeg_here.png',
            'fits_loc': 'fits_there.fits'
        }
    ])


def test_create_manifest_from_joint_catalog(joint_catalog):
    new_manifest = upload_utils.create_manifest_from_catalog(joint_catalog)
    assert len(new_manifest) == len(joint_catalog)
    entry = new_manifest[0]
    assert entry['png_loc'] == 'jpeg_here.png'
    assert type(entry['key_data']) == dict
    assert entry['key_data']['!ra'] == 147.45674
    assert type(entry['key_data']['!sdss_search'] == str)
    assert type(entry['key_data']['!decals_search'] == str)
    assert type(entry['key_data']['!simbad_search'] == str)
    assert type(entry['key_data']['!nasa_ned_search'] == str)


def test_coords_to_decals_skyviewer(joint_catalog):
    galaxy = joint_catalog.iloc[0]
    url = upload_utils.coords_to_decals_skyviewer(galaxy['ra'], galaxy['dec'])
    print(url)
    # TODO I don't know how to programmatically test that this query works, beyond not falling over


def test_coords_to_sdss_navigate(joint_catalog):
    galaxy = joint_catalog.iloc[0]
    url = upload_utils.coords_to_sdss_navigate(galaxy['ra'], galaxy['dec'])
    print(url)
    # TODO I don't know how to programmatically test that this query works, beyond not falling over


def test_coords_to_simbad(joint_catalog):
    galaxy = joint_catalog.iloc[0]
    url = upload_utils.coords_to_simbad(galaxy['ra'], galaxy['dec'], search_radius=10.)
    print(url)
    # TODO I don't know how to programmatically test that this query works, beyond not falling over


def test_coords_to_ned(joint_catalog):
    galaxy = joint_catalog.iloc[0]
    url = upload_utils.coords_to_ned(galaxy['ra'], galaxy['dec'], search_radius=10.)
    print(url)
    # TODO I don't know how to programmatically test that this query works, beyond not falling over


def test_coords_to_vizier(joint_catalog):
    galaxy = joint_catalog.iloc[0]
    url = upload_utils.coords_to_vizier(galaxy['ra'], galaxy['dec'], search_radius=10.)
    print(url)
    # TODO I don't know how to programmatically test that this query works, beyond not falling over


def test_coords_to_panstarrs(joint_catalog):
    galaxy = joint_catalog.iloc[0]
    url = upload_utils.coords_to_panstarrs(galaxy['ra'], galaxy['dec'])
    print(url)
    # TODO I don't know how to programmatically test that this query works, beyond not falling over


def test_replace_bytes_with_str():

    byt = b'J094552.53-000534.1'
    assert type(byt) == bytes
    assert type(byt) != str
    string = upload_utils.replace_bytes_with_str(byt)
    assert type(string) == str
    print(string)

    not_byt = 'hello world'
    string = upload_utils.replace_bytes_with_str(not_byt)
    assert type(string) == str
