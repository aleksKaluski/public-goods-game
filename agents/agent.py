import numpy as np

from game import payoff


class Agent:
    """
    Agent class that represents the agent's strategy and keeps info about agent's endowment and contribution.
    An agent is a minimal element of the game.
    """
    def __init__(self, identifier: int, endowment: int, strategy: str = "coop", contribution: int = 0, payoff: int = 0):
        self.identifier = identifier
        self.strategy = strategy
        self.endowment = endowment
        self.contribution = contribution
        self.payoff = payoff

    def decide_contribution(self):
        """
        Decide how much contribution would be made.
        """
        if self.strategy == "coop":
            # for the initial moment the endowment = contribution
            self.contribution = self.endowment
        if self.strategy == "defect":
            self.contribution = 0
        if self.strategy == "random":
            self.contribution = np.random.randint(low=0, high=self.endowment)


    def receive_payoff(self, payoff: int ):
        """
        Update the agent's contribution and payoff.
        """
        self.payoff = payoff
        self.endowment += payoff

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

    def check_neighbours(self, range):
        #look at the neighbours
        print()

    def vote(self):
        #vote for one of the checked neighbors
        check_neighbours(3)


