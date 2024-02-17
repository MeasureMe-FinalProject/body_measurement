import cv2


def get_keypoints(img: cv2.typing.MatLike, keypoints, idx):
    landmark = keypoints[idx]
    key = int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0])
    return key[0], key[1]


def anonymize_face(image: cv2.typing.MatLike, keypoints, factor=30.0) -> cv2.typing.MatLike:
    face_keypoint = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # Automatically determine the size of the blurring kernel based
    # on the spatial dimensions of the input image
    (h, w) = image.shape[:2]
    kW = int(w / factor)
    kH = int(h / factor)
    # Ensure the width of the kernel is odd
    if kW % 2 == 0:
        kW -= 1
    # Ensure the height of the kernel is odd
    if kH % 2 == 0:
        kH -= 1
    # Apply a Gaussian blur to the input image using our computed kernel size
    for keypoint in face_keypoint:
        x, y = get_keypoints(image, keypoints, keypoint)
        # Ensure the region is within image bounds
        x1, y1 = max(x - kW // 2, 0), max(y - kH // 2, 0)
        x2, y2 = min(x + kW // 2, w), min(y + kH // 2, h)
        # Apply Gaussian blur to the region
        blurred_region = cv2.GaussianBlur(image[y1:y2, x1:x2], (kW, kH), 0)
        # Replace the original region with the blurred region
        image[y1:y2, x1:x2] = blurred_region
    return image
