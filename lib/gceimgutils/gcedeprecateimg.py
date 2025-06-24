# Copyright 2025 SUSE LLC
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
# along with gcedeprecateimg. If not, see <http://www.gnu.org/licenses/>.

import datetime
import logging

from gceimgutils.gceutils import wait_on_operation, get_image, compute_v1
from gceimgutils.gceimgutils import GCEImageUtils
from gceimgutils.gceimgutilsExceptions import GCEDeprecateImgException

from dateutil.relativedelta import relativedelta


class GCEDeprecateImage(GCEImageUtils):
    """Class to deprecate images from GCE project"""

    # ---------------------------------------------------------------------
    def __init__(
        self,
        image_name,
        project,
        replacement_image_name=None,
        months_to_deletion=6,
        credentials_path=None,
        credentials_info=None,
        state='DEPRECATED',
        log_callback=None,
        log_level=logging.INFO
    ):
        GCEImageUtils.__init__(
            self,
            project,
            credentials_path,
            credentials_info,
            log_level,
            log_callback
        )

        self.image_name = image_name
        self.replacement_image_name = replacement_image_name
        self.months_to_deletion = months_to_deletion
        self.state = state

    # ---------------------------------------------------------------------
    def deprecate_image(self):
        """Deprecate the image"""
        kwargs = {
            'state': self.state
        }

        if self.state == 'DEPRECATED':
            delete_on = datetime.date.today() + relativedelta(
                months=int(self.months_to_deletion)
            )
            delete_timestamp = ''.join([
                delete_on.isoformat(),
                'T00:00:00.000-00:00'
            ])
            kwargs['deleted'] = delete_timestamp

        if self.state == 'DEPRECATED' and self.replacement_image_name:
            replacement = get_image(
                self.images_client,
                self.project,
                self.replacement_image_name
            )
            kwargs['replacement'] = replacement.self_link

        deprecation_status = compute_v1.DeprecationStatus(**kwargs)

        try:
            operation = self.images_client.deprecate(
                project=self.project,
                image=self.image_name,
                deprecation_status_resource=deprecation_status
            )
        except Exception as error:
            msg = (
                f'Unable to deprecate image: "{self.image_name}". '
                f'{str(error)}'
            )
            self.log.error(msg)
            raise GCEDeprecateImgException(msg) from error

        wait_on_operation(operation, self.log, 'image deprecation')
