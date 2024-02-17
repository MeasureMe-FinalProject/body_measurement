from typing import List

import numpy as np

from app.schemas.body_landmarks import Coords


def find_nearest_point(points, target):
    # Reshape the target array to match the shape of points
    target = target.reshape(1, 2)
    distances = np.linalg.norm(points - target, axis=2)
    nearest_index = np.argmin(distances)
    return points[nearest_index][0]


def parse_coords(start_coords: tuple[int, int], end_coords: tuple[int, int]) -> List[Coords]:
    """Accept start_coords and end_coords as tuples then return as a dictionary"""
    start = Coords(x=start_coords[0], y=start_coords[1])
    end = Coords(x=end_coords[0], y=end_coords[1])
    return [start, end]
