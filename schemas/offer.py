from typing import Literal

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class Offer(BaseModel):

    supplier: str
    item: Literal["apple", "chip", "gold"]
    quantity: PositiveInt
    price: PositiveFloat
    message: str = Field(default="")
