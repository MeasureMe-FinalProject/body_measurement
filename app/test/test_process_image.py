import os
import unittest
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class TestProcessImage(TestCase):
    def setUp(self):
        """Prepare each test with a clean environment and initialize the test client."""
        self.test_image_dir = os.path.join(os.getcwd(), "test_images")
        self.front_image_path = os.path.join(self.test_image_dir, "front_test.jpg")
        self.side_image_path = os.path.join(self.test_image_dir, "side_test.jpg")
        self.front_cat_image_path = os.path.join(self.test_image_dir, "cat_front.jpg")
        self.side_cat_image_path = os.path.join(self.test_image_dir, "cat_side.jpg")

    def tearDown(self):
        pass

    def test_process_images_real_images(self):
        """Test processing real images loaded from files."""
        with TestClient(app) as client:
            with open(self.front_image_path, "rb") as front_file, open(
                self.side_image_path, "rb"
            ) as side_file:
                files = {
                    "front_image": ("front.jpg", front_file, "image/jpeg"),
                    "side_image": ("side.jpg", side_file, "image/jpeg"),
                }
                response = client.post("/process_images", files=files)

        # Assertions
        assert response.status_code == 200
        assert "front" in response.json()
        assert "side" in response.json()

    def test_process_images_detector_not_initialized(self):
        """Test processing images when the detector is not initialized."""
        with TestClient(app) as client:
            # Mock the detector to not include 'mediapipe'
            with patch("app.main.detector", {}):
                with open(self.front_image_path, "rb") as front_file, open(
                    self.side_image_path, "rb"
                ) as side_file:
                    files = {
                        "front_image": ("front.jpg", front_file, "image/jpeg"),
                        "side_image": ("side.jpg", side_file, "image/jpeg"),
                    }
                    response = client.post("/process_images", files=files)

                # Assertions
                assert response.status_code == 503
                assert "detector not initialized" in response.json()["detail"]

    def test_image_no_human_pose(self):
        """Test error handling during image processing when no human pose is detected."""
        with TestClient(app) as client:
            # Mock the image processing and pose detection functions
            with open(self.front_cat_image_path, "rb") as front_file, open(
                self.side_cat_image_path, "rb"
            ) as side_file:
                files = {
                    "front_image": ("front.jpg", front_file, "image/jpeg"),
                    "side_image": ("side.jpg", side_file, "image/jpeg"),
                }
                response = client.post("/process_images", files=files)

            # Assertions to check the response for error handling
            assert response.status_code == 422
            assert "Body not found" in response.json()["detail"]


# More test cases can be added to simulate different error scenarios or edge cases.
if __name__ == "__main__":
    unittest.main()
