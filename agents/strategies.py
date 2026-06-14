from abc import ABC, abstractmethod
import random
# make the other strategies formatted like adaptive startegy

class BaseStrategy(ABC):
    """
    The Super Class for strategies. All Strategies should inherit this class.
    """

    def __init__(self, name: str, contribution_rate: float = 0.0):
        self.name = name
        self.contribution_rate = contribution_rate

    @abstractmethod
    def decide_contribution(self,
                            payoff: int | float,
                            endowment: int,
                            contribution_history: list,
                            payoff_history: list) -> int:
        """
        Every subclass MUST implement this method.
        """
        pass

    @abstractmethod
    def to_string(self):
        pass


class AlwaysCooperate(BaseStrategy):
    """
    Naive cooperation strategy.
    """
    def __init__(self, name="Cooperative"):
        super().__init__(
            name=name,
            contribution_rate=1.0
        )

    def decide_contribution(self,
                            payoff: int | float,
                            endowment: int,
                            contribution_history: list,
                            payoff_history: list) -> int:
        return endowment

    def to_string(self):
        return "AlwaysCooperate"


class AlwaysDefect(BaseStrategy):
    """
    Naive defection strategy.
    """
    def __init__(self, name="Defector"):
        super().__init__(
            name=name,
            contribution_rate=0.0
        )

    def decide_contribution(self,
                            payoff: int | float,
                            endowment: int,
                            contribution_history: list,
                            payoff_history: list) -> int:
        return 0
    def to_string(self):
        return "AlwaysDefect"


class RandomStrategy(BaseStrategy):
    """
    Random strategy.
    """
    def __init__(self, name="Chaotic"):
        super().__init__(
            name=name,
            contribution_rate=0.0
        )

    def decide_contribution(self,
                            payoff: int | float,
                            endowment: int,
                            contribution_history: list,
                            payoff_history: list) -> int:

        contribution = random.randint(0, endowment)

        if endowment > 0:
            self.contribution_rate = contribution / endowment
        else:
            self.contribution_rate = 0

        return contribution

    def to_string(self):
        return "RandomStrategy"


class AdaptiveStrategy(BaseStrategy):
    """
    Evolvable strategy.
    contribution_rate = percentage of endowment contributed.
    dont give you whole money now.
    """

    def __init__(
            self,
            name="Adaptive",
            contribution_rate=0.5,
            learning_rate=0.2):

        super().__init__(
            name=name,
            contribution_rate=contribution_rate
        )
        self.learning_rate = learning_rate

    def decide_contribution(
            self,
            payoff: int | float,
            endowment: int,
            contribution_history: list,
            payoff_history: list) -> int:

        return int(endowment * self.contribution_rate)

    def update(self, nearby_agents):
        """
        Learn from neighbours.

        Copy the contribution rate of the richest neighbour
        that is not at high risk of being voted out.
        """

        if not nearby_agents:
            return

        candidates = []

        for agent in nearby_agents:

            if not hasattr(agent.strategy, "contribution_rate"):
                continue

            # estimate kick risk
            lower_than = 0

            for other in nearby_agents:

                if other == agent:
                    continue

                if other.contribution > agent.contribution:
                    lower_than += 1

            risk = lower_than / max(1, len(nearby_agents) - 1)

            # only imitate socially safe agents
            if risk < 0.5:
                candidates.append(agent)

        if not candidates:
            return

        best_agent = max(
            candidates,
            key=lambda a: a.endowment
        )

        target_rate = best_agent.strategy.contribution_rate

        self.contribution_rate += (
            self.learning_rate *
            (target_rate - self.contribution_rate)
        )

        self.contribution_rate = max(
            0.0,
            min(1.0, self.contribution_rate)
        )

    def mutate(self, mutation_strength=0.05):

        self.contribution_rate += random.uniform(
            -mutation_strength,
            mutation_strength
        )

        self.contribution_rate = max(
            0.0,
            min(1.0, self.contribution_rate)
        )

    def to_string(self):
        return (
            f"AdaptiveStrategy("
            f"rate={self.contribution_rate:.2f})"
        )
