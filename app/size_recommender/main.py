from typing import Literal

from app.body_measurement.main import MeasureChart
from app.size_recommender.size_chart import SizeChart
from app.size_recommender.weight_chart import WeightChart

ClothingType = Literal["T_SHIRT", "LONG_SHIRT", "SHORT_PANTS", "LONG_PANTS", "JACKET"]
Gender = Literal["MALE", "FEMALE"]


class SizeRecommendationSystem:
    def __init__(
        self,
        gender: Gender,
        clothing_type: ClothingType,
        customer_measurements: MeasureChart,
    ):
        self.customer_measurements = customer_measurements

        if gender == "MALE":
            self.size_chart = SizeChart.MAN_SIZE_CHART
        elif gender == "FEMALE":
            self.size_chart = SizeChart.WOMAN_SIZE_CHART
        else:
            raise ValueError("Invalid gender")

        if clothing_type == "T_SHIRT":
            self.weights = WeightChart.T_SHIRT
        elif clothing_type == "LONG_SHIRT":
            self.weights = WeightChart.LONG_SHIRT
        elif clothing_type == "SHORT_PANTS":
            self.weights = WeightChart.SHORT_PANTS
        elif clothing_type == "LONG_PANTS":
            self.weights = WeightChart.LONG_PANTS
        elif clothing_type == "JACKET":
            self.weights = WeightChart.JACKET
            self.size_chart = SizeChart.JACKET
        else:
            raise ValueError("Invalid clothing type")

    def calculate_deviation(self, measurements: MeasureChart):
        deviations: dict = {}

        for size, size_measurements in self.size_chart.items():
            deviations[size] = sum(
                self.weights[key] * abs(measurements[key] - size_measurements[key])
                for key, val in measurements
            )
        return deviations

    def recommend_size(self):
        deviations = self.calculate_deviation(self.customer_measurements)
        recommended_size = min(deviations, key=lambda k: deviations.get(k, 0))
        return recommended_size
