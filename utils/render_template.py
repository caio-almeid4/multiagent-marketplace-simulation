from pathlib import Path
from typing import Any, Dict

from jinja2 import Template


def render_template(name: str, variables: Dict[str, Any]) -> str:

    template_path = Path("agents/templates") / f"{name}.jinja"
    with open(template_path, "r", encoding="utf-8") as t:
        template = Template(t.read())

    renderized_template = template.render(**variables)

    return renderized_template
