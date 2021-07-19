#!/usr/bin/python3
#
# Copyright (c) 2021 SUSE LLC.  All rights reserved.
#
# This file is part of gceimgutils
#
# gceutils is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# gceutils is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gceutils. If not, see
# <http://www.gnu.org/licenses/>.
#

import logging
import os

from gceimgutils import gceutils
from gceimgutils.gceimgutilsExceptions import (
    GCEProjectCredentialsException
)

this_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.dirname(this_path) + os.sep + 'data'

logger = logging.getLogger('gceimgutils')
logger.setLevel(logging.INFO)


# --------------------------------------------------------------------
def test_find_images_by_name_find_one():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name(
        images, 'sles15sp2hpc-test-v20210131', logger
    )
    assert 1 == len(found_images)
    assert found_images[0].get('name') == 'sles15sp2hpc-test-v20210131'


# --------------------------------------------------------------------
def test_find_images_by_name_find_multiple():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name(
        images, 'nested-vm-image', logger
    )
    assert 2 == len(found_images)
    assert found_images[0].get('name') == 'nested-vm-image'
    assert found_images[1].get('name') == 'nested-vm-image'


# --------------------------------------------------------------------
def test_find_images_by_name_find_none():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name(
        images, 'foo', logger
    )
    assert 0 == len(found_images)


# --------------------------------------------------------------------
def test_find_images_by_name_fragment_find_one():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name_fragment(
        images, 'hpc', logger
    )
    assert 1 == len(found_images)
    assert found_images[0].get('name') == 'sles15sp2hpc-test-v20210131'


# --------------------------------------------------------------------
def test_find_images_by_name_fragment_find_multiple():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name_fragment(
        images, 'opensuse', logger
    )
    # The image data we read also contains dleted images and the test helper
    # does not filter
    assert 21 == len(found_images)
    for image in found_images:
        assert 'opensuse' in image.get('name')


# --------------------------------------------------------------------
def test_find_images_by_name_fragment_find_none():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name_fragment(
        images, 'foo', logger
    )
    assert 0 == len(found_images)


# --------------------------------------------------------------------
def test_find_images_by_name_regex_find_one():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name_regex_match(
        images, '.*hpc.*', logger
    )
    assert 1 == len(found_images)
    assert found_images[0].get('name') == 'sles15sp2hpc-test-v20210131'


# --------------------------------------------------------------------
def test_find_images_by_name_regex_find_multiple():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name_regex_match(
        images, 'sles', logger
    )
    assert 11 == len(found_images)


# --------------------------------------------------------------------
def test_find_images_by_name_regex_find_none():
    images = _get_test_images()
    found_images = gceutils.find_images_by_name_regex_match(
        images, 'foo', logger
    )
    assert 0 == len(found_images)


# --------------------------------------------------------------------
def test_get_credentials_no_args():
    try:
        gceutils.get_credentials()
    except GCEProjectCredentialsException as ex:
        expected_msg = 'Either project name or credentials file path must '
        expected_msg += 'be given'
        assert expected_msg == format(ex)


# --------------------------------------------------------------------
def test_get_credentials_no_credfile():
    try:
        gceutils.get_credentials(credentials_file='foo')
    except GCEProjectCredentialsException as ex:
        expected_msg = 'Provided credentials file "foo" not found'
        assert expected_msg == format(ex)


# --------------------------------------------------------------------
def test_get_credentials_no_credfile_default_loc():
    test_def_config = os.path.expanduser('~/.config/gce/foo.json')
    try:
        gceutils.get_credentials('foo')
    except GCEProjectCredentialsException as ex:
        expected_msg = '"%s" credentials not found' % test_def_config
        assert expected_msg == format(ex)


# --------------------------------------------------------------------
def test_get_credentials_format_error():
    cred_file = data_path + '/fake_credentials.json'
    try:
        gceutils.get_credentials(
            credentials_file=cred_file
        )
    except GCEProjectCredentialsException as ex:
        expected_msg = 'Could not extract credentials from "%s"' % cred_file
        assert expected_msg == format(ex)


# --------------------------------------------------------------------
# Helpers
def _get_test_images():
    """Read the stored image data and return as list"""

    return eval(open(data_path + '/image_data.txt').read())
