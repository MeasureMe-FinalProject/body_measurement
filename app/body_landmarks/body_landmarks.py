from abc import abstractmethod
from typing import List

import cv2
import numpy as np

from app.body_landmarks.helpers import find_nearest_point
from app.image_process.face_blur import anonymize_face
from app.schemas.body_landmarks import Coords


class BodyLandmarks:
    """
    Represents landmarks detected on the human body.

    This class provides a representation for landmarks detected on the human body.

    Attributes:
        keypoints (list): List of keypoints detected on the human body.
        contours (list): List of contours detected on the human body.
        image (cv2.typing.MatLike): The image containing the body on which landmarks are detected.
        debug (bool): Flag indicating whether debug mode is enabled or not.

    # This class is meant to be inherited by more specific classes.
    """

    def __init__(self, keypoints, contours, image: cv2.typing.MatLike, debug: bool):
        """
        Initialize the BodyMeasurement instance.

        Parameters:
        - height (float): The actual height of the subject.
        - keypoints (list): List of keypoints.
        - contours (list): List of contours.
        - image (numpy.ndarray): The image.

        Returns:
        None
        """
        self.image = anonymize_face(image, keypoints)
        self.process_image = self.image.copy()

        self.width, self.height = self.process_image.shape[:2]
        self.keypoints = keypoints
        self.contours = contours
        self.debug = debug
        self.hip_left_coords, self.hip_right_coords = self.find_hip_landmarks()

        self.waist_left_coords, self.waist_right_coords = self.find_waist_landmarks()

        self.bust_left_coords, self.bust_right_coords = self.find_bust_landmarks()

        self.top_coords, self.bot_coords = self.find_top_and_bottom()

        # HELPER FUNCTIONS

    def get_image(self, img_path: str) -> str:
        path = img_path.split("/")[1]
        cv2.imwrite(img_path, self.image)
        return path

    def offset_factor(self, x_offset_ratio, y_offset_ratio):
        x_offset = int(self.width * x_offset_ratio)
        y_offset = int(self.height * y_offset_ratio)

        return x_offset, y_offset

    def apply_offset(self, keypoints, x_offset, y_offset):
        x, y = keypoints
        x += x_offset
        y += y_offset
        return np.array([x, y])

    def find_nearest_contour_point(self, keypoints):
        return find_nearest_point(self.contours, keypoints)

    def calculate_middle_point(self, left, right):
        # Calculate the average of x and y coordinates
        x_left, y_left = left
        x_right, y_right = right
        middle_x = (x_left + x_right) / 2
        middle_y = (y_left + y_right) / 2

        # Return the middle point as a tuple
        middle_point = (middle_x, middle_y)
        return middle_point

    def get_keypoints(self, idx):
        landmark = self.keypoints[idx]
        key = (
            int(landmark.x * self.process_image.shape[1]),
            int(landmark.y * self.process_image.shape[0]),
        )
        return key[0], key[1]

        ############################################################################################################

    # DEBUGGER FUNCTIONS
    def debug_points(self, x, y, color=(0, 255, 0)):
        if self.debug:
            cv2.circle(self.process_image, (int(x), int(y)), 2, color, 2)

    def draw_line(self, start: Coords, end: Coords, color=(0, 255, 0)):
        if self.debug:
            start_coords = (int(start.x), int(start.y))
            end_coords = (int(end.x), int(end.y))
            cv2.line(self.process_image, start_coords, end_coords, color, 2)

        ############################################################################################################

    def get_bust(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Find the bust from shoulders keypoints based on
        /home/dapa/Documents/PAPER/JETIR2203456.pdf
        """
        # 11 and 12
        left_shoulder = self.get_keypoints(11)
        right_shoulder = self.get_keypoints(12)
        return left_shoulder, right_shoulder

    def get_hip(self) -> tuple[tuple[int, int], tuple[int, int]]:
        # Get hip keypoints
        left_hip = self.get_keypoints(23)
        right_hip = self.get_keypoints(24)
        return left_hip, right_hip

    def get_top_of_head(self) -> tuple[int, int]:
        """
        Get the top of the head based on the middle point of the two eyes
        and the nearest point on the contour with some offset
        """
        # This will offset the average of people hair height
        x_offset, y_offset = self.offset_factor(0.0, 0.05)

        # get the middle point of the two eyes
        x_left_eye, y_left_eye = self.get_keypoints(2)
        x_right_eye, y_right_eye = self.get_keypoints(5)

        # Calculate the middle point of the two eyes
        middle_point = self.calculate_middle_point(
            (x_left_eye, y_left_eye), (x_right_eye, y_right_eye)
        )
        middle_point = self.apply_offset(middle_point, 0, -y_offset)
        # self.debug_points(middle_point[0], middle_point[1], (0, 0, 0))

        # Get the nearest point on the contour based on the middle point of the two eyes
        top_point = self.find_nearest_contour_point(middle_point)
        self.debug_points(top_point[0], top_point[1], (0, 0, 0))
        return top_point

    def get_bottom_of_heel(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Front: Get the bottom of the heel based on the middle point of the two heel keypoints
        Side: Get the bottom of the heel based on the left heel keypoints
        """
        left_heel = self.get_keypoints(29)
        right_heel = self.get_keypoints(30)
        return left_heel, right_heel

    def find_waist_landmarks(self):
        """
        Get the center of the waist by getting the
        middle point of the 4 keypoints that are trapezoid shaped
        """
        x_offset, y_offset = self.offset_factor(0.01, 0.0)
        x1, y1 = self.get_keypoints(23)
        x2, y2 = self.get_keypoints(24)
        x3, y3 = self.get_keypoints(12)
        x4, y4 = self.get_keypoints(11)
        # Calculate midpoints
        M1 = ((x1 + x2) / 2, (y1 + y2) / 2)
        M2 = ((x3 + x4) / 2, (y3 + y4) / 2)

        middle_point = ((M1[0] + M2[0]) / 2, (M1[1] + M2[1]) / 2)
        self.debug_points(middle_point[0], middle_point[1], (255, 255, 0))

        # left_waist = self.apply_offset(middle_point, x_offset, -y_offset)
        right_waist = self.apply_offset(middle_point, -x_offset, -y_offset)
        # self.debug_points(left_waist[0], left_waist[1], (255, 255, 0))
        # self.debug_points(right_waist[0], right_waist[1], (255, 255, 0))

        # left_edge_point = self.find_nearest_contour_point(left_waist)
        right_edge_point = self.find_nearest_contour_point(right_waist)

        x_start, y_start = int(middle_point[0]), int(middle_point[1])
        x_end, y_end = int(right_edge_point[0]), int(right_edge_point[1])
        self.debug_points(x_start, y_start)
        self.debug_points(x_end, y_end)

        start_point = Coords(x=x_start, y=y_start)
        end_point = Coords(x=x_end, y=y_end)
        self.draw_line(start_point, end_point, (255, 255, 0))
        coords = [start_point, end_point]
        return coords

    @abstractmethod
    def find_hip_landmarks(self) -> List[Coords]:
        pass

    @abstractmethod
    def find_bust_landmarks(self) -> List[Coords]:
        pass

    @abstractmethod
    def find_top_and_bottom(self) -> List[Coords]:
        pass

    @abstractmethod
    def convert_json(self):
        pass

    def display_image(self, filename):
        cv2.imwrite(filename=f"res/{filename}_result.jpg", img=self.process_image)
