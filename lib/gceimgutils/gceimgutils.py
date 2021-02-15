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
            self, project, credentials_path,
            log_level=logging.INFO, log_callback=None
    ):

        self.project = project
        self.credentials = None

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

        try:
            self.credentials = utils.get_credentials(project, credentials_path)
        except Exception as err:
            self.log.error(format(err))

    # ---------------------------------------------------------------------
    def _get_api(self):
        """Set up the API"""

        return utils.get_compute_api(self.credentials)
