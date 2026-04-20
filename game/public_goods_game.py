from agents.agent import Agent


class PublicGoodsGame:
    """
    A central class of the project. It is here where the game happens.
    Functionalities:
    - Initialize the game
    - Run rounds of the game
    """

    def __init__(self, n_agents: int, endowment: int, factor: float):
        self.n_agents = n_agents # number of agents
        self.agents = [Agent(i, endowment) for i in range(n_agents)] # list of Agent class objects
        self.endowment = endowment
        self.factor = factor # factor that multiplies the payoff from public pot
        self.public_goods = 0

        # game stats
        self.average_contribution = 0
        self.average_cooperation = 0


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
        for agent in self.agents:
            agent.to_string()
            agent.decide_contribution()
            total_contributions += agent.contribution

        # multiply them by a factor
        self.public_goods = total_contributions*self.factor + total_contributions

        # give payoff to agents
        list_of_payoffs = []
        for agent in self.agents:
            calculated_payoff = self.calculate_payoffs(agent)
            list_of_payoffs.append(calculated_payoff)
        return list_of_payoffs

    def game_stas(self):
        """
        Retrieve game stats
        :return:
        """
        pass



pgg = PublicGoodsGame(n_agents=2, endowment=10, factor=0.5)
pgg.run_round()
