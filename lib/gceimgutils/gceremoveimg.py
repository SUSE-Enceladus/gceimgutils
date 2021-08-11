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
# along with gceremoveimg. If not, see <http://www.gnu.org/licenses/>.

import logging
import sys

import gceimgutils.gceutils as utils

from gceimgutils.gceimgutils import GCEImageUtils
from gceimgutils.gceimgutilsExceptions import GCERemoveImgException

from googleapiclient.errors import HttpError


class GCERemoveImage(GCEImageUtils):
    """Class to remove images from GCE project"""

    # ---------------------------------------------------------------------
    def __init__(
            self,
            confirm=False,
            credentials_path=None,
            image_name=None,
            image_name_fragment=None,
            image_name_match=None,
            log_callback=None,
            log_level=logging.INFO,
            project=None,
            remove_all=False
    ):
        GCEImageUtils.__init__(
            self, project, credentials_path,
            log_level, log_callback
        )

        self.confirm = confirm
        self.image_name = image_name
        self.image_name_fragment = image_name_fragment
        self.image_name_match = image_name_match
        self.remove_all = remove_all

    # ---------------------------------------------------------------------
    def _check_images_boundary_condition(self, images):
        """Check if the images found meet operating conditions:
           If all is true we delete all found images if not we should have
           found only one image"""

        if not images:
            self.log.info(
                'No images to remove found'
            )

        if len(images) > 1 and not self.remove_all:
            msg = 'Found multiple images to remove, but "all" is '
            msg += 'not set. Cannot disambiguate images to remove'
            self.log.info(msg)
            return False

        return True

    # ---------------------------------------------------------------------
    def _get_images_to_remove(self):
        """Find the images to remove"""
        owned_images = utils.get_project_images(
            self.project, self.credentials, True
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
                raise GCERemoveImgException(msg)
        else:
            msg = 'No remove image condition set. Should not reach '
            msg += 'this point.'
            raise GCERemoveImgException(msg)

    # ---------------------------------------------------------------------
    def print_remove_info(self):
        """Print information about images that would be deleted"""
        images = self._get_images_to_remove()
        images_ok = self._check_images_boundary_condition(images)

        if not images_ok:
            # While the boundary conditions are not met, we are just printing
            # information thus this is not considered a failure
            return True

        header_msg = 'Would remove image'
        if len(images) > 1:
            header_msg += 's'

        self.log.info(header_msg)
        for image in images:
            self.log.info('\t\t%s' % image.get('name'))

        return True

    # ---------------------------------------------------------------------
    def remove_images(self):
        """Remove the images"""
        images = self._get_images_to_remove()
        images_ok = self._check_images_boundary_condition(images)

        if not images_ok:
            raise GCERemoveImgException('Image ambiguity')

        for image in images:
            try:
                self.remove_image(image.get('name'))
            except GCERemoveImgException:
                pass  # If an image fails it is logged

    # ---------------------------------------------------------------------
    def remove_image(self, image_name):
        """Remove the image"""
        delete = True
        if self.confirm:
            delete = self._query_yes_no(image_name)

        if delete:
            try:
                self._get_api().images().delete(
                    project=self.project, image=image_name
                ).execute()
            except HttpError as error:
                msg = 'Unable to remove image: "{image}". {error}'.format(
                    image=image_name,
                    error=error
                )
                self.log.error(msg)
                raise GCERemoveImgException(msg) from error

    # ---------------------------------------------------------------------
    def _query_yes_no(self, image):
        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}

        while True:
            try:
                choice = input(
                    '\tConfirm Delete Image: %s\t (Y/n)'
                    % image.get('name')
                ).lower()
                if choice in yes:
                    return True
                elif choice in no:
                    return False
                else:
                    sys.stdout.write("Please respond with 'yes' or 'no'\n")
            except KeyboardInterrupt:
                raise GCERemoveImgException(
                    'Keyboard Interrupt received, exiting'
                )
