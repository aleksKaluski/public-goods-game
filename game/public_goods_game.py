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

    def calculate_payoffs(self) -> int:
        """
        Calculates the payoff for each agent in the game
        :return: individual payoff
        """
        pass



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
        public_goods = total_contributions*self.factor + total_contributions

        # give payoff to agents
        list_of_payoffs = []
        for agent in self.agents:
            payoff = int(public_goods//self.n_agents)
            agent.receive_payoff(payoff)
            list_of_payoffs.append(payoff)
            agent.to_string()

        return list_of_payoffs




pgg = PublicGoodsGame(n_agents=2, endowment=10, factor=0.5)
pgg.run_round()
