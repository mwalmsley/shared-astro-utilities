
import numpy as np
import pandas as pd
from astropy import table
from astropy.coordinates import SkyCoord
from astropy import units as u


def match_galaxies_to_catalog_table(galaxies, catalog, matching_radius=10 * u.arcsec,
                              galaxy_suffix='_subject', catalog_suffix=''):

    galaxies_coord = SkyCoord(ra=galaxies['ra'], dec=galaxies['dec'], unit=u.deg)
    catalog_coord = SkyCoord(ra=catalog['ra'], dec=catalog['dec'], unit=u.deg)

    catalog['best_match'] = np.arange(len(catalog))
    best_match_catalog_index, sky_separation, _ = galaxies_coord.match_to_catalog_sky(catalog_coord)
    galaxies['best_match'] = best_match_catalog_index
    galaxies['sky_separation'] = sky_separation.to(u.arcsec).value
    matched_galaxies = galaxies[galaxies['sky_separation'] < matching_radius.value]

    matched_catalog = table.join(matched_galaxies,
                                 catalog,
                                 keys='best_match',
                                 join_type='inner',
                                 table_names=['{}'.format(galaxy_suffix), '{}'.format(catalog_suffix)],
                                 uniq_col_name='{col_name}{table_name}')
    # correct names not shared
    unmatched_galaxies = galaxies[galaxies['sky_separation'] >= matching_radius.value]
    return matched_catalog, unmatched_galaxies


def match_galaxies_to_catalog_pandas(galaxies, catalog, matching_radius=10 * u.arcsec,
                              galaxy_suffix='_subject', catalog_suffix=''):

    galaxies_coord = SkyCoord(ra=galaxies['ra'].values * u.degree, dec=galaxies['dec'].values * u.degree)
    catalog_coord = SkyCoord(ra=catalog['ra'].values * u.degree, dec=catalog['dec'].values * u.degree)

    catalog['best_match'] = np.arange(len(catalog))
    best_match_catalog_index, sky_separation, _ = galaxies_coord.match_to_catalog_sky(catalog_coord)
    galaxies['best_match'] = best_match_catalog_index
    galaxies['sky_separation'] = sky_separation.to(u.arcsec).value
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
