# Copyright 2021 SUSE LLC
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
# along with gcelistimg. If not, see <http://www.gnu.org/licenses/>.

import logging
import json

import gceimgutils.gceutils as utils

from gceimgutils.gceimgutils import GCEImageUtils
from gceimgutils.gceimgutilsExceptions import GCEListImgException


class GCEListImage(GCEImageUtils):
    """Class to list images from GCE project"""

    # ---------------------------------------------------------------------
    def __init__(
            self,
            credentials_path=None,
            credentials_info=None,
            image_name=None,
            image_name_fragment=None,
            image_name_match=None,
            log_callback=None,
            log_level=logging.INFO,
            project=None,
            detail=False
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
        self.image_name_fragment = image_name_fragment
        self.image_name_match = image_name_match
        self.detail = detail

    # ---------------------------------------------------------------------
    def get_images(self):
        """Get images from sdk"""
        owned_images = utils.get_project_images(
            self.images_client,
            self.project,
            True
        )

        if self.image_name:
            return utils.find_images_by_name(
                owned_images,
                self.image_name,
                self.log
            )
        elif self.image_name_fragment:
            return utils.find_images_by_name_fragment(
                owned_images,
                self.image_name_fragment,
                self.log
            )
        elif self.image_name_match:
            try:
                return utils.find_images_by_name_regex_match(
                    owned_images,
                    self.image_name_match,
                    self.log
                )
            except Exception:
                msg = 'Unable to complie regular expression "%s"'
                msg = msg % self.image_name_match
                raise GCEListImgException(msg)
        else:
            return owned_images

    # ---------------------------------------------------------------------
    def list_images(self):
        """List the images"""
        images = self.get_images()

        if not images:
            raise GCEListImgException('No Images found')

        for image in images:
            if self.detail or self.image_name:
                self.log.info(json.dumps(utils.image_to_dict(image), indent=4))
            else:
                self.log.info(image.name)
