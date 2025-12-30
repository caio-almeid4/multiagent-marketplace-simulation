from typing import Any, Dict

from langchain.tools import BaseTool
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from agents.states.agent import AgentState, AgentStateUpdate
from schemas.agent import AgentAnalysis, AgentConfig
from utils.render_template import render_template


class Agent:

    def __init__(self, config: AgentConfig, tools: Dict[str, BaseTool] = {}):
        self.config = config
        self.name = self.config.name
        self.state = self.config.state
        self.llm = self._get_llm()
        self.graph = self._build_graph()
        self.tools = tools

    def _get_llm(self):

        return ChatOpenAI(
            model="gpt-4o",
            temperature=self.config.temperature,
        )

    def _update_messages(self, message: AnyMessage) -> None:

        self.state["messages"].append(message)

    def _get_internal_memory(self) -> SystemMessage:
        return SystemMessage(
            render_template(
                "memory",
                {"internal_monologue": self.config.state["internal_monologue"]},
            )
        )
        
    def _get_inventory(self) -> SystemMessage:
        return SystemMessage(
            render_template(
                'inventory',
                {
                    'cash':self.state['cash'],
                    'apple':self.state['apple'],
                    'gold':self.state['gold'],
                    'chip':self.state['chip']
                }
            )
        )

    def run_turn(self, market_data: str) -> Dict[str, Any]:

        self._update_messages(self._get_internal_memory())
        self._update_messages(HumanMessage(market_data))
        self._update_messages(self._get_inventory())
        self._update_messages(
            SystemMessage(
                """Return ONLY a JSON object with EXACTLY the following fields:
- updated_monologue: string
- next_step: Literal['create_offer', 'manage_inbox', 'wait']

Do not include any other text.

YOU SHOULD GO to create_offer step to create offers and sell products."""
            )
        )

        return self.graph.invoke(self.state)

    def _build_graph(self):

        graph = StateGraph(AgentState)
        graph.add_node("router", self._routing_node)
        graph.add_node("analyze_market", self._analyze_market)
        graph.add_node("manage_inbox", self._manage_inbox)
        graph.add_node("create_offer", self._create_offer)

        graph.add_edge(START, "analyze_market")
        graph.add_edge("analyze_market", "router")
        graph.add_edge("manage_inbox", END)
        graph.add_edge("create_offer", END)

        return graph.compile()

    def _analyze_market(self, state: AgentState) -> Command:

        agent = self.llm.with_structured_output(AgentAnalysis)
        response = agent.invoke(state["messages"])

        return Command(update={
            "internal_monologue": response["updated_monologue"],
            "next_step": response["next_step"],
        }
        )

    def _routing_node(self, state: AgentState) -> Command:
        next_step = state.get("next_step")

        if next_step in ("wait", "", None):
            return Command(goto=END)

        return Command(goto=next_step)

    def _manage_inbox(self, state: AgentState) -> AgentStateUpdate:

        print("Managed inbox")
        return AgentStateUpdate(**state)

    def _create_offer(self, state: AgentState) -> Command:

        state['messages'].pop()
        state['messages'].append(SystemMessage('use the tool create_public_offer to create an offer'))
        agent = self.llm.bind_tools([self.tools["create_public_offer"]])
        response = agent.invoke(self.state["messages"])
        messages = self._execute_tools(response.tool_calls)

        return Command(update={"messages": messages})

    def _execute_tools(self, tool_calls):

        messages = []
        for call in tool_calls:
            result = self.tools[call["name"]].invoke(call["args"])
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=call["id"],
                )
            )
        return messages
