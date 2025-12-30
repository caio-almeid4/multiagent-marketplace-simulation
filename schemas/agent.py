from typing import Literal

from pydantic import BaseModel, Field

from agents.states.agent import AgentState


class AgentConfig(BaseModel):

    name: str
    temperature: float = Field(ge=0, le=1)
    state: AgentState


class AgentResponse:

    next_step: Literal["manage_offers", "manage_inbox", "wait"]


class AgentAnalysis(AgentResponse):

    updated_monologue: str
