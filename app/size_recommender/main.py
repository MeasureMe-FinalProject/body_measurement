from typing import Dict, Literal, Optional

from app.body_measurement.main import MeasureChart
from app.size_recommender.model import InputModel, SizeRecommendationModel
from app.size_recommender.size_chart import SizeChart
from app.size_recommender.size_type import SizeOutput, SizeType

ClothingType = Literal["T_SHIRT", "SHORT_PANTS", "LONG_PANTS", "JACKET"]
GarmentType = Literal["Tops", "Pants"]
Gender = Literal["MALE", "FEMALE"]
size_type = SizeType()


class SizeRecommendationSystem:
    def __init__(
        self,
        gender: Gender,
        clothing_type: ClothingType,
        customer_measurements: MeasureChart,
    ):
        self.gender = gender.lower()
        self.model = SizeRecommendationModel()
        self.customer_measurements = customer_measurements
        self.clothing_type = clothing_type
        self.garment_type: GarmentType = (
            "Tops" if self.clothing_type == "T_SHIRT" else "Pants"
        )
        self.use_model = self._should_use_model()

    def _should_use_model(self):
        return self.clothing_type in ["T_SHIRT", "SHORT_PANTS", "JACKET"]

    def recommend_size(self) -> SizeOutput:
        if self.use_model:
            return self._predict_size_with_model()

        self.size_chart = self._get_size_chart()
        if self.clothing_type == "LONG_PANTS":
            return self._find_best_fit_longpants()
        elif self.clothing_type == "LONG_SLEEVE":
            return self._find_best_fit_longsleeve()
        else:
            raise ValueError("Unsupported clothing type for size recommendation")

    def _get_size_chart(self):
        if self.clothing_type == "LONG_PANTS":
            if self.gender == "male":
                return SizeChart.MALE_LONGPANTS
            elif self.gender == "female":
                return SizeChart.FEMALE_LONGPANTS
        return {}

    def _find_best_fit(
        self,
        size_chart,
        user_measurements: Dict[str, float],
        weight_factor: Optional[Dict[str, float]] = None,
    ) -> SizeOutput:
        best_fit = None
        smallest_difference = float("inf")

        for size, measurements in size_chart.items():
            total_diff = self._calculate_total_difference(
                user_measurements, measurements, weight_factor
            )

            if total_diff < smallest_difference:
                smallest_difference = total_diff
                best_fit = size

        if best_fit is None:
            best_fit = "XS"  # Default to XS if no suitable size is found

        return size_type(best_fit)

    def _calculate_total_difference(
        self,
        user_measurements: Dict[str, float],
        chart_measurements: Dict[str, float],
        weight_factor: Optional[Dict[str, float]] = None,
    ):
        total_diff = 0
        weight_factor = weight_factor or {}

        for dim, user_value in user_measurements.items():
            chart_value = chart_measurements.get(dim)
            if chart_value is None:
                continue

            weight = weight_factor.get(dim, 1.0)
            total_diff += weight * abs(chart_value - user_value)

        return total_diff

    def _find_best_fit_longpants(self) -> SizeOutput:
        measurements = {
            "Height": self.customer_measurements.height,
            "Waist": self.customer_measurements.waist_circumference,
            "Pants_length": self.customer_measurements.pants_length,
        }
        weight_factor = {
            "Waist": 2.0,
            "Height": 1.0,
            "Pants_length": 1.0,
        }
        return self._find_best_fit(self.size_chart, measurements, weight_factor)

    def _find_best_fit_longsleeve(self) -> SizeOutput:
        measurements = {
            "Height": self.customer_measurements.height,
            "Bust": self.customer_measurements.bust_circumference,
            "Shoulder_width": self.customer_measurements.shoulder_width,
            "Sleeve_length": self.customer_measurements.sleeve_length,
        }
        return self._find_best_fit(self.size_chart, measurements)

    def _predict_size_with_model(self):
        prediction = self.model.predict(
            InputModel(
                Gender=self.gender,
                Height=self.customer_measurements.height,
                Garment_Type=self.garment_type,
                Chest=self.customer_measurements.bust_circumference,
                Waist=self.customer_measurements.waist_circumference,
                Hip=self.customer_measurements.hip_circumference,
            )
        )
        return size_type(prediction)
