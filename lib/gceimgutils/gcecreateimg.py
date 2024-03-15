# Copyright 2024 SUSE LLC
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
# along with gceremoveimg. If not, see <http://www.gnu.org/licenses/>.

import logging

import gceimgutils.gceutils as utils

from gceimgutils.gceimgutils import GCEImageUtils
from gceimgutils.gceimgutilsExceptions import GCECreateImgException

from google.cloud import compute_v1


class GCECreateImage(GCEImageUtils):
    """Class to create images from GCE project"""

    # ---------------------------------------------------------------------
    def __init__(
        self,
        image_name,
        image_description,
        family,
        bucket_name,
        object_name,
        architecture='x86_64',
        guest_os_features=None,
        credentials_path=None,
        project=None,
        skip_rollout=False,
        log_callback=None,
        log_level=logging.INFO,
    ):
        GCEImageUtils.__init__(
            self, project, credentials_path,
            log_level, log_callback
        )

        self.image_name = image_name
        self.image_description = image_description
        self.family = family
        self.blob_uri = ''.join([
            'https://www.googleapis.com/storage/v1/b/',
            bucket_name,
            '/o/',
            object_name
        ])
        self.architecture = architecture
        self.guest_os_features = guest_os_features
        self.skip_rollout = skip_rollout

    # ---------------------------------------------------------------------
    def create_image(self):
        """Create the image"""
        mapping = {
            'name': self.image_name,
            'family': self.family,
            'description': self.image_description,
            'raw_disk': {'source': self.blob_uri},
            'architecture': self.architecture.upper()
        }

        if self.guest_os_features:
            mapping['guest_os_features'] = [
                {'type_': feature} for feature in self.guest_os_features
            ]

        if not self.skip_rollout:
            zones_client = compute_v1.ZonesClient(credentials=self.credentials)
            mapping['rollout_override'] = utils.create_gce_rollout(
                zones_client,
                self.project
            )

        image = compute_v1.Image(mapping)

        try:
            operation = self.compute_driver.insert(
                project=self.project,
                image_resource=image
            )
        except Exception as error:
            msg = f'Unable to create image: "{self.image_name}". {str(error)}'
            self.log.error(msg)
            raise GCECreateImgException(msg) from error

        utils.wait_on_operation(operation, self.log, 'image creation')
        return self.compute_driver.get(
            project=self.project,
            image=self.image_name
        )