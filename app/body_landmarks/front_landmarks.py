from typing import List

from app.body_landmarks.body_landmarks import BodyLandmarks
from app.body_landmarks.helpers import parse_coords
from app.schemas.body_landmarks import Coords, FrontCoords


class FrontBodyLandmarks(BodyLandmarks):
    """
    Landmarks from front-facing image

    This class represents landmarks detected from a front-facing image.
    It inherits properties and methods from the `BodyLandmarks` class.

    Attributes:
        Inherits all attributes from the `BodyLandmarks` class.

    Methods:
        Inherits all methods from the `BodyLandmarks` class.
    """

    def __init__(self, keypoints, contours, image, debug: bool = False):
        super().__init__(keypoints, contours, image, debug=debug)
        (
            self.shoulder_left_coords,
            self.shoulder_right_coords,
        ) = self.find_shoulder_landmarks()
        self.sleeve_top_coords = self.get_sleeve_top()
        self.elbow_coords = self.get_elbow()
        self.sleeve_bot_coords = self.get_sleeve_bot()
        self.pants_top_coords = self.get_pants_top()
        self.knee_coords = self.get_knee()
        self.pants_bot_coords = self.get_pants_bot()
        self.middle_shoulder_coords = self.find_middle_shoulder()
        self.middle_hip_coords = self.find_middle_hip()

    def find_shoulder_landmarks(self):
        x_offset, y_offset = self.offset_factor(0.03, 0.01)

        # 11 and 12
        left_shoulder = self.get_keypoints(12)
        right_shoulder = self.get_keypoints(11)

        # Apply offset to shoulder keypoints
        left_shoulder = self.apply_offset(left_shoulder, -x_offset, -y_offset)
        right_shoulder = self.apply_offset(right_shoulder, x_offset, -y_offset)
        # self.debug_points(left_shoulder[0], left_shoulder[1])
        # self.debug_points(right_shoulder[0], right_shoulder[1])

        # Find the nearest points on the contour for shoulders
        left_edge_point = self.find_nearest_contour_point(left_shoulder)
        right_edge_point = self.find_nearest_contour_point(right_shoulder)

        # Extract coordinates of nearest points
        x_start, y_start = int(left_edge_point[0]), int(left_edge_point[1])
        x_end, y_end = int(right_edge_point[0]), int(right_edge_point[1])

        start_point, end_point = (x_start, y_start), (x_end, y_end)

        # Debugging: Output debug points
        self.debug_points(x_start, y_start, (0, 0, 100))
        self.debug_points(x_end, y_end, (0, 0, 100))
        coords = parse_coords(start_point, end_point)
        return coords

    def find_middle_shoulder(self) -> Coords:
        left_shoulder, right_shoulder = (
            self.shoulder_left_coords,
            self.shoulder_right_coords,
        )

        left_shoulder = (left_shoulder.x, left_shoulder.y)
        right_shoulder = (right_shoulder.x, right_shoulder.y)

        print(left_shoulder, right_shoulder)

        middle_points = self.calculate_middle_point(left_shoulder, right_shoulder)
        return Coords(x=middle_points[0], y=middle_points[1])

    def find_hip_landmarks(self):
        left_hip, right_hip = self.get_hip()

        # Apply offset to hip keypoints
        x_offset, y_offset = self.offset_factor(0.04, 0.04)
        left_hip = self.apply_offset(left_hip, x_offset, y_offset)
        right_hip = self.apply_offset(right_hip, -x_offset, y_offset)

        # Find the nearest points on the contour for hip
        left_edge_point = self.find_nearest_contour_point(left_hip)
        right_edge_point = self.find_nearest_contour_point(right_hip)

        # Extract coordinates of nearest points
        x_start, y_start = int(left_edge_point[0]), int(left_edge_point[1])
        x_end, y_end = int(right_edge_point[0]), int(right_edge_point[1])

        start_point, end_point = (x_start, y_start), (x_end, y_end)

        # Debugging: Output debug points
        self.debug_points(x_start, y_start)
        self.debug_points(x_end, y_end)
        coords = parse_coords(start_point, end_point)
        return coords

    def find_middle_hip(self) -> Coords:
        left_hip, right_hip = (self.hip_left_coords, self.hip_right_coords)

        left_hip = (left_hip.x, left_hip.y)
        right_hip = (right_hip.x, right_hip.y)

        middle_points = self.calculate_middle_point(left_hip, right_hip)
        return Coords(x=middle_points[0], y=middle_points[1])

    def get_bottom_of_heel(self) -> tuple[int, int]:
        left_heel, right_heel = super().get_bottom_of_heel()

        x_left_heel, y_left_heel = left_heel
        x_right_heel, y_right_heel = right_heel

        left_heel = (x_left_heel, y_left_heel)
        right_heel = (x_right_heel, y_right_heel)

        # Debugging: Output debug points
        self.debug_points(x_left_heel, y_left_heel)
        self.debug_points(x_right_heel, y_right_heel)

        middle_point = self.calculate_middle_point(left_heel, right_heel)
        return middle_point

    def find_top_and_bottom(self) -> List[Coords]:
        return parse_coords(self.get_top_of_head(), self.get_bottom_of_heel())

    def find_bust_landmarks(self):
        left_shoulder, right_shoulder = self.get_bust()

        # Apply offset to shoulder keypoints
        x_offset, y_offset = self.offset_factor(0.0, 0.04)
        left_shoulder = self.apply_offset(left_shoulder, x_offset, y_offset)
        right_shoulder = self.apply_offset(right_shoulder, x_offset, y_offset)

        # Find the nearest points on the contour for shoulders
        left_edge_point = left_shoulder
        right_edge_point = right_shoulder

        # Extract coordinates of nearest points
        x_start, y_start = int(left_edge_point[0]), int(left_edge_point[1])
        x_end, y_end = int(right_edge_point[0]), int(right_edge_point[1])

        start_point, end_point = (x_start, y_start), (x_end, y_end)

        # Debugging: Output debug points
        self.debug_points(x_start, y_start, color=(255, 255, 0))
        self.debug_points(x_end, y_end, color=(255, 255, 0))
        coords = parse_coords(start_point, end_point)
        return coords

    def get_sleeve_top(self):
        x, y = self.get_keypoints(12)
        self.debug_points(x, y, color=(255, 255, 0))
        return Coords(x=x, y=y)

    def get_elbow(self):
        x, y = self.get_keypoints(14)
        self.debug_points(x, y, color=(255, 255, 0))
        return Coords(x=x, y=y)

    def get_sleeve_bot(self):
        x, y = self.get_keypoints(16)
        self.debug_points(x, y, color=(255, 255, 0))
        return Coords(x=x, y=y)

    def get_pants_top(self):
        x, y = self.get_keypoints(24)
        self.debug_points(x, y, color=(255, 255, 0))
        return Coords(x=x, y=y)

    def get_knee(self):
        x, y = self.get_keypoints(26)
        self.debug_points(x, y, color=(255, 255, 0))
        return Coords(x=x, y=y)

    def get_pants_bot(self):
        x, y = self.get_keypoints(28)
        self.debug_points(x, y, color=(255, 255, 0))
        return Coords(x=x, y=y)

    def convert_json(self) -> FrontCoords:
        data = FrontCoords(
            top_coords=self.top_coords,
            shoulder_start_coords=self.shoulder_left_coords,
            shoulder_end_coords=self.shoulder_right_coords,
            sleeve_top_coords=self.sleeve_top_coords,
            elbow_coords=self.elbow_coords,
            sleeve_bot_coords=self.sleeve_bot_coords,
            bust_start_coords=self.bust_left_coords,
            bust_end_coords=self.bust_right_coords,
            waist_start_coords=self.waist_left_coords,
            waist_end_coords=self.waist_right_coords,
            hip_start_coords=self.hip_left_coords,
            hip_end_coords=self.hip_right_coords,
            pants_top_coords=self.pants_top_coords,
            knee_coords=self.knee_coords,
            pants_bot_coords=self.pants_bot_coords,
            bot_coords=self.bot_coords,
        )
        return data
