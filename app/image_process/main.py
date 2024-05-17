from http import HTTPStatus

import cv2
import mediapipe as mp
import numpy as np
from fastapi import HTTPException


def load_image(file_name, target_width):
    """Resizing image resolution"""
    img = cv2.imread(file_name)
    # Specify the target width and calculate the target height to maintain the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0]
    target_height = int(target_width / aspect_ratio)
    resized_img = cv2.resize(img, (target_width, target_height))
    return resized_img


def detect_landmarks(detector, _img):
    """Detect bodylandmarks"""
    try:
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(_img))
        detection_result = detector.detect(img)

        return detection_result
    except Exception as e:
        print(f"Error during landmark detection: {e}")
        return None


def contour(detection_result):
    """Define contour using detection result"""
    if detection_result.segmentation_masks is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Body not found",
        )
    try:
        segmentation_mask = detection_result.segmentation_masks[0].numpy_view()
        visualized_mask = (
            np.repeat(segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255
        )

        gray = cv2.cvtColor(visualized_mask, cv2.COLOR_BGR2GRAY)
        flag, thresh = cv2.threshold(gray.astype(np.uint8), 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Draw contours on the image
        contour_image = np.zeros_like(visualized_mask)
        cv2.drawContours(contour_image, contours, -1, (0, 0, 255), 2)
        cv2.imwrite("res/contour.jpg", contour_image)
        return contours
    except (AttributeError, IndexError) as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Error during contour extraction: {e}",
        )
