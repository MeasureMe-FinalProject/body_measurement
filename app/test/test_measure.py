import unittest
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import app


class TestMeasure(TestCase):
    def setUp(self):
        self.adjusted_keypoints = {
            "front": {
                "top_coords": {"x": 243.0, "y": 98.0},
                "shoulder_start_coords": {"x": 173.0, "y": 207.0},
                "shoulder_end_coords": {"x": 309.0, "y": 211.0},
                "sleeve_top_coords": {"x": 189.0, "y": 209.0},
                "elbow_coords": {"x": 164.0, "y": 278.0},
                "sleeve_bot_coords": {"x": 143.0, "y": 319.0},
                "bust_start_coords": {"x": 294.0, "y": 233.0},
                "bust_end_coords": {"x": 189.0, "y": 229.0},
                "waist_start_coords": {"x": 243.0, "y": 287.0},
                "waist_end_coords": {"x": 189.0, "y": 287.0},
                "hip_start_coords": {"x": 302.0, "y": 384.0},
                "hip_end_coords": {"x": 185.0, "y": 384.0},
                "pants_top_coords": {"x": 214.0, "y": 364.0},
                "knee_coords": {"x": 201.0, "y": 484.0},
                "pants_bot_coords": {"x": 195.0, "y": 597.0},
                "bot_coords": {"x": 252.5, "y": 614.5},
            },
            "side": {
                "top_coords": {"x": 218.0, "y": 88.0},
                "bust_start_coords": {"x": 236.0, "y": 190.0},
                "bust_end_coords": {"x": 295.0, "y": 201.0},
                "waist_start_coords": {"x": 254.0, "y": 261.0},
                "waist_end_coords": {"x": 218.0, "y": 252.0},
                "hip_start_coords": {"x": 291.0, "y": 380.0},
                "hip_end_coords": {"x": 211.0, "y": 375.0},
                "bot_coords": {"x": 280.0, "y": 627.0},
            },
            "front_path": "1714833573.2066374-front.jpg",
            "side_path": "1714833573.2066455-side.jpg",
        }

    def test_measure_result(self):
        """Test processing real images loaded from files."""
        request_data = {
            "actual_height": 160.0,
            "gender": "MALE",  # Assuming your Gender enum includes 'Male'
            "clothing_type": "T_SHIRT",  # Assuming your ClothingType enum includes 'Shirt'
            "adjusted_keypoints": self.adjusted_keypoints,
        }

        with TestClient(app) as client:
            response = client.post("/measure_result", json=request_data)

        # Assertions to check the response
        assert response.status_code == 200
        assert "measurement_result" in response.json()
        assert "size_recommendation" in response.json()

    def test_missing_value(self):
        """Test processing real images loaded from files."""
        request_data = {
            "actual_height": 160.0,
            "gender": "MALE",  # Assuming your Gender enum includes 'Male'
            "clothing_type": "T_SHIRT",  # Assuming your ClothingType enum includes 'Shirt'
            "adjusted_keypoints": None,
        }

        with TestClient(app) as client:
            response = client.post("/measure_result", json=request_data)

        # Assertions to check the response
        assert response.status_code == 422


if __name__ == "__main__":
    unittest.main()
