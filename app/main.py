from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.image_process import detect_landmarks, contour, load_image, Mediapipe
from app.body_landmarks import FrontBodyLandmarks, SideBodyLandmarks, FrontAndSideCoords
from app.body_measurement import BodyMeasurement

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


class AdjustedKeypoints(BaseModel):
    keypoints: dict


@app.get("/", description="Test")
async def get_root():
    return {"message": "Hello World"}


@app.post("/", description="Test Post")
async def post_root(text: str,):
    return {"message": text}


@app.post("/process_images", description="Inference landmarks")
async def process_images(front_image: UploadFile = File(...), side_image: UploadFile = File(...), height: float = 0):

    # save the file
    front_img = await front_image.read()
    with open(f"{IMAGEDIR}{front_image.filename}", "wb") as f:
        f.write(front_img)

    side_img = await side_image.read()
    with open(f"{IMAGEDIR}{side_image.filename}", "wb") as f:
        f.write(side_img)

    front = load_image(f"{IMAGEDIR}{front_image.filename}", 512)
    side = load_image(f"{IMAGEDIR}{side_image.filename}", 512)
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
        height, front_detection.pose_landmarks[0], front_contours[0], front)
    front_landmarks.display_image("front")

    side_landmarks = SideBodyLandmarks(
        height, side_detection.pose_landmarks[0], side_contours[0], side)
    side_landmarks.display_image("side")
    return FrontAndSideCoords(front=front_landmarks.json(), side=side_landmarks.json())


@app.post("/measure_result", description="Get measurement result from the adjusted keypoints")
async def measure_result(adjusted_keypoints: FrontAndSideCoords):
    measure_result = BodyMeasurement(keypoints=adjusted_keypoints)
    return measure_result.measure_result()
