import numpy as np
import uuid
from game import payoff
from agents.strategies import AlwaysCooperate, AlwaysDefect, RandomStrategy

class Agent:
    """
    Agent class that represents the agent's strategy and keeps info about agent's endowment and contribution.
    An agent is a minimal element of the game.
    """
    def __init__(self, endowment: int, strategy: str = "coop", contribution: int = 0, payoff: int = 0):
        self.identifier = str(uuid.uuid4().hex[:5]) # id
        self.endowment = endowment # current money of an agent
        self.contribution = contribution # how much the agent will contribute
        self.payoff = payoff # agent's payoff

        # type of strategy
        self.strategy = None
        self.set_strategy(strategy)

        self.cumulative_payoff = 0 # payoffs in the rounds
        self.contribution_history = [] # list of contributions
        self.payoff_history = [] # list of payoffs

    def set_strategy(self, strategy_name: str):
        """
        Helper for maping strategies to agents.
        """
        mapping = {
            "coop": AlwaysCooperate(name="Cooperative"),
            "defect": AlwaysDefect(name="Defector"),
            "random": RandomStrategy(name="Chaotic")
        }

        self.strategy = mapping.get(strategy_name)

        if not self.strategy:
            raise ValueError(f"Unknown strategy: {strategy_name}")



    def decide_contribution(self):
        """
        Decide how much contribution would be made. Substitute contribution from endowment.
        """
        contribution = self.strategy.decide_contribution(payoff=self.payoff,
                                                         endowment=self.endowment,
                                                         contribution_history=self.contribution_history,
                                                         payoff_history=self.payoff_history)


        try:
            self.contribution = contribution
            self.endowment -= contribution
            self.contribution_history.append(contribution)

        except UnboundLocalError:
            print("Contribution cannot be made, since the strategy not 'coop', 'defect' or 'random'.")


    def receive_payoff(self, payoff: int):
        """
        Update the agent's contribution and payoff.
        """
        self.payoff = payoff
        self.endowment += payoff
        self.cumulative_payoff += payoff
        self.payoff_history.append(self.payoff)

    def to_string(self):
        """
        Print the agent's statistics.
        """
        print(f"Agent ID: {self.identifier}")
        print(f"Endowment: {self.endowment}")
        print(f"Contribution: {self.contribution}")
        print(f"Payoff: {self.payoff}")
        print(f"Strategy: {self.strategy}")
        print("-"*20)

    #Move this to the world class sen agent position check in neighbourhoods
    # def check_neighbours(self, range):
    #     #look at the neighbours
    #     print()

    def vote(self, world, sight=3):

        nearby_agents = world.get_agents_in_range(
            self,
            sight
        )

        if not nearby_agents:
            return None

        # choose agent with minimum contribution or someting else
        voted_agent = min(
            nearby_agents,
            key=lambda agent: agent.contribution
        )

        return voted_agent


