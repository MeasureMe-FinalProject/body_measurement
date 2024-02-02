
import numpy as np
from app.body_landmarks.main import FrontAndSideCoords, calculate_distance


class BodyMeasurement():
    def __init__(self, keypoints: FrontAndSideCoords):
        self.front_ratio = keypoints.front.ratio
        self.side_ratio = keypoints.side.ratio
        self.front = keypoints.front
        self.side = keypoints.side

    def circumference(self, long_axis, short_axis):
        """
        Calculate circumference of ellipse
        /home/dapa/Documents/PAPER/Body_Size_Measurement_Using_a_Smartphone.pdf
        """
        c = 2*np.pi*np.sqrt((np.power(long_axis,2)+np.power(short_axis,2))/2)
        return c

    def calculate_waist_circumference(self):
        if self.front is not None and self.side is not None:
            long_axis = calculate_distance(self.front.waist_start_coords, self.front.waist_end_coords)*self.front_ratio
            short_axis = calculate_distance(self.side.waist_start_coords, self.side.waist_end_coords)*self.side_ratio
            return self.circumference(long_axis, short_axis)
        else:
            return None

    def calculate_bust_circumference(self):
        if self.front is not None and self.side is not None:
            long_axis = calculate_distance(self.front.bust_left_coords, self.front.bust_right_coords)*self.front_ratio / 2
            short_axis = calculate_distance(self.side.bust_left_coords, self.side.bust_right_coords)*self.side_ratio / 2
            return self.circumference(long_axis, short_axis)
        else:
            return None

    def calculate_hip_circumference(self):
        if self.front is not None and self.side is not None:
            long_axis = calculate_distance(self.front.hip_left_coords, self.front.hip_right_coords) * self.front_ratio / 2
            short_axis = calculate_distance(self.side.hip_left_coords, self.side.hip_right_coords) * self.side_ratio / 2
            return self.circumference(long_axis, short_axis)
        else:
            return None
        

    def calculate_shoulder_width(self):
        if self.front is not None and self.side is not None:
            return calculate_distance(self.front.shoulder_left_coords, self.front.shoulder_right_coords) * self.front_ratio
        else:
            return None
        
    def measure_result(self):
        data = {
            "waist_circumference": self.calculate_waist_circumference(),
            "bust_circumference": self.calculate_bust_circumference(),
            "hip_circumference": self.calculate_hip_circumference(),
            "shoulder_width": self.calculate_shoulder_width()
        }
        return data