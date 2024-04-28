from app.body_measurement.main import MeasureChart


class WeightChart:
    T_SHIRT = MeasureChart(
        height=1,
        shoulder_width=1,
        sleeve_length=0,
        bust_circumference=1,
        waist_circumference=0.5,
        hip_circumference=0.1,
        pants_length=0,
    )

    LONG_SHIRT = MeasureChart(
        height=1,
        shoulder_width=1,
        sleeve_length=1,
        bust_circumference=1,
        waist_circumference=0.5,
        hip_circumference=0.1,
        pants_length=0,
    )

    SHORT_PANTS = MeasureChart(
        height=1,
        shoulder_width=0,
        sleeve_length=0,
        bust_circumference=0,
        waist_circumference=0.5,
        hip_circumference=0.75,
        pants_length=0,
    )

    LONG_PANTS = MeasureChart(
        height=1,
        shoulder_width=0,
        sleeve_length=0,
        bust_circumference=0,
        waist_circumference=0.5,
        hip_circumference=0.75,
        pants_length=1,
    )

    JACKET = MeasureChart(
        height=1,
        shoulder_width=1,
        sleeve_length=1,
        bust_circumference=1,
        waist_circumference=0,
        hip_circumference=0,
        pants_length=0,
    )
