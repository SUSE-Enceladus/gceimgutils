# Copyright 2026 SUSE LLC
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
# along with gcegetblob. If not, see <http://www.gnu.org/licenses/>.

import logging

from gceimgutils.gceimgutils import GCEImageUtils
from gceimgutils.gceimgutilsExceptions import GCEGetBlobException


class GCEGetBlob(GCEImageUtils):
    """Class to download blobs from a bucket in a GCE project"""

    # ---------------------------------------------------------------------
    def __init__(
        self,
        blob_name,
        bucket_name,
        destination_file_name,
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

        self.blob_name = blob_name
        self.bucket_name = bucket_name
        self.destination_file_name = destination_file_name

    # ---------------------------------------------------------------------
    def get_blob(self):
        """get the blob"""
        bucket = self.storage_client.bucket(self.bucket_name)

        try:
            blob = bucket.blob(
                blob_name=self.blob_name,
            )
            blob.download_to_filename(self.destination_file_name)
        except Exception as error:
            msg = f'Unable to download blob: "{self.blob_name}". {str(error)}'
            self.log.error(msg)
            raise GCEGetBlobException(msg) from error
