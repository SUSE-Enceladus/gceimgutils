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
# along with gceuploadblob. If not, see <http://www.gnu.org/licenses/>.

import logging
import os

from gceimgutils.gceimgutils import GCEImageUtils
from gceimgutils.gceimgutilsExceptions import GCEUploadBlobException


class GCEUploadBlob(GCEImageUtils):
    """Class to upload blobs to a bucket in a GCE project"""

    # ---------------------------------------------------------------------
    def __init__(
        self,
        bucket_name,
        source_filename,
        blob_name=None,
        checksum=None,
        credentials_path=None,
        credentials_info=None,
        project=None,
        log_callback=None,
        log_level=logging.INFO,
    ):
        GCEImageUtils.__init__(
            self,
            project,
            credentials_path,
            credentials_info,
            log_level,
            log_callback
        )

        self.blob_name = (
            blob_name or source_filename.rsplit(os.sep, maxsplit=1)[-1]
        )
        self.source_filename = source_filename
        self.bucket_name = bucket_name
        self.checksum = checksum

    # ---------------------------------------------------------------------
    def upload_blob(self):
        """Upload the blob"""
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(self.blob_name)

        try:
            blob.upload_from_filename(
                self.source_filename,
                checksum=self.checksum
            )
        except Exception as error:
            msg = f'Unable to upload blob: "{self.blob_name}". {str(error)}'
            self.log.error(msg)
            raise GCEUploadBlobException(msg) from error

        return blob
