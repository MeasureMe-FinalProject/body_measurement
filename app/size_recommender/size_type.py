from typing import Literal, Union

SizeOutput = Union[Literal["XXS", "XS", "S", "M", "L", "XL", "XXL"], str]


class SizeType:
    def __call__(
        self, size: Union[Literal["XXS", "XS", "S", "M", "L", "XL", "XXL"], int]
    ) -> str:
        if isinstance(size, int):
            return str(size)
        elif size in ["XXS", "XS", "S", "M", "L", "XL", "XXL"]:
            return size
        else:
            raise ValueError("Invalid size value")

