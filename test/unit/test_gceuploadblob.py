import pytest

from unittest.mock import patch, MagicMock

from gceimgutils.gceuploadblob import GCEUploadBlob


class TestGCEUploadBlob(object):
    def setup_method(self, method):
        self.storage_client = MagicMock()
        self.logger = MagicMock()

        self.kwargs = {
            'bucket_name': 'bucket',
            'source_filename': 'test/data/fake.tar.gz',
            'credentials_path': 'test/data/creds.json',
            'log_callback': self.logger
        }

        self.uploader = GCEUploadBlob(**self.kwargs)

    @patch('gceimgutils.gceutils.storage')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_remove_blob(self, mock_auth_session, mock_storage):
        mock_storage.Client.return_value = self.storage_client

        self.uploader.upload_blob()

    @patch('gceimgutils.gceutils.storage')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_deprecate_exc(self, mock_auth_session, mock_storage):
        mock_storage.Client.return_value = self.storage_client

        blob = MagicMock()
        bucket = MagicMock()
        bucket.blob.return_value = blob
        blob.upload_from_filename.side_effect = Exception(
            'Invalid credentials!'
        )

        self.storage_client.bucket.return_value = bucket

        with pytest.raises(Exception) as error:
            self.uploader.upload_blob()

        msg = 'Unable to upload blob: "fake.tar.gz". Invalid credentials!'
        assert str(error.value) == msg
