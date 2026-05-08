from agents.agent import Agent
import pandas as pd


class PublicGoodsGame:
    """
    A central class of the project. It is here where the game happens.
    Functionalities:
    - Initialize the game
    - Run rounds of the game
    - Save info about the hame history
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
            for i in range(strategy[key]): self.agents.append(Agent(endowment,
                                                                    key))

        # track history
        self.history = [] # all previous states of the game

        # game stats (fast and for testing)
        self.number_of_turns = 1


    def calculate_payoffs(self, agent: Agent) -> int:
        """
        Calculates the payoff for each agent in the game and makes the agent receive it.
        As for now we make it in a naive way.
        """
        payoff = int(self.public_goods//self.n_agents)
        agent.receive_payoff(payoff)
        return payoff


    def run_round(self) -> None:
        """
        Run a single round of the game.
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
        agent_moves = []
        list_of_payoffs = []
        for agent in self.agents:
            calculated_payoff = self.calculate_payoffs(agent)
            list_of_payoffs.append(calculated_payoff)

            agent_moves.append({"id": agent.identifier,
                                "payoff": agent.payoff,
                                "contribution": agent.contribution,
                                "strategy": agent.strategy})

        # compute stats and keep them in the dict
        self.record_round(round_number=self.number_of_turns,
                          factor=self.factor,
                          average_contribution= total_contributions / self.n_agents,
                          average_cooperation=n_agents_contributed / self.n_agents,
                          average_payoff=sum(list_of_payoffs) / len(list_of_payoffs),
                          public_goods=self.public_goods,
                          agents=agent_moves)

        self.number_of_turns += 1

    def record_round(self, **kwargs):
        """
        Transfer info about a single round of the game to the list of dicts (self.history)
        """
        self.history.append({
            "round_number": kwargs.get('round_number'),
            "factor": kwargs.get('factor'),
            "average_contribution": round(kwargs.get('average_contribution'), 2),
            "average_cooperation": round(kwargs.get('average_cooperation'), 2),
            "average_payoff": round(kwargs.get('average_payoff'), 2),
            "public_goods": round(kwargs.get('public_goods'), 2),
            "agents": kwargs.get('agents')
        })


    def game_stats(self):
        """
        Retrieve game stats
        """
        n_rounds = self.history[-1].get("round_number")
        average_contribution = sum([elt.get("average_contribution") for elt in self.history])/n_rounds
        average_cooperation = self.history[-1].get("average_cooperation")
        average_payoff = sum([elt.get("average_payoff") for elt in self.history])/n_rounds
        public_goods = self.history[-1].get("public_goods")

        print(f"\nGame stats after {n_rounds} turns:")
        print(f"\tAverage contribution: {round(average_contribution, 2)}")
        print(f"\tAverage cooperation: {round(average_cooperation, 2)}")
        print(f"\tAverage payoff: {round(average_payoff, 2)}")
        print(f"\tPublic goods: {round(public_goods, 2)}")
        print(self.history)

        return average_payoff, average_contribution, average_cooperation, n_rounds

