from typing import Literal

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class OfferDraft(BaseModel):
    supplier: str
    item: Literal['apple', 'chip', 'gold']
    quantity: PositiveInt
    price: PositiveFloat
    message: str = Field(default='')


class TrackedOffer(OfferDraft):
    id: int
