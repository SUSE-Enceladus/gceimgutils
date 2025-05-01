import pytest

from unittest.mock import patch, MagicMock

from gceimgutils.gcedeprecateimg import GCEDeprecateImage


class TestGCEDeprecateImage(object):
    def setup_method(self, method):
        self.images_client = MagicMock()
        self.logger = MagicMock()
        self.operation = MagicMock()
        self.images_client.deprecate.return_value = self.operation

        self.kwargs = {
            'image_name': 'image123',
            'project': 'fakeproject',
            'credentials_path': 'test/data/creds.json',
            'log_callback': self.logger
        }

        self.deprecater = GCEDeprecateImage(**self.kwargs)

    @patch('gceimgutils.gceutils.compute_v1')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_deprecate_image(self, mock_auth_session, mock_compute_v1):
        mock_compute_v1.ImagesClient.return_value = self.images_client

        self.operation.error_code = None
        self.operation.warnings = None
        self.operation.result.return_value = 0

        self.deprecater.deprecate_image()

    @patch('gceimgutils.gceutils.compute_v1')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_deprecate_exc(self, mock_auth_session, mock_compute_v1):
        mock_compute_v1.ImagesClient.return_value = self.images_client

        self.operation.error_code = None
        self.operation.warnings = None
        self.operation.result.return_value = 0
        self.images_client.deprecate.side_effect = Exception(
            'Invalid credentials!'
        )

        with pytest.raises(Exception) as error:
            self.deprecater.deprecate_image()

        msg = 'Unable to deprecate image: "image123". Invalid credentials!'
        assert str(error.value) == msg
