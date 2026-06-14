from agents.agent import Agent
from dynamics.world import World
from game.stats import GameStatistics

class PublicGoodsGame:
    """
    A central class of the project. It is here where the game happens.
    Functionalities:
    - Initialize the game
    - Run rounds of the game
    - Save info about the hame history
    """
    def __init__(self,
                 endowment: int,
                 factor: float,
                 strategy: dict,
                 width: int = 5,
                 height: int = 5,
                 num_neighborhoods:int = 2,
                 learning_rate: float | None = None) -> None:

        # strategy is a dict of strings
        # that provides potential strategies of the agents and their number
        # {"coop" : 10, "defect" :5, "random":0} means that we have 15 agents
        # with various strategies

        # key arguments
        assert (isinstance(strategy, dict)), "Strategy must be a dict"
        assert (strategy != {}), "Strategy must not be empty!"

        self.n_agents = sum(strategy.values()) # number of agents

        # initialize various agents
        self.agents = []
        for key in strategy:
            for i in range(strategy[key]):
                agent = Agent(endowment, key)

                # strategy has lr, add it
                if (learning_rate is not None and
                    hasattr(agent.strategy, "learning_rate")):
                    agent.strategy.learning_rate = learning_rate
                self.agents.append(agent)

        self.endowment = endowment
        self.factor = factor # factor that multiplies the payoff from public pot
        self.public_goods = 0

        # initialize the world and fill it with agents
        self.world = World(width=width, height=height, num_neighborhoods=num_neighborhoods)
        self.world.fill_with_agents(agents=self.agents)

        self.number_of_turns = 1

        self.game_stats = GameStatistics(self)


    def calculate_payoffs(self, agent: Agent) -> int:
        """
        Calculates the payoff for each agent in the game and makes the agent receive it.
        As for now we make it in a naive way.
        """

        neighborhood = agent.neighborhood
        payoff = int(neighborhood.local_pot/len(neighborhood.agents))

        agent.receive_payoff(payoff)
        return payoff


    def run_council_steps(self, sight: int = 5) -> None:
        """
        Run council phases after contributions and payoffs:
        votes, acceptance.
        """
        neighborhoods = list(self.world.neighborhoods.values())

        for neighborhood in neighborhoods:
            neighborhood.council.hold_vote(
                vote_sight=sight
            )

        for neighborhood in neighborhoods:
            neighborhood.council.accept_expelled()


    def update_agent_strategies(self,
                                sight: int = 3,
                                mutation_enabled: bool = True,
                                mutation_strength: float = 0.05,
                                mutation_probability: float = 1.0) -> None:
        """
        Update strategies  of all (adaptive) agents after contributions and payoffs.
        """

        for agent in self.agents:
            if agent.neighborhood is not None:
                agent.update_strategy(
                    sight=sight,
                    mutation_enabled=mutation_enabled,
                    mutation_strength=mutation_strength,
                    mutation_probability=mutation_probability)


    def run_round(self,
                  councils: bool = False,
                  vote_sight: int = 3,
                  update_sight: int = 3,
                  mutation_enabled: bool = True,
                  mutation_strength: float = 0.05,
                  mutation_probability: float = 1.0) -> None:
        """
        Run a single round of the game:
        council votes, acceptance of expelled agents, then strategy updates.
        """
        total_cooperation_rate = 0
        agent_moves = []

        # reset public googs in each rund
        self.public_goods = 0

        # compute the local pot for each neighborhood
        for n in self.world.neighborhoods.values():
            neighborhood_contributions = 0

            for agent in n.agents:
                agent.decide_contribution()
                neighborhood_contributions += agent.contribution

            n.local_pot = neighborhood_contributions * (self.factor + 1 if self.factor < 1 else self.factor)

            self.public_goods  += n.local_pot

            for agent in n.agents:
                payoff = self.calculate_payoffs(agent)

                agent_moves.append({
                    "id": agent.identifier,
                    "payoff": payoff,
                    "contribution": agent.contribution,
                    "strategy": agent.strategy
                })

        # run council
        if councils:
            self.run_council_steps(sight=vote_sight)

        # change the strategies
        self.update_agent_strategies(sight=update_sight,
                                     mutation_enabled=mutation_enabled,
                                     mutation_strength=mutation_strength,
                                     mutation_probability=mutation_probability)

        self.number_of_turns += 1

        self.game_stats.calculate_round_stats()


    def run_turns(self,
                  turns: int,
                  councils: bool = False,
                  vote_sight: int = 3,
                  update_sight: int = 3,
                  show_stats: bool = True,
                  show_map: bool = True,
                  show_neighborhood_details: bool = False,
                  mutation_enabled: bool = True,
                  mutation_strength: float = 0.05,
                  mutation_probability: float = 1.0) -> None:
        """
        Run any number of turns and optionally print stats/map after each turn.
        """
        assert turns >= 0, "Turns must be non-negative"
        assert 0 <= mutation_probability <= 1, "Mutation probability must be between 0 and 1"

        for _ in range(turns):
            self.run_round(councils=councils,
                            vote_sight=vote_sight,
                            update_sight=update_sight,
                            mutation_enabled=mutation_enabled,
                            mutation_strength=mutation_strength,
                            mutation_probability=mutation_probability)

        if show_map:
            self.world.to_string(
                show_neighborhood_details=show_neighborhood_details
            )


    @classmethod
    def run_simulation(cls,
                        turns: int,
                        endowment: int = 10,
                        factor: float = 2,
                        strategy: dict | None = None,
                        width: int = 6,
                        height: int = 6,
                        num_neighborhoods: int = 4,
                        councils: bool = True,
                        vote_sight: int = 3,
                        update_sight: int = 3,
                        learning_rate: float | None = None,
                        show_stats: bool = True,
                        show_map: bool = True,
                        show_neighborhood_details: bool = False,
                        mutation_enabled: bool = True,
                        mutation_strength: float = 0.05,
                        mutation_probability: float = 1.0):
        """
        Create and run a game with configurable world size and turn count.
        """

        # define game rules
        game = cls(endowment=endowment,
                    factor=factor,
                    strategy=strategy,
                    width=width,
                    height=height,
                    num_neighborhoods=num_neighborhoods,
                    learning_rate=learning_rate)

        # run various turns
        game.run_turns(turns=turns,
                        councils=councils,
                        vote_sight=vote_sight,
                        update_sight=update_sight,
                        show_stats=show_stats,
                        show_map=show_map,
                        show_neighborhood_details=show_neighborhood_details,
                        mutation_enabled=mutation_enabled,
                        mutation_strength=mutation_strength,
                        mutation_probability=mutation_probability)

        return game