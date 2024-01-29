import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


# def draw_landmarks_on_image(rgb_image, detection_result):
#   pose_landmarks_list = detection_result.pose_landmarks
#   annotated_image = np.copy(rgb_image)

#   # Loop through the detected poses to visualize.
#   for idx in range(len(pose_landmarks_list)):
#     pose_landmarks = pose_landmarks_list[idx]

#     # Draw the pose landmarks.
#     pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
#     pose_landmarks_proto.landmark.extend([
#       landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
#     ])
#     solutions.drawing_utils.draw_landmarks(
#       annotated_image,
#       pose_landmarks_proto,
#       solutions.pose.POSE_CONNECTIONS,
#       solutions.drawing_styles.get_default_pose_landmarks_style())
#   return annotated_image


def load_image(file_name, target_width):
    img = cv2.imread(file_name)
    # Specify the target width and calculate the target height to maintain the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0]
    target_height = int(target_width / aspect_ratio)
    resized_img = cv2.resize(img, (target_width, target_height))
    return resized_img


def detect_landmarks(detector, _img):
    try:
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(_img))
        detection_result = detector.detect(img)

        return detection_result
    except Exception as e:
        print(f"Error during landmark detection: {e}")
        return None


def contour(detection_result):
    try:
        segmentation_mask = detection_result.segmentation_masks[0].numpy_view()
        visualized_mask = np.repeat(
            segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255

        gray = (cv2.cvtColor(visualized_mask, cv2.COLOR_BGR2GRAY))
        flag, thresh = cv2.threshold(gray.astype(
            np.uint8), 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Draw contours on the image
        return contours
    except (AttributeError, IndexError) as e:
        print(f"Error during contour extraction: {e}")
        return None


class Mediapipe():
    def __init__(self) -> None:
        base_options = python.BaseOptions(
            model_asset_path='app/models/pose_landmarker_heavy.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(options)
