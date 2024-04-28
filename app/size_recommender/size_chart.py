from fastapi import APIRouter

from app.body_measurement.main import MeasureChart

class SizeChart:
    MAN_SIZE_CHART = {
        "XS": MeasureChart(
            height=155,
            bust_circumference=76,
            waist_circumference=68,
            hip_circumference=83.1,
            shoulder_width=41.6,
            sleeve_length=54.5,
            pants_length=93,
        ),
        "S": MeasureChart(
            height=160,
            bust_circumference=80,
            waist_circumference=72,
            hip_circumference=85.9,
            shoulder_width=42.8,
            sleeve_length=55.5,
            pants_length=96,
        ),
        "M": MeasureChart(
            height=165,
            bust_circumference=84,
            waist_circumference=74,
            hip_circumference=88.7,
            shoulder_width=44,
            sleeve_length=56.5,
            pants_length=99,
        ),
        "L": MeasureChart(
            height=170,
            bust_circumference=88,
            waist_circumference=78,
            hip_circumference=91.5,
            shoulder_width=45.2,
            sleeve_length=57.5,
            pants_length=102,
        ),
        "XL": MeasureChart(
            height=180,
            bust_circumference=96,
            waist_circumference=84,
            hip_circumference=97.1,
            shoulder_width=47.6,
            sleeve_length=60,
            pants_length=108,
        ),
    }

    WOMAN_SIZE_CHART = {
        "XS": MeasureChart(
            height=154,
            bust_circumference=79,
            waist_circumference=64,
            hip_circumference=84,
            shoulder_width=36,
            sleeve_length=55,
            pants_length=88,
        ),
        "S": MeasureChart(
            height=159,
            bust_circumference=83,
            waist_circumference=68,
            hip_circumference=87,
            shoulder_width=38,
            sleeve_length=56,
            pants_length=90.5,
        ),
        "M": MeasureChart(
            height=164,
            bust_circumference=87,
            waist_circumference=72,
            hip_circumference=90,
            shoulder_width=40,
            sleeve_length=57,
            pants_length=93.5,
        ),
        "L": MeasureChart(
            height=169,
            bust_circumference=91,
            waist_circumference=76,
            hip_circumference=93,
            shoulder_width=42,
            sleeve_length=58,
            pants_length=96.5,
        ),
        "XL": MeasureChart(
            height=174,
            bust_circumference=95,
            waist_circumference=81,
            hip_circumference=97,
            shoulder_width=44,
            sleeve_length=59,
            pants_length=99.5,
        ),
    }

    JACKET = {
        "S": MeasureChart(
            height=0,
            shoulder_width=45,
            sleeve_length=59,
            bust_circumference=112,
            waist_circumference=0,
            hip_circumference=0,
            pants_length=0,
        ),
        "M": MeasureChart(
            height=0,
            shoulder_width=46,
            sleeve_length=60,
            bust_circumference=116,
            waist_circumference=0,
            hip_circumference=0,
            pants_length=0,
        ),
        "L": MeasureChart(
            height=0,
            shoulder_width=48,
            sleeve_length=61,
            bust_circumference=120,
            waist_circumference=0,
            hip_circumference=0,
            pants_length=0,
        ),
        "XL": MeasureChart(
            height=0,
            shoulder_width=50,
            sleeve_length=61.5,
            bust_circumference=126,
            waist_circumference=0,
            hip_circumference=0,
            pants_length=0,
        ),
    }


router = APIRouter(
    prefix="/size_chart",
    tags=["Size Chart"],
    responses={404: {"description": "Not found"}},
)


@router.get("/man", response_model=dict[str, MeasureChart])
async def get_man_size_chart():
    return SizeChart.MAN_SIZE_CHART


@router.get("/woman", response_model=dict[str, MeasureChart])
async def get_woman_size_chart():
    return SizeChart.WOMAN_SIZE_CHART
