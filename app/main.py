from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from numpy import size
from pydantic import BaseModel

from app.image_process.main import detect_landmarks, contour, load_image, Mediapipe
from app.body_landmarks.main import FrontBodyLandmarks, SideBodyLandmarks, FrontAndSideCoords
from app.body_measurement.main import BodyMeasurement
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


@app.get("/", description="Test")
async def get_root():
    return {"message": "Hello World"}


@app.post("/", description="Test Post")
async def post_root(text: str,):
    return {"message": text}


@app.post("/process_images", description="Inference landmarks")
async def process_images(front_image: UploadFile = File(...), side_image: UploadFile = File(...)):

    FRONT = f"{IMAGEDIR}{front_image.filename}"
    SIDE = f"{IMAGEDIR}{side_image.filename}"

    # save the file
    front_img = await front_image.read()
    with open(FRONT, "wb") as f:
        f.write(front_img)

    side_img = await side_image.read()
    with open(SIDE, "wb") as f:
        f.write(side_img)

    front = load_image(FRONT, 512)
    side = load_image(SIDE, 512)
    front_detection = detect_landmarks(detector["mediapipe"], front)
    side_detection = detect_landmarks(detector["mediapipe"], side)
    front_contours = contour(front_detection)
    side_contours = contour(side_detection)

    os.remove(FRONT)
    os.remove(SIDE)

    if front_detection is None or side_detection is None:
        raise HTTPException(
            status_code=500, detail="Error during contour extraction")

    if front_contours is None or side_contours is None:
        raise HTTPException(
            status_code=500, detail="Error during contour extraction")

    front_landmarks = FrontBodyLandmarks(
        front_detection.pose_landmarks[0], front_contours[-1], front)
    front_landmarks.display_image("front")

    side_landmarks = SideBodyLandmarks(
        side_detection.pose_landmarks[0], side_contours[-1], side)
    side_landmarks.display_image("side")
    return FrontAndSideCoords(front=front_landmarks.json(), side=side_landmarks.json())

class MeasureReq(BaseModel):
    actual_height: float
    adjusted_keypoints: FrontAndSideCoords


@app.post("/measure_result", description="Get measurement result from the adjusted keypoints")
async def measure_result(request: MeasureReq):
    measure_result = BodyMeasurement(
        keypoints=request.adjusted_keypoints, height=request.actual_height)
    measurement_result = measure_result.measure_result()
    recommended_size = SizeRecommendationSystem(
        measurement_result).recommend_size()
    return {"measurement_result": measurement_result, "recommended_size": recommended_size}
