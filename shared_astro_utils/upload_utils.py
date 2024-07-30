import logging
import os
import functools
import ast
from datetime import datetime

import numpy as np
import pandas as pd
from tqdm import tqdm
from panoptes_client import Panoptes, Project, SubjectSet, Subject

from shared_astro_utils import time_utils, subject_utils

UPLOAD_COLS = ['iauname', 'nsa_id', 'ra', 'dec', 'petrotheta',
                   'petroth50', 'petroth90', 'redshift', 'nsa_version', 'file_loc']

def upload_to_gz(
        login_loc: str,
        selected_catalog: pd.DataFrame,
        name: str,
        retirement: int,
        project_id='5733',
        uploader='gz_upload_util'):
    """Simple wrapper to upload selected galaxies to GZ

    Args:
        login_loc (str): path to json file of form {"username": ..., "password": ...}
        selected_catalog (pd.DataFrame): catalog of galaxies to be uploaded
        name (str): name of subject set to be created or appended
        retirement (int): sets retirement_limit metadata field, used by Caesar to retire after this many classifications
        project_id (str, optional): Which project to upload to. Defaults to '5733'. 6490 for GZ Mobile.
        uploader (str, optional): Sets uploader metadata field, to name the uploader used (for posterity only). Defaults to 'gz_upload_util'.
    """
    # restrict to key columns
    upload_cols = UPLOAD_COLS
    upload_catalog = selected_catalog[upload_cols]
    upload_catalog['#retirement_limit'] = retirement
    upload_catalog['#uploader'] = uploader

    logging.info(f'Uploading {len(selected_catalog)} subjects to {name}')
    manifest = create_manifest_from_catalog(upload_catalog)
    bulk_upload_subjects(
        subject_set_name=name,
        manifest=manifest,
        project_id=project_id,
        login_loc=login_loc)
    logging.info('Upload complete')


def create_manifest_from_catalog(catalog):
    """
    Create dict of files and metadata.
    All columns will be uploaded and visible!

    Catalog including 'png_loc' and key astro data, one galaxy per row
    Catalog can only contain scalars.
    Required cols:
        ['ra', 'dec']
    Suggested cols:
        ['redshift', 'iauname', 'nsa_version', 'nsa_id']

    Args:
        catalog (astropy.Table): NSA joint catalog to upload

    Returns:
        (dict) of form {png_loc: img.png, metadata: {metadata_col: metadata_value}}
    """
    metadata_df = catalog.copy()  # assume already filtered - all cols will be included!

    # np.nan cannot be handled by JSON encoder. Convert to flag value of -999
    metadata_df = metadata_df.applymap(replace_nan_with_flag)
    # bytes cannot be handled by JSON encoder. Convert to string
    metadata_df = metadata_df.applymap(replace_bytes_with_str)

    metadata_df['decals_search'] = metadata_df.apply(
        lambda galaxy: coords_to_decals_skyviewer(galaxy['ra'], galaxy['dec']),
        axis=1)
    metadata_df['sdss_search'] = metadata_df.apply(
        lambda galaxy: coords_to_sdss_navigate(galaxy['ra'], galaxy['dec']),
        axis=1)
    metadata_df['panstarrs_dr1_search'] = metadata_df.apply(
        lambda galaxy: coords_to_panstarrs(galaxy['ra'], galaxy['dec']),
        axis=1)
    metadata_df['simbad_search'] = metadata_df.apply(
        lambda galaxy: coords_to_simbad(galaxy['ra'], galaxy['dec'], search_radius=10.),
        axis=1)
    metadata_df['nasa_ned_search'] = metadata_df.apply(
        lambda galaxy: coords_to_ned(galaxy['ra'], galaxy['dec'], search_radius=10.),
        axis=1)
    metadata_df['vizier_search'] = metadata_df.apply(
        lambda galaxy: coords_to_vizier(galaxy['ra'], galaxy['dec'], search_radius=10.),
        axis=1)

    markdown_text = {
        'decals_search': 'Click to view in DECALS',
        'sdss_search': 'Click to view in SDSS',
        'panstarrs_dr1_search': 'Click to view in PANSTARRS DR1',
        'simbad_search': 'Click to search SIMBAD',
        'nasa_ned_search': 'Click to search NASA NED',
        'vizier_search': 'Click to search VizieR'
    }
    for link_column, link_text in markdown_text.items():
        metadata_df[link_column] = metadata_df[link_column].apply(
            lambda url: wrap_url_in_new_tab_markdown(url=url, display_text=link_text))

    # rename all columns to appear only in Talk by prepending with '!'
    current_columns = set(metadata_df.columns.values) - {'#retirement_limit', '#uploader'}
    prepended_columns = ['!' + col for col in current_columns]
    metadata_df = metadata_df.rename(columns=dict(zip(current_columns, prepended_columns)))

    metadata_df['metadata_df_message'] = 'You can access this galaxy\'s metadata if you chose to discuss it with other volunteers by pressing "Done and Talk" at the end of your classification.'
    metadata_df['#upload_date'] = time_utils.current_date()  # not shown to users

    metadata_df['!filename'] = metadata_df['file_loc'].apply(os.path.basename)
    

    # create the manifest structure that Panoptes Python client expects
    metadata = metadata_df.to_dict(orient='records')

    return metadata


def bulk_upload_subjects(
    subject_set_name, 
    manifest, 
    project_id='5733'  # default to main GZ project
    # login_loc='zooniverse_login.txt'
    ):
    """
    Save manifest (set of galaxies with metadata prepared) to Galaxy Zoo

    Args:
        subject_set_name (str): name for subject set
        manifest (list): containing dicts of form {locations: [img.jpg], metadata: {metadata_col: metadata_value, ...}}
        project_id (str): panoptes project id e.g. '5733' for Galaxy Zoo, '6490' for mobile
        n_processes (int): number of processes with which to upload galaxies in parallel

    Returns:
        None
    """
    # assert os.path.exists(login_loc)
    if 'TEST' in subject_set_name:
        logging.warning('Testing mode detected - not uploading!')
        return manifest

    if project_id == '5733':
        logging.info('Uploading to Galaxy Zoo project 5733')
    elif project_id == '6490':
        logging.info('Uploading to mobile app project 6490')
    elif project_id == '8751':
        logging.info('Uploading to staging project 8751')
    else:
        logging.info('Uploading to unknown project {}'.format(project_id))

    subject_utils.authenticate()



    project = Project.find(project_id)

    # check if subject set already exists
    # subject_set = None
    # subject_sets = SubjectSet.where(project_id=project_id)
    # for candidate_subject_set in subject_sets:
    #     if candidate_subject_set.raw['display_name'] == subject_set_name:
    #         # use if it already exists
    #         subject_set = candidate_subject_set
    # if not subject_set:  # make a new one if not
    #     subject_set = SubjectSet()
    #     subject_set.links.project = project
    #     subject_set.display_name = subject_set_name
    #     subject_set.save()

    subject_set = subject_utils.get_or_create_subject_set(project_id, subject_set_name)

    pbar = tqdm(total=len(manifest), unit=' subjects uploaded')

    # save_subject_params = {
    #     'project': project,
    #     'pbar': pbar
    # }
    # save_subject_partial = functools.partial(save_subject, **save_subject_params)

    # upload in async blocks, to avoid huge join at end
    manifest_block_start = 0
    manifest_block_size = 100

    while True:
        manifest_block = manifest[manifest_block_start: manifest_block_start + manifest_block_size]
        

        new_subjects = []
        with Subject.async_saves():
            for manifest_entry in manifest_block:
                new_subjects.append(
                    save_subject(
                        locations=manifest_entry['locations'], 
                        metadata=manifest_entry['metadata'],
                        project=project,
                        pbar=pbar
                    )
                )

        subject_set.add(new_subjects)
        logging.info('{} subjects linked'.format(new_subjects))

        manifest_block_start += manifest_block_size
        if manifest_block_start > len(manifest):
            break

    return manifest  # for debugging only


def save_subject(locations, project, metadata, pbar=None):
    """
    Add manifest item to project. Note: follow with subject_set.add(subject) to associate with subject set.
    Args:
        locations (list): ['img.jpg'] list of file locations to upload
        project (str): project to upload subject too e.g. '5773' for Galaxy Zoo
        metadata (dict): metadata to attach to subject
        pbar (tqdm.tqdm): progress bar to update. If None, no bar will display.

    Returns:
        None
    """
    subject = Subject()

    subject.links.project = project
    for location in locations:
        if not os.path.isfile(location):
            raise FileNotFoundError('Missing subject location: {}'.format(location))
        subject.add_location(location)
    assert '!filename' in metadata.keys(), 'Metadata must contain !filename for BAJOR'
    subject.metadata.update(metadata)

    subject.save()

    if pbar:
        pbar.update()

    return subject


def replace_nan_with_flag(x):
    """
    For any x, if x is nan or masked, replace with -999
    Args:
        x (Any): input of unknown type to be checked

    Returns:
        (float): -999 if x is of nan or masked, x if not
    """
    try:
        if np.isnan(x) or np.isinf(x):
            return -999.
        else:
            return x
    except TypeError:  # not a numpy-supported data type e.g. string, therefore can't be nan
        return x


def replace_bytes_with_str(x):
    """
    For any x, if x is nan or masked, replace with -999
    Args:
        x (Any): input of unknown type to be checked

    Returns:
        (float): -999 if x is of nan or masked, x if not
    """
    if type(x) is bytes:
        return x.decode('utf-8')
    else:
        return x


def coords_to_simbad(ra, dec, search_radius):
    """
    Get SIMBAD search url for objects within search_radius of ra, dec coordinates.
    Args:
        ra (float): right ascension in degrees
        dec (float): declination in degrees
        search_radius (float): search radius around ra, dec in arcseconds

    Returns:
        (str): SIMBAD database search url for objects at ra, dec
    """
    return 'http://simbad.u-strasbg.fr/simbad/sim-coo?Coord={0}+%09{1}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius={2}&Radius.unit=arcmin&submit=submit+query&CoordList='.format(ra, dec, search_radius)


def coords_to_decals_skyviewer(ra, dec):
    """
    Get decals_skyviewer viewpoint url for objects within search_radius of ra, dec coordinates. Default zoom.
    Args:
        ra (float): right ascension in degrees
        dec (float): declination in degrees

    Returns:
        (str): decals_skyviewer viewpoint url for objects at ra, dec
    """
    return 'http://www.legacysurvey.org/viewer?ra={}&dec={}&zoom=15&layer=decals-dr5'.format(ra, dec)


def coords_to_sdss_navigate(ra, dec):
    """
    Get sdss navigate url for objects within search_radius of ra, dec coordinates. Default zoom.
    Args:
        ra (float): right ascension in degrees
        dec (float): declination in degrees

    Returns:
        (str): sdss navigate url for objects at ra, dec
    """
    # skyserver.sdss.org really does skip the wwww, but needs http or link keeps the original Zooniverse root
    return 'http://skyserver.sdss.org/dr14/en/tools/chart/navi.aspx?ra={}&dec={}&scale=0.1&width=120&height=120&opt='.format(ra, dec)


def coords_to_ned(ra, dec, search_radius):
    """
    Get NASA NED search url for objects within search_radius of ra, dec coordinates.
    Args:
        ra (float): right ascension in degrees
        dec (float): declination in degrees
        search_radius (float): search radius around ra, dec in arcseconds

    Returns:
        (str): SIMBAD database search url for objects at ra, dec
    """
    ra_string = '{:3.8f}d'.format(ra)
    dec_string = '{:3.8f}d'.format(dec)
    search_radius_arcmin = search_radius / 60.
    return 'https://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&in_csys=Equatorial&in_equinox=J2000.0&lon={}&lat={}&radius={}&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&nmp_op=ANY&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES'.format(ra_string, dec_string, search_radius_arcmin)


def coords_to_vizier(ra, dec, search_radius):
    """
    Get vizier search url for objects within search_radius of ra, dec coordinates.
    Include radius from search target, sort by radius from search target.
    http://vizier.u-strasbg.fr/doc/asu-summary.htx
    Args:
        ra (float): right ascension in degrees
        dec (float): declination in degrees
        search_radius (float): search radius around ra, dec in arcseconds

    Returns:
        (str): vizier url for objects at ra, dec
    """
    return 'http://vizier.u-strasbg.fr/viz-bin/VizieR?&-c={},{}&-c.rs={}&-out.add=_r&-sort=_r'.format(
        ra, dec, search_radius)


def coords_to_panstarrs(ra, dec):
    """
    Get panstarrs dr1 cutout url at ra, dec coordinates.
    http://ps1images.stsci.edu/cgi-bin/ps1cutouts
    Args:
        ra (float): right ascension in degrees
        dec (float): declination in degrees

    Returns:
        (str): cutout url for objects at ra, dec
    """
    return 'http://ps1images.stsci.edu/cgi-bin/ps1cutouts?pos={}{:+f}&filter=color&filter=g&filter=r&filter=i&filter=z&filter=y&filetypes=stack&auxiliary=data&size=240&output_size=0&verbose=0&autoscale=99.500000&catlist='.format(
        ra, dec)


def wrap_url_in_new_tab_markdown(url, display_text):
    return '[{}](+tab+{})'.format(display_text, url)
