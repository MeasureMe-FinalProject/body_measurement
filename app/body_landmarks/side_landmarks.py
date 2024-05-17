from typing import List

from app.body_landmarks.body_landmarks import BodyLandmarks
from app.body_landmarks.helpers import parse_coords
from app.schemas.body_landmarks import Coords, SideCoords


class SideBodyLandmarks(BodyLandmarks):
    """
    Landmarks from side-facing image.

    This class represents landmarks detected from a side-facing image.
    It inherits properties and methods from the `BodyLandmarks` class.

    Attributes:
        Inherits all attributes from the `BodyLandmarks` class.

    Methods:
        Inherits all methods from the `BodyLandmarks` class.
    """

    def __init__(self, keypoints, contours, image, debug: bool = False):
        super().__init__(keypoints, contours, image, debug=debug)

    def get_bottom_of_heel(self):
        left_heel, _ = super().get_bottom_of_heel()
        return left_heel

    def find_top_and_bottom(self) -> List[Coords]:
        return parse_coords(self.get_top_of_head(), self.get_bottom_of_heel())

    def find_bust_landmarks(self):
        left_shoulder, right_shoulder = self.get_bust()

        # Apply offset to shoulder keypoints
        x_offset, y_offset = self.offset_factor(0.02, 0.07)
        back_bust = self.apply_offset(left_shoulder, -x_offset, y_offset)
        front_bust = self.apply_offset(left_shoulder, x_offset, y_offset)
        # self.debug_points(back_bust[0], back_bust[1], color=(255, 255, 0))
        # self.debug_points(front_bust[0], front_bust[1], color=(255, 255, 0))

        # Find the nearest points on the contour for bust
        left_edge_point = self.find_nearest_contour_point(back_bust)
        right_edge_point = self.find_nearest_contour_point(front_bust)

        # Extract coordinates of nearest points
        x_start, y_start = int(left_edge_point[0]), int(left_edge_point[1])
        x_end, y_end = int(right_edge_point[0]), int(right_edge_point[1])

        start_point = Coords(x=x_start, y=y_start)
        end_point = Coords(x=x_end, y=y_end)

        # Debugging: Output debug points
        self.debug_points(x_start, y_start, color=(255, 255, 0))
        self.debug_points(x_end, y_end, color=(255, 255, 0))
        self.draw_line(start_point, end_point, (255, 255, 0))

        coords = [start_point, end_point]
        return coords

    def find_hip_landmarks(self):
        left_hip, right_hip = self.get_hip()
        # Apply offset to hip keypoints
        x_offset, y_offset = self.offset_factor(0.04, 0.04)
        left_hip = self.apply_offset(right_hip, x_offset, y_offset)
        right_hip = self.apply_offset(right_hip, -x_offset, y_offset)

        # Find the nearest points on the contour for hip
        left_edge_point = self.find_nearest_contour_point(left_hip)
        right_edge_point = self.find_nearest_contour_point(right_hip)

        # Extract coordinates of nearest points
        x_start, y_start = int(left_edge_point[0]), int(left_edge_point[1])
        x_end, y_end = int(right_edge_point[0]), int(right_edge_point[1])

        start_point = Coords(x=x_start, y=y_start)
        end_point = Coords(x=x_end, y=y_end)

        # Debugging: Output debug points
        self.debug_points(x_start, y_start, color=(255, 255, 0))
        self.debug_points(x_end, y_end, color=(255, 255, 0))
        self.draw_line(start_point, end_point, (255, 255, 0))

        coords = [start_point, end_point]
        return coords

    def convert_json(self) -> SideCoords:
        data = SideCoords(
            top_coords=self.top_coords,
            bust_start_coords=self.bust_left_coords,
            bust_end_coords=self.bust_right_coords,
            waist_start_coords=self.waist_left_coords,
            waist_end_coords=self.waist_right_coords,
            hip_start_coords=self.hip_left_coords,
            hip_end_coords=self.hip_right_coords,
            bot_coords=self.bot_coords,
        )

        return data
