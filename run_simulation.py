from dotenv import load_dotenv
import argparse

from models.agent import Agent
from models.market import Market
from schemas.simulation import SimulationSettings
from simulation import Simulation
from utils.agent_config import get_agents_configs
from utils.id_generator import SerialIDGenerator
from trade_service import TradeService
from db import get_db_session, create_tables



def main(rounds: int):

    load_dotenv()
    create_tables()
    
    agents_configs = get_agents_configs(['*'])
    agents = {name: Agent(config) for name, config in agents_configs.items()}
    id_gen = SerialIDGenerator()
    
    with get_db_session() as session:
        trade_service = TradeService(session=session)
        market = Market(agents=agents, id_gen=id_gen, trade_service=trade_service)
        sim_settings = SimulationSettings(rounds=rounds)
        sim = Simulation(settings=sim_settings, agents=agents, market=market)
        sim.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulation configs')
    parser.add_argument('--rounds', default=20, type=int)
    args = parser.parse_args()
    main(**vars(args))
