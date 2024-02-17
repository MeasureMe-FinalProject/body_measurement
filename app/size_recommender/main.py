from app.body_measurement.main import MeasureResult


class SizeRecommendationSystem:
    def __init__(self, customer_measurements: MeasureResult):
        self.size_chart = {
            'XS': MeasureResult(height=155, bust_circumference=76, waist_circumference=68, hip_circumference=83.1, shoulder_width=41.6, sleeve_length=54.5, pants_length=93),
            'S': MeasureResult(height=160, bust_circumference=80, waist_circumference=72, hip_circumference=85.9, shoulder_width=42.8, sleeve_length=55.5, pants_length=96),
            'M': MeasureResult(height=165, bust_circumference=84, waist_circumference=74, hip_circumference=88.7, shoulder_width=44, sleeve_length=56.5, pants_length=99),
            'L': MeasureResult(height=170, bust_circumference=88, waist_circumference=78, hip_circumference=91.5, shoulder_width=45.2, sleeve_length=57.5, pants_length=102),
            'XL': MeasureResult(height=180, bust_circumference=96, waist_circumference=84, hip_circumference=97.1, shoulder_width=47.6, sleeve_length=60, pants_length=108),
        }
        self.weights = MeasureResult(height=1, bust_circumference=1, waist_circumference=1,
                                     hip_circumference=1, shoulder_width=1, sleeve_length=1, pants_length=1)
        self.customer_measurements = customer_measurements

    def calculate_deviation(self, measurements: MeasureResult):
        deviations: dict = {}

        for size, size_measurements in self.size_chart.items():
            deviations[size] = sum(
                self.weights[key] *
                abs(measurements[key] - size_measurements[key])
                for key, val in measurements
            )
        return deviations

    def recommend_size(self):
        deviations = self.calculate_deviation(self.customer_measurements)
        recommended_size = min(deviations, key=lambda k: deviations.get(k, 0))
        return recommended_size
