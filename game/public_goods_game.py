from agents.agent import Agent
import pandas as pd

class PublicGoodsGame:
    """
    A central class of the project. It is here where the game happens.
    Functionalities:
    - Initialize the game
    - Run rounds of the game
    """

    def __init__(self, endowment: int, factor: float, strategy: dict):
        # strategy is a dict of strings
        # that provides potential strategies of the agents and their number
        # {"coop" : 10, "defect" :5, "random":0} means that we have 15 agents
        # with various strategies

        # key arguments
        assert (isinstance(strategy, dict)), "Strategy must be a dict"
        assert (strategy != {}), "Strategy must not be empty!"

        self.n_agents = sum(strategy.values()) # number of agents
        self.agents = []

        self.endowment = endowment
        self.factor = factor # factor that multiplies the payoff from public pot
        self.public_goods = 0

        # initialize various agents
        for key in strategy:
            for i in range(strategy[key]): self.agents.append(Agent(i, endowment, key))

        # game stats
        self.number_of_turns = 0
        self.average_payoff = []
        self.average_contribution = []
        self.average_cooperation = []


    def calculate_payoffs(self, agent: Agent) -> int:
        """
        Calculates the payoff for each agent in the game and makes the agent receive it.
        As for now we make it in a naive way.
        """
        payoff = int(self.public_goods//self.n_agents)
        agent.receive_payoff(payoff)
        return payoff


    def run_round(self) -> list[int]:
        """
        Run a single round of the game.
        :return: list of payoffs
        """

        # collect contributions from all agents
        total_contributions = 0
        n_agents_contributed = 0
        for agent in self.agents:
            agent.decide_contribution()
            # agent.to_string()

            contribution = agent.contribution
            total_contributions += contribution

            if contribution > 0:
                n_agents_contributed += 1

        # multiply them by a factor
        if self.factor < 1:
            self.public_goods = total_contributions * self.factor + total_contributions
        else:
            self.public_goods = total_contributions*self.factor

        # give payoff to agents
        list_of_payoffs = []
        for agent in self.agents:
            calculated_payoff = self.calculate_payoffs(agent)
            list_of_payoffs.append(calculated_payoff)

        # compute stats
        self.number_of_turns += 1
        self.average_cooperation.append(n_agents_contributed / self.n_agents)
        self.average_payoff.append(sum(list_of_payoffs) / len(list_of_payoffs))
        self.average_contribution.append(total_contributions / self.n_agents)


    def game_stas(self):
        """
        Retrieve game stats
        """
        print(f"\nGame stats after {self.number_of_turns} turns:")
        print(f"Public goods: {self.public_goods}$")
        print(f"Average payoff: {sum(self.average_payoff) / self.number_of_turns:.2f}$")
        print(f"Average contribution: {sum(self.average_contribution) / self.number_of_turns:.2f}$")
        print(f"Average cooperation: {(sum(self.average_cooperation) / self.number_of_turns)*100:.2f}%")
        return self.average_payoff, self.average_contribution, self.average_cooperation, self.number_of_turns