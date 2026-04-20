from agents.agent import Agent


class PublicGoodsGame:

    def __init__(self, n_agents: int, endowment: int, factor: float):
        self.n_agents = n_agents # number of agents
        self.agents = [Agent(i, endowment) for i in range(n_agents)] # list of Agent class objects
        self.endowment = endowment
        self.factor = factor # factor that multiplies the payoff from public pot

    def run_round(self):

        # collect contributions from all agents
        # contributions =

        pass

pgg = PublicGoodsGame(n_agents=2, endowment=100, factor=0.5)
