from typing import Optional

import numpy as np
from pydantic import BaseModel

from app.schemas.body_landmarks import Coords, FrontAndSideCoordsIn


class MeasureChart(BaseModel):
    def __getitem__(self, item):
        return getattr(self, item)

    height: float
    bust_circumference: float
    chest_width: Optional[float] = 0.0
    waist_circumference: float
    waist_width: Optional[float] = 0.0
    hip_circumference: float
    shoulder_width: float
    sleeve_length: float
    pants_length: float


class BodyMeasurement:
    def __init__(self, keypoints: FrontAndSideCoordsIn, height: float):
        self.height = height
        self.front = keypoints.front
        self.side = keypoints.side

        self.front_ratio = self.get_front_ratio()
        self.side_ratio = self.get_side_ratio()

    def calculate_distance(self, start: Coords, end: Coords) -> float:
        start_array = np.array((start.x, start.y))
        end_array = np.array((end.x, end.y))
        distance = np.linalg.norm(end_array - start_array)
        return float(distance)

    def get_front_ratio(self) -> float:
        x_top, y_top = self.front.top_coords.x, self.front.top_coords.y
        x_bot, y_bot = self.front.bot_coords.x, self.front.bot_coords.y

        start = Coords(x=x_top, y=y_top)
        end = Coords(x=x_bot, y=y_bot)
        coords = [start, end]
        distance_pixels = self.calculate_distance(coords[0], coords[1])

        ratio = self.height / distance_pixels
        return ratio

    def get_side_ratio(self) -> float:
        x_top, y_top = self.side.top_coords.x, self.side.top_coords.y
        x_bot, y_bot = self.side.bot_coords.x, self.side.bot_coords.y

        start = Coords(x=x_top, y=y_top)
        end = Coords(x=x_bot, y=y_bot)
        coords = [start, end]
        distance_pixels = self.calculate_distance(coords[0], coords[1])

        # Calculate the scale factor
        ratio = self.height / distance_pixels
        return ratio

    def circumference(self, long_axis, short_axis):
        """
        Calculate circumference of ellipse
        /home/dapa/Documents/PAPER/Body_Size_Measurement_Using_a_Smartphone.pdf
        """
        c = 2 * np.pi * np.sqrt((np.power(long_axis, 2) + np.power(short_axis, 2)) / 2)
        return c

    def calculate_chest_width(self) -> float:
        if self.front is not None and self.side is not None:
            long_axis = (
                self.calculate_distance(
                    self.front.bust_start_coords, self.front.bust_end_coords
                )
                * self.front_ratio
            )
            return long_axis
        else:
            return 0.0

    def calculate_waist_width(self) -> float:
        if self.front is not None and self.side is not None:
            long_axis = (
                self.calculate_distance(
                    self.front.waist_start_coords, self.front.waist_end_coords
                )
                * self.front_ratio
            )
            return long_axis
        else:
            return 0.0

    def calculate_waist_circumference(self) -> float:
        if self.front is not None and self.side is not None:
            long_axis = self.calculate_waist_width()
            short_axis = (
                self.calculate_distance(
                    self.side.waist_start_coords, self.side.waist_end_coords
                )
                * self.side_ratio
            )
            return self.circumference(long_axis, short_axis)
        else:
            return 0.0

    def calculate_bust_circumference(self) -> float:
        if self.front is not None and self.side is not None:
            long_axis = self.calculate_chest_width() / 2
            short_axis = (
                self.calculate_distance(
                    self.side.bust_start_coords, self.side.bust_end_coords
                )
                * self.side_ratio
                / 2
            )
            return self.circumference(long_axis, short_axis)
        else:
            return 0.0

    def calculate_hip_circumference(self) -> float:
        if self.front is not None and self.side is not None:
            long_axis = (
                self.calculate_distance(
                    self.front.hip_start_coords, self.front.hip_start_coords
                )
                * self.front_ratio
                / 2
            )
            short_axis = (
                self.calculate_distance(
                    self.side.hip_start_coords, self.side.hip_end_coords
                )
                * self.side_ratio
                / 2
            )
            return self.circumference(long_axis, short_axis)
        else:
            return 0.0

    def calculate_shoulder_width(self) -> float:
        if self.front is not None and self.side is not None:
            return (
                self.calculate_distance(
                    self.front.shoulder_start_coords, self.front.shoulder_end_coords
                )
                * self.front_ratio
            )
        else:
            return 0.0

    def calculate_sleeve_length(self) -> float:
        if self.front is not None and self.side is not None:
            shoulder_to_elbow = (
                self.calculate_distance(
                    self.front.sleeve_top_coords, self.front.elbow_coords
                )
                * self.front_ratio
            )
            elbow_to_wrist = (
                self.calculate_distance(
                    self.front.elbow_coords, self.front.sleeve_bot_coords
                )
                * self.front_ratio
            )

            return shoulder_to_elbow + elbow_to_wrist
        else:
            return 0.0

    def calculate_pants_length(self) -> float:
        if self.front is not None and self.side is not None:
            hip_to_knee = (
                self.calculate_distance(
                    self.front.pants_top_coords, self.front.knee_coords
                )
                * self.front_ratio
            )
            knee_to_ankle = (
                self.calculate_distance(
                    self.front.knee_coords, self.front.pants_bot_coords
                )
                * self.front_ratio
            )

            return hip_to_knee + knee_to_ankle
        else:
            return 0.0

    def calculate_inseam_length(self) -> float:
        if self.front is not None and self.side is not None:
            return (
                self.calculate_distance(
                    self.front.hip_start_coords, self.front.knee_coords
                )
                * self.front_ratio
                + self.calculate_distance(
                    self.front.knee_coords, self.front.pants_bot_coords
                )
                * self.front_ratio
            )
        else:
            return 0.0

    def measure_result(self):
        data = MeasureChart(
            height=self.height,
            bust_circumference=self.calculate_bust_circumference(),
            chest_width=self.calculate_chest_width(),
            waist_circumference=self.calculate_waist_circumference(),
            waist_width=self.calculate_waist_width(),
            hip_circumference=self.calculate_hip_circumference(),
            shoulder_width=self.calculate_shoulder_width(),
            sleeve_length=self.calculate_sleeve_length(),
            pants_length=self.calculate_pants_length(),
        )
        return data
