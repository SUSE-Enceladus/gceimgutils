import pytest

from unittest.mock import patch, MagicMock

from gceimgutils.gcegetblob import GCEGetBlob


class TestGCEGetBlob(object):
    def setup_method(self, method):
        self.storage_client = MagicMock()
        self.logger = MagicMock()

        self.kwargs = {
            'bucket_name': 'bucket',
            'blob_name': 'blob',
            'destination_file_name': 'test/data/blob.zip',
            'credentials_path': 'test/data/creds.json',
            'log_callback': self.logger
        }

        self.getter = GCEGetBlob(**self.kwargs)

    @patch('gceimgutils.gceutils.storage')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_get_blob(self, mock_auth_session, mock_storage):
        mock_storage.Client.return_value = self.storage_client

        self.getter.get_blob()

    @patch('gceimgutils.gceutils.storage')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_get_exc(self, mock_auth_session, mock_storage):
        mock_storage.Client.return_value = self.storage_client

        blob = MagicMock()
        bucket = MagicMock()
        bucket.blob.return_value = blob
        blob.download_to_filename.side_effect = Exception(
            'Invalid credentials!'
        )

        self.storage_client.bucket.return_value = bucket

        with pytest.raises(Exception) as error:
            self.getter.get_blob()

        msg = 'Unable to download blob: "blob". Invalid credentials!'
        assert str(error.value) == msg
