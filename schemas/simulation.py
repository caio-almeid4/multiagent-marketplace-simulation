from pydantic import BaseModel, Field, PositiveInt


class SimulationSettings(BaseModel):

    rounds: PositiveInt = Field(
        default=20,
        description="Number of rounds to simulate",
    )
