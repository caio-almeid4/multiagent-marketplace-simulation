from pathlib import Path
from typing import List

import yaml
from langchain_core.messages import SystemMessage

from agents.states.agent import AgentState
from schemas.agent import AgentConfig
from utils.render_template import render_template


def load_agent_config(name: str):

    filepath = Path("agents/configs") / f"{name}.yaml"

    with open(filepath, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    system_prompt = SystemMessage(render_template("system_prompt", config))

    agent_state = AgentState(
        **config["initial_state"],
        inbox=[],
        internal_monologue="",
        messages=[system_prompt],
        next_step="",
    )

    return AgentConfig(
        name=name,
        temperature=config["temperature"],
        state=agent_state,
    )


def get_agents_configs(agents: List[str]):

    if "*" not in agents:
        agents = [name.lower().strip().replace(" ", "_") for name in agents]

    else:
        folder = Path("agents/configs")
        agents = [
            f.name.split(".")[0]
            for f in folder.iterdir()
            if f.is_file() and f.suffix == ".yaml"
        ]

    configs = {name: load_agent_config(name) for name in agents}

    return configs
