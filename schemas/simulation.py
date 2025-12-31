from pydantic import BaseModel, Field, PositiveInt


class SimulationSettings(BaseModel):
    rounds: PositiveInt = Field(
        description='Number of rounds to simulate',
    )
