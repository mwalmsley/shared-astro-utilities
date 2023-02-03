
import os
import logging
import json
from typing import List, Dict

from panoptes_client import Panoptes, Project, SubjectSet, Subject


def authenticate():  # inplace
    this_dir = os.path.split(__file__)[0]  # neaten
    login_loc = os.path.join(this_dir, "secret_login.json")
    with open(login_loc, 'r') as f:
        credentials = json.load(f)
    Panoptes.connect(**credentials)


def upload_subject(locations: List, project: Project, subject_set_name: str, metadata: Dict):
    subject = Subject()
    # add files
    subject.links.project = project
    for location in locations:
        if not os.path.isfile(location):
            raise FileNotFoundError('Missing subject location: {}'.format(location))
        subject.add_location(location)

    subject.metadata.update(metadata)

    subject_set_name = subject_set_name
    subject_set = get_or_create_subject_set(project.id, subject_set_name)

    subject.save()
    subject_set.add(subject)
    return subject.id


def make_subject_sets(project_id: int, names: List):
    # to avoid threading issues where I might try to make the same subject set twice, make them all at the start
    for name in names:
        return get_or_create_subject_set(project_id, name)


def get_or_create_subject_set(project_id: int, name: str):
    # copied from shared_astro_utils
    # check if subject set already exists
    try:
        return get_subject_set(project_id, name)
    except ValueError:
        logging.info(f'Didnt find subject set {name} - creating it')
        return create_subject_set(project_id, name)


def get_subject_set(project_id: int, name: str):
    # will fail if duplicate display name - don't do this (not allowed, perhaps)
    try:
        return next(SubjectSet.where(project_id=project_id, display_name=name))
    except StopIteration:
        raise ValueError(f'Project {project_id} has no subject set {name}')


def create_subject_set(project_id: int, name: str):
    subject_set = SubjectSet()
    subject_set.links.project = Project(project_id)
    subject_set.display_name = name
    subject_set.save()
    return subject_set
