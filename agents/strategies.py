from abc import ABC, abstractmethod
import random


class BaseStrategy(ABC):
    """
    The Super Class for strategies. All Strategies should inherit this class.
    """

    def __init__(self, name: str):
        self.name = name

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
    def decide_contribution(self,
                            payoff: int | float,
                            endowment: int,
                            contribution_history: list,
                            payoff_history: list) -> int:

        return random.randint(0, endowment)

    def to_string(self):
        return "RandomStrategy"