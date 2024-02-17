from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class Mediapipe():
    """Initiate detector"""

    def __init__(self) -> None:
        base_options = python.BaseOptions(
            model_asset_path='app/models/pose_landmarker_heavy.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(options)
