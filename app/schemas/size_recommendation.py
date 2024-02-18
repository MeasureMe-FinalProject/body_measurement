
from typing import Literal
from pydantic import BaseModel
from app.body_measurement.main import MeasureChart
from app.schemas.body_landmarks import FrontAndSideCoordsIn

from app.size_recommender.main import ClothingType, Gender


class MeasureResultIn(BaseModel):
    actual_height: float
    gender: Gender
    clothing_type: ClothingType
    adjusted_keypoints: FrontAndSideCoordsIn


SizeRecommendation = Literal["S", "M", "L", "XL"]


class MeasureResultOut(BaseModel):
    measurement_result: MeasureChart
    size_recommendation: SizeRecommendation
