from pydantic import BaseModel


class Coords(BaseModel):
    x: float
    y: float


class FrontCoords(BaseModel):
    top_coords: Coords
    shoulder_start_coords: Coords
    shoulder_end_coords: Coords
    sleeve_top_coords: Coords
    elbow_coords: Coords
    sleeve_bot_coords: Coords
    bust_start_coords: Coords
    bust_end_coords: Coords
    waist_start_coords: Coords
    waist_end_coords: Coords
    hip_start_coords: Coords
    hip_end_coords: Coords
    pants_top_coords: Coords
    knee_coords: Coords
    pants_bot_coords: Coords
    bot_coords: Coords


class SideCoords(BaseModel):
    top_coords: Coords
    bust_start_coords: Coords
    bust_end_coords: Coords
    waist_start_coords: Coords
    waist_end_coords: Coords
    hip_start_coords: Coords
    hip_end_coords: Coords
    bot_coords: Coords


class FrontAndSideCoordsIn(BaseModel):
    front: FrontCoords
    side: SideCoords


class FrontAndSideCoordsOut(BaseModel):
    front: FrontCoords
    side: SideCoords
    front_path: str
    side_path: str
