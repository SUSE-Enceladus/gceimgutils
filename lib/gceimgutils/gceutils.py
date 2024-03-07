# Copyright (c) 2021 SUSE LLC
#
# This file is part of gceimgutils
#
# gceimgutils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gceimgutils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gceimgutils.ase.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import re

from google.oauth2 import service_account
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import AuthorizedSession
from google.cloud import compute_v1

from gceimgutils.gceimgutilsExceptions import (
    GCEProjectCredentialsException
)


# ----------------------------------------------------------------------------
def find_images_by_name(images, image_name, log_callback):
    """Return a list of images that match the given name."""
    matching_images = []
    for image in images:
        if not image.name:
            _no_name_warning(image, log_callback)
            continue
        if image_name == image.name:
            matching_images.append(image)

    return matching_images


# ----------------------------------------------------------------------------
def find_images_by_name_fragment(images, image_name_fragment, log_callback):
    """Return a list of images that match the given fragment in any part
       of the image name."""
    matching_images = []
    for image in images:
        if not image.name:
            _no_name_warning(image, log_callback)
            continue
        if image.name.find(image_name_fragment) != -1:
            matching_images.append(image)

    return matching_images


# ----------------------------------------------------------------------------
def find_images_by_name_regex_match(images, image_name_regex, log_callback):
    """Return a list of images that match the given regular expression in
       their name."""
    matching_images = []
    image_name_exp = re.compile(image_name_regex)
    for image in images:
        if not image.name:
            _no_name_warning(image, log_callback)
            continue
        if image_name_exp.match(image.name):
            matching_images.append(image)

    return matching_images


# ----------------------------------------------------------------------------
def get_credentials(project_name=None, credentials_file=None):
    """Get the service account credentials for the given project"""

    if not project_name and not credentials_file:
        raise GCEProjectCredentialsException(
            'Either project name or credentials file path must be given'
        )

    if credentials_file and not os.path.exists(credentials_file):
        raise GCEProjectCredentialsException(
            'Provided credentials file "%s" not found' % credentials_file
        )

    if not credentials_file:
        credentials_file = os.path.expanduser(
            '~/.config/gce/%s.json' % project_name)
        if not os.path.exists(credentials_file):
            raise GCEProjectCredentialsException(
                '"%s" credentials not found' % credentials_file
            )

    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file
        )
    except Exception as error:
        raise GCEProjectCredentialsException(
            'Could not extract credentials from "{credentials_file}": '
            '{error}'.format(credentials_file=credentials_file, error=error)
        )

    try:
        # https://developers.google.com/identity/protocols/oauth2/scopes#google-sign-in
        scoped_credentials = credentials.with_scopes(['profile'])
        authed_session = AuthorizedSession(scoped_credentials)
        authed_session.get('https://www.googleapis.com/oauth2/v2/userinfo')
    except RefreshError:
        raise GCEProjectCredentialsException(
            'The provided credentials are invalid or expired: '
            '{creds_file}'.format(creds_file=credentials_file)
        )
    except Exception as error:
        raise GCEProjectCredentialsException(
            'GCP authentication failed: {error}'.format(error=error)
        )

    return credentials


# ----------------------------------------------------------------------------
def get_logger(verbose):
    """
    Return new console logger at provided log level.
    """
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger = logging.getLogger('gceimgutils')
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter('%(message)s'))

    logger.addHandler(console_handler)
    return logger


# ----------------------------------------------------------------------------
def get_project_images(compute_driver, project_name, deprecated=False):
    """Get the images owned by the given project"""

    current_images = []
    try:
        response = compute_driver.list(
            project=project_name
        )
    except Exception:
        return current_images

    for image in response:
        if not deprecated and image.deprecated:
            continue
        current_images.append(image)

    return current_images


# ----------------------------------------------------------------------------
def get_version():
    version_file_name = 'VERSION'
    base_path = os.path.dirname(__file__)
    version = open(os.path.join(base_path, version_file_name), 'r').read()
    return version.rstrip('\n')


# ----------------------------------------------------------------------------
def get_compute_api(credentials):
    """Build the compute API"""
    return compute_v1.ImagesClient(
        credentials=credentials
    )


# ----------------------------------------------------------------------------
def _no_name_warning(image, log_callback):
    """Print a warning for images that have no name"""
    msg = 'WARNING: Found image with no name, ignoring for search results. '
    msg += 'Image ID: %s' % image['ImageId']
    log_callback.info(msg)


# ----------------------------------------------------------------------------
def image_to_dict(image):
    return {
        'kind': image.kind,
        'id': image.id,
        'creationTimestamp': image.creation_timestamp,
        'name': image.name,
        'description': image.description,
        'soureType': image.source_type,
        'rawDisk': {
            'source': image.raw_disk.source,
            'containerType': image.raw_disk.container_type
        },
        'status': image.status,
        'archiveSizeBytes': image.archive_size_bytes,
        'diskSizeGb': image.disk_size_gb,
        'licenses': [img_lic for img_lic in image.licenses],
        'family': image.family,
        'selfLink': image.self_link,
        'labelFingerprint': image.label_fingerprint,
        'guestOsFeatures': [
            {'type': feature.type_} for feature in image.guest_os_features
        ],
        'licenseCodes': [code for code in image.license_codes],
        'storageLocations': [loc for loc in image.storage_locations],
        'architecture': image.architecture
    }
