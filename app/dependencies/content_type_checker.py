from typing import List

from fastapi import HTTPException, UploadFile


class ContentTypeChecker:
    def __init__(self, content_types: List[str]) -> None:
        self.content_types = content_types

    def __call__(self, front_image: UploadFile, side_image: UploadFile):
        if not all(image.content_type in self.content_types for image in [front_image, side_image]):
            raise HTTPException(
                400, detail="Invalid document type")
        return True
