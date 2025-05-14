import pytest

from unittest.mock import patch, MagicMock

from gceimgutils.gceremoveblob import GCERemoveBlob


class TestGCERemoveBlob(object):
    def setup_method(self, method):
        self.storage_client = MagicMock()
        self.logger = MagicMock()

        self.kwargs = {
            'bucket_name': 'bucket',
            'blob_name': 'blob',
            'credentials_path': 'test/data/creds.json',
            'log_callback': self.logger
        }

        self.remover = GCERemoveBlob(**self.kwargs)

    @patch('gceimgutils.gceutils.storage')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_remove_blob(self, mock_auth_session, mock_storage):
        mock_storage.Client.return_value = self.storage_client

        self.remover.remove_blob()

    @patch('gceimgutils.gceutils.storage')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_deprecate_exc(self, mock_auth_session, mock_storage):
        mock_storage.Client.return_value = self.storage_client

        bucket = MagicMock()
        bucket.delete_blob.side_effect = Exception(
            'Invalid credentials!'
        )

        self.storage_client.bucket.return_value = bucket

        with pytest.raises(Exception) as error:
            self.remover.remove_blob()

        msg = 'Unable to delete blob: "blob". Invalid credentials!'
        assert str(error.value) == msg
