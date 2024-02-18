
from pydantic import BaseModel


class Coords(BaseModel):
    x: float
    y: float


class FrontCoords(BaseModel):
    shoulder_left_coords: Coords
    shoulder_right_coords: Coords
    sleeve_top_coords: Coords
    elbow_coords: Coords
    sleeve_bot_coords: Coords
    waist_start_coords: Coords
    waist_end_coords: Coords
    bust_left_coords: Coords
    bust_right_coords: Coords
    hip_left_coords: Coords
    hip_right_coords: Coords
    pants_top_coords: Coords
    knee_coords: Coords
    pants_bot_coords: Coords
    top_coords: Coords
    bot_coords: Coords


class SideCoords(BaseModel):
    bust_left_coords: Coords
    bust_right_coords: Coords
    waist_start_coords: Coords
    waist_end_coords: Coords
    hip_left_coords: Coords
    hip_right_coords: Coords
    top_coords: Coords
    bot_coords: Coords


class FrontAndSideCoordsIn(BaseModel):
    front: FrontCoords
    side: SideCoords


class FrontAndSideCoordsOut(BaseModel):
    front: FrontCoords
    side: SideCoords
    front_path: str
    side_path: str
