# Copyright (c) 2021 SUSE LLC
#
# This file is part of gceimgutils.
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

import gceimgutils.gceutils as utils


class GCEImageUtils():
    """Base class for GCE Image Utilities"""

    # ---------------------------------------------------------------------
    def __init__(
        self,
        project,
        credentials_path=None,
        credentials_info=None,
        log_level=logging.INFO,
        log_callback=None
    ):

        self.project = project
        self.credentials_path = credentials_path
        self.credentials_info = credentials_info
        self._credentials = None
        self._images_client = None
        self._regions_client = None
        self._zones_client = None
        self._storage_client = None

        if log_callback:
            self.log = log_callback
        else:
            logger = logging.getLogger('gceimgutils')
            logger.setLevel(log_level)
            self.log = logger

        try:
            self.log_level = self.log.level
        except AttributeError:
            self.log_level = self.log.logger.level  # LoggerAdapter

    # ---------------------------------------------------------------------
    @property
    def images_client(self):
        """Get an authenticated images client"""
        if not self._images_client:
            self._images_client = utils.get_images_client(
                self.credentials
            )

        return self._images_client

    # ---------------------------------------------------------------------
    @property
    def regions_client(self):
        """Get an authenticated regions client"""
        if not self._regions_client:
            self._regions_client = utils.get_regions_client(
                self.credentials
            )

        return self._regions_client

    # ---------------------------------------------------------------------
    @property
    def zones_client(self):
        """Get an authenticated zones client"""
        if not self._regions_client:
            self._zones_client = utils.get_zones_client(
                self.credentials
            )

        return self._zones_client

    # ---------------------------------------------------------------------
    @property
    def storage_client(self):
        """Get an authenticated storage client"""
        if not self._storage_client:
            self._storage_client = utils.get_storage_client(
                self.project,
                self.credentials
            )

        return self._storage_client

    # ---------------------------------------------------------------------
    @property
    def credentials(self):
        if not self._credentials:
            self._credentials = utils.get_credentials(
                self.project,
                self.credentials_path,
                self.credentials_info
            )

        return self._credentials
