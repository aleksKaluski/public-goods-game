import random
import uuid
from agents.strategies import AlwaysCooperate, AlwaysDefect, RandomStrategy, AdaptiveStrategy
from dynamics.world import World

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

        # coords
        self.x = 0
        self.y = 0

        # da hood
        self.neighborhood = None

        # type of strategy
        self.strategy = None
        self.set_strategy(strategy)

        self.cumulative_payoff = 0 # payoffs in the rounds
        self.contribution_history = [] # list of contributions
        self.payoff_history = [] # list of payoffs

    def set_strategy(self, strategy_name: str):
        """
        Helper for mapping strategies to agents.
        """
        mapping = {
            "coop": AlwaysCooperate(name="Cooperative"),
            "defect": AlwaysDefect(name="Defector"),
            "random": RandomStrategy(name="Chaotic"),
            "adaptive": AdaptiveStrategy(name="Adaptive")
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

            # add contribution to the local pot
            if self.neighborhood is not None:
                self.neighborhood.add_contribution(contribution)

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
        print(f"Neighborhood: {self.neighborhood}")
        print("-"*20)

    def vote(self, sight: int = 3, social_voting: bool = False):
        nearby_agents = self.neighborhood.world.get_agents_in_range(self, sight)
        if not nearby_agents:
            return None

        use_contribution_rate = (
            social_voting and
            self.strategy.name == "Cooperative"
        )
        # either get rate or contribution itself
        def voting_value(agent):
            if use_contribution_rate:
                return agent.strategy.contribution_rate
            return agent.contribution

        voted_agent = min(
            nearby_agents,
            key=voting_value
        )
        return voted_agent


    # call after vote
    def update_strategy(self,
                        sight: int=3,
                        mutation_enabled: bool=True,
                        mutation_strength: float=0.05,
                        mutation_probability: float=1.0):

        """
        Adapt behavior based on the performance of neighboring agents.
        """

        # check if strategy is updatable
        if not hasattr(self.strategy, "update"):
            return

        # find nearby agents and update the strategy
        nearby_agents = self.neighborhood.world.get_agents_in_range(self, sight)
        self.strategy.update(nearby_agents)

        # mutate if possible
        if (mutation_enabled and
            hasattr(self.strategy, "mutate") and
            random.random() < mutation_probability):

            # add random value between -mutation_strength and
            # +mutation_strength to contribution_rate
            self.strategy.mutate(
                mutation_strength=mutation_strength
            )

