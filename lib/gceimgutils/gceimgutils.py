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
import os

import gceimgutils.gceutils as utils


class GCEImageUtils():
    """Base class for GCE Image Utilities"""

    # ---------------------------------------------------------------------
    def __init__(
            self, project, credentials_path,
            log_level=logging.INFO, log_callback=None
    ):

        self.project = project
        self.credentials_path = os.path.expanduser(credentials_path)
        self._credentials = None
        self._compute_driver = None

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
    def compute_driver(self):
        """Get an authenticated compute driver"""
        if not self._compute_driver:
            self._compute_driver = utils.get_compute_api(self.credentials)

        return self._compute_driver

    # ---------------------------------------------------------------------
    @property
    def credentials(self):
        if not self._credentials:
            self._credentials = utils.get_credentials(
                self.project,
                self.credentials_path
            )

        return self._credentials
