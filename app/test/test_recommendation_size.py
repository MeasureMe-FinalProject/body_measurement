import unittest

from app.body_measurement.main import MeasureChart
from app.size_recommender.main import SizeRecommendationSystem


class TestSizeRecommendationSystem(unittest.TestCase):
    def setUp(self):
        self.weights = MeasureChart(
            height=1,
            bust_circumference=1,
            waist_circumference=1,
            hip_circumference=1,
            shoulder_width=1,
            sleeve_length=1,
            pants_length=1,
        )

        self.customer_1 = MeasureChart(
            height=155,
            bust_circumference=76,
            waist_circumference=68,
            hip_circumference=83.1,
            shoulder_width=41.6,
            sleeve_length=54.5,
            pants_length=93,
        )

        self.customer_2 = MeasureChart(
            height=170,
            bust_circumference=88,
            waist_circumference=78,
            hip_circumference=91.5,
            shoulder_width=45.2,
            sleeve_length=57.5,
            pants_length=102,
        )

        self.recommendation_system_1 = SizeRecommendationSystem(
            "MALE", "T_SHIRT", self.customer_1
        )
        self.recommendation_system_1.weights = self.weights

        self.recommendation_system_2 = SizeRecommendationSystem(
            "MALE", "T_SHIRT", self.customer_2
        )

    def test_recommend_size(self):
        self.assertEqual(
            self.recommendation_system_1.recommend_size(),
            "XS",
            "Incorrect recommended size for the given measurements",
        )

        self.assertEqual(
            self.recommendation_system_2.recommend_size(),
            "L",
            "Incorrect recommended size for the given measurements",
        )


if __name__ == "__main__":
    unittest.main()
