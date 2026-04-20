import numpy as np

from game import payoff


class Agent:
    def __init__(self, identifier: int, endowment: int, strategy: str = "coop", contribution: int = 0, payoff: int = 0):
        self.identifier = identifier
        self.strategy = strategy
        self.endowment = endowment
        self.contribution = contribution
        self.payoff = payoff

    def decide_contribution(self):
        # for the initial moment the endowment = contribution
        self.contribution = self.endowment


    def receive_payoff(self, payoff: int ):
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


