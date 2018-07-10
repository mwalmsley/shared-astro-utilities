
import numpy as np
import pandas as pd
from astropy import table
from astropy.coordinates import SkyCoord
from astropy import units


def match_galaxies_to_catalog_table(
    galaxies, 
    catalog, 
    matching_radius=10 * units.arcsec,
    join_type='inner',
    galaxy_suffix='_subject', 
    catalog_suffix=''):

    galaxies_coord = SkyCoord(ra=galaxies['ra'], dec=galaxies['dec'], unit=units.deg)
    catalog_coord = SkyCoord(ra=catalog['ra'], dec=catalog['dec'], unit=units.deg)

    catalog['best_match'] = np.arange(len(catalog))
    best_match_catalog_index, sky_separation, _ = galaxies_coord.match_to_catalog_sky(catalog_coord)
    galaxies['best_match'] = best_match_catalog_index
    galaxies['sky_separation'] = sky_separation.to(units.arcsec).value
    matched_galaxies = galaxies[galaxies['sky_separation'] < matching_radius.value]

    matched_catalog = table.join(matched_galaxies,
                                 catalog,
                                 keys='best_match',
                                 join_type=join_type,
                                 table_names=['{}'.format(galaxy_suffix), '{}'.format(catalog_suffix)],
                                 uniq_col_name='{col_name}{table_name}')
    # correct names not shared
    unmatched_galaxies = galaxies[galaxies['sky_separation'] >= matching_radius.value]
    return matched_catalog, unmatched_galaxies


def match_galaxies_to_catalog_pandas(galaxies, catalog, matching_radius=10 * units.arcsec,
                              galaxy_suffix='_subject', catalog_suffix=''):

    galaxies_coord = SkyCoord(ra=galaxies['ra'].values * units.degree, dec=galaxies['dec'].values * units.degree)
    catalog_coord = SkyCoord(ra=catalog['ra'].values * units.degree, dec=catalog['dec'].values * units.degree)

    catalog['best_match'] = np.arange(len(catalog))
    best_match_catalog_index, sky_separation, _ = galaxies_coord.match_to_catalog_sky(catalog_coord)
    galaxies['best_match'] = best_match_catalog_index
    galaxies['sky_separation'] = sky_separation.to(units.arcsec).value
    matched_galaxies = galaxies[galaxies['sky_separation'] < matching_radius.value]

    matched_catalog = pd.merge(
        matched_galaxies,
        catalog,
        on='best_match',
        how='inner',
        suffixes=['{}'.format(galaxy_suffix), '{}'.format(catalog_suffix)]
    )
    # correct names not shared
    unmatched_galaxies = galaxies[galaxies['sky_separation'] >= matching_radius.value]
    return matched_catalog, unmatched_galaxies
