from typing import Dict, List

from models.agent import Agent
from schemas.offer import Offer
from utils.render_template import render_template


class Market:

    def __init__(self, agents: Dict[str, Agent]):
        self.public_board: List[Offer] = []
        self.agents = agents

    def clear_public_board(self) -> None:
        self.public_board.clear()

    def format_public_board(self) -> str:

        if self.public_board:
            return render_template("market", {"public_board": self.public_board})

        return "There aren't any available offers"

    def create_offer(self, offer: Offer) -> str:

        current_qty = self.agents[offer.supplier].config.state[offer.item]
        if current_qty < offer.quantity:
            raise ValueError(
                f"""Itens insuficientes. Você tem {current_qty} {offer.item}, 
                tentou vender {offer.quantity}"""
            )

        self.public_board.append(offer)
        return "Offer created"
