import os
import time
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.body_landmarks.front_landmarks import FrontBodyLandmarks
from app.body_landmarks.side_landmarks import SideBodyLandmarks
from app.body_measurement.main import BodyMeasurement
from app.image_process.main import contour, detect_landmarks, load_image
from app.image_process.mediapipe import Mediapipe
from app.schemas.body_landmarks import FrontAndSideCoords
from app.size_recommender.main import SizeRecommendationSystem

detector = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    detector['mediapipe'] = Mediapipe().detector
    yield
    # Clean up the ML models and release the resources
    detector.clear()

IMAGEDIR = "images/"
app = FastAPI(lifespan=lifespan)


def cleanup(file_path: str):
    os.remove(file_path)


@app.get("/get_images/", description="Inference landmarks")
async def download_images(file_path: str, background_tasks: BackgroundTasks):
    path = IMAGEDIR+file_path
    try:
        background_tasks.add_task(cleanup, path)
        return FileResponse(path, media_type='image/jpeg')
    except Exception as e:
        # Handle file not found or other errors
        raise HTTPException(status_code=404, detail=e) from e


@app.post("/process_images", description="Inference landmarks")
async def process_images(front_image: UploadFile = File(...), side_image: UploadFile = File(...)):
    front_path = f"{IMAGEDIR}{time.time()}-{front_image.filename}"
    side_path = f"{IMAGEDIR}{time.time()}-{side_image.filename}"

    # save the file
    front_img = await front_image.read()
    with open(front_path, "wb") as f:
        f.write(front_img)

    side_img = await side_image.read()
    with open(side_path, "wb") as f:
        f.write(side_img)

    front = load_image(front_path, 512)
    side = load_image(side_path, 512)
    front_detection = detect_landmarks(detector["mediapipe"], front)
    side_detection = detect_landmarks(detector["mediapipe"], side)
    front_contours = contour(front_detection)
    side_contours = contour(side_detection)

    if front_detection is None or side_detection is None:
        raise HTTPException(
            status_code=500, detail="Error during contour extraction")

    if front_contours is None or side_contours is None:
        raise HTTPException(
            status_code=500, detail="Error during contour extraction")

    front_landmarks = FrontBodyLandmarks(
        front_detection.pose_landmarks[0], front_contours[-1], front, debug=True)
    front_landmarks.display_image("front")
    front_path = front_landmarks.get_image(front_path)

    side_landmarks = SideBodyLandmarks(
        side_detection.pose_landmarks[0], side_contours[-1], side, debug=True)
    side_landmarks.display_image("side")
    side_path = side_landmarks.get_image(side_path)

    return FrontAndSideCoords(front=front_landmarks.json(), side=side_landmarks.json(), front_path=front_path, side_path=side_path)


class MeasureReq(BaseModel):
    actual_height: float
    adjusted_keypoints: FrontAndSideCoords


@app.post("/measure_result", description="Get measurement result from the adjusted keypoints")
async def calculate_measure_result(request: MeasureReq):
    measure_result = BodyMeasurement(
        keypoints=request.adjusted_keypoints, height=request.actual_height)
    measurement_result = measure_result.measure_result()
    recommended_size = SizeRecommendationSystem(
        measurement_result).recommend_size()
    return {"measurement_result": measurement_result, "recommended_size": recommended_size}
