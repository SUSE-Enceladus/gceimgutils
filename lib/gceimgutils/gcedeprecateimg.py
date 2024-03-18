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

import datetime
import logging

import gceimgutils.gceutils as utils

from gceimgutils.gceimgutils import GCEImageUtils
from gceimgutils.gceimgutilsExceptions import GCEDeprecateImgException

from google.cloud import compute_v1

from dateutil.relativedelta import relativedelta


class GCEDeprecateImage(GCEImageUtils):
    """Class to deprecate images in GCE project"""

    # ---------------------------------------------------------------------
    def __init__(
        self,
        image_name,
        replacement_image_name,
        months_to_deletion=6,
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
        self.replacement_image_name = replacement_image_name
        self.months_to_deletion = months_to_deletion

    # ---------------------------------------------------------------------
    def deprecate_image(self):
        """Deprecate the image"""
        delete_on = datetime.date.today() + relativedelta(
            months=int(self.months_to_deletion)
        )
        delete_timestamp = ''.join([
            delete_on.isoformat(),
            'T00:00:00.000-00:00'
        ])

        replacement_image = self.compute_driver.get(
            project=self.project,
            image=self.replacement_image_name
        )

        mapping = {
            'replacement': replacement_image.self_link,
            'deleted': delete_timestamp,
            'state': 'DEPRECATED',
        }

        deprecation_resource = compute_v1.DeprecationStatus(mapping)

        try:
            operation = self.compute_driver.deprecate(
                project=self.project,
                image=self.image_name,
                deprecation_status_resource=deprecation_resource
            )
        except Exception as error:
            msg = (
                'Unable to deprecate image: '
                f'"{self.image_name}". {str(error)}'
            )
            self.log.error(msg)
            raise GCEDeprecateImgException(msg) from error

        utils.wait_on_operation(operation, self.log, 'image deprecation')
