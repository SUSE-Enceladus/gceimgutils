import pytest

from unittest.mock import patch, MagicMock

from gceimgutils.gcecreateimg import GCECreateImage


class TestGCECreateImage(object):
    def setup_method(self, method):
        self.images_client = MagicMock()
        self.logger = MagicMock()
        self.operation = MagicMock()

        image = MagicMock()
        image.status = 'READY'

        self.images_client.insert.return_value = self.operation
        self.images_client.get.return_value = image

        self.kwargs = {
            'image_name': 'image123',
            'project': 'fakeproject',
            'image_description': 'Test image',
            'family': 'images',
            'bucket_name': 'my-bucket',
            'object_name': 'image.tar.gz',
            'guest_os_features': [
                'UEFI_COMPATIBLE',
                'VIRTIO_SCSI_MULTIQUEUE',
                'GVNIC'
            ],
            'licenses': [
                'projects/project-123/global/licenses/'
                'cloud-marketplace-1234567890123456-1234567890123456'
            ],
            'credentials_path': 'test/data/creds.json',
            'log_callback': self.logger
        }

        self.creator = GCECreateImage(**self.kwargs)

    @patch('gceimgutils.gceutils.time')
    @patch('gceimgutils.gceutils.compute_v1')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_create_image(
        self,
        mock_auth_session,
        mock_compute_v1,
        mock_time
    ):
        mock_compute_v1.ImagesClient.return_value = self.images_client

        self.operation.error_code = None
        self.operation.warnings = None
        self.operation.result.return_value = 0

        self.creator.create_image()

    @patch('gceimgutils.gceutils.time')
    @patch('gceimgutils.gceutils.compute_v1')
    @patch('gceimgutils.gceutils.AuthorizedSession')
    def test_create_exc(
        self,
        mock_auth_session,
        mock_compute_v1,
        mock_time
    ):
        mock_compute_v1.ImagesClient.return_value = self.images_client

        self.operation.error_code = None
        self.operation.warnings = None
        self.operation.result.return_value = 0
        self.images_client.insert.side_effect = Exception(
            'Invalid credentials!'
        )

        with pytest.raises(Exception) as error:
            self.creator.create_image()

        msg = 'Unable to create image: "image123". Invalid credentials!'
        assert str(error.value) == msg
