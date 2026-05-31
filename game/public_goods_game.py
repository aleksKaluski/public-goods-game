from agents.agent import Agent
from dynamics.world import World


class PublicGoodsGame:
    """
    A central class of the project. It is here where the game happens.
    Functionalities:
    - Initialize the game
    - Run rounds of the game
    - Save info about the hame history
    """
    def __init__(self, endowment: int,
                 factor: float,
                 strategy: dict,
                 width: int = 0,
                 height: int = 0,
                 num_neighborhoods:int = 0,
                 local_game: bool = False) -> None:

        # strategy is a dict of strings
        # that provides potential strategies of the agents and their number
        # {"coop" : 10, "defect" :5, "random":0} means that we have 15 agents
        # with various strategies

        # key arguments
        assert (isinstance(strategy, dict)), "Strategy must be a dict"
        assert (strategy != {}), "Strategy must not be empty!"

        self.n_agents = sum(strategy.values()) # number of agents
        self.agents = []

        # initialize various agents
        for key in strategy:
            for i in range(strategy[key]): self.agents.append(Agent(endowment,
                                                                    key))

        self.local_game = local_game # decide how to compute payoffs
        self.endowment = endowment
        self.factor = factor # factor that multiplies the payoff from public pot
        self.public_goods = 0

        # initialize the world and fill it with agents
        self.world = World(width=width, height=height, num_neighborhoods=num_neighborhoods)
        self.world.fill_with_agents(agents=self.agents)

        # track history
        self.history = [] # all previous states of the game

        # game stats (fast and for testing)
        self.number_of_turns = 1


    def calculate_payoffs(self, agent: Agent) -> int:
        """
        Calculates the payoff for each agent in the game and makes the agent receive it.
        As for now we make it in a naive way.
        """

        # global pot
        if not self.local_game:
            payoff = int(self.public_goods//self.n_agents)

        # local pots
        else:
            neighborhood = agent.neighborhood
            payoff = int(neighborhood.local_pot//len(neighborhood.agents))

        agent.receive_payoff(payoff)
        return payoff


    def cooperation_rate(self, agent: Agent) -> float:
        """
        Measure cooperation as the strategy's intended contribution rate.
        """
        if hasattr(agent.strategy, "contribution_rate"):
            return agent.strategy.contribution_rate

        available_money = agent.endowment + agent.contribution

        if available_money <= 0:
            return 0

        return agent.contribution / available_money


    def run_round(
            self,
            councils: bool = False,
            mutation_enabled: bool = True,
            mutation_strength: float = 0.05,
            mutation_probability: float = 1.0) -> None:
        """
        Run a single round of the game.

        When councils is True, local games also run:
        council votes, acceptance of expelled agents, then strategy updates.
        """
        # global mode
        if not self.local_game:

            # collect contributions from all agents
            total_contributions = 0
            total_cooperation_rate = 0
            for agent in self.agents:
                agent.decide_contribution()
                # agent.to_string()

                contribution = agent.contribution
                total_contributions += contribution
                total_cooperation_rate += self.cooperation_rate(agent)

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
                              average_cooperation=total_cooperation_rate / self.n_agents,
                              average_payoff=sum(list_of_payoffs) / len(list_of_payoffs),
                              public_goods=self.public_goods,
                              agents=agent_moves)

            self.number_of_turns += 1

        # local mode
        if self.local_game:
            total_world_contributions = 0
            total_world_payoff = 0
            total_cooperation_rate = 0
            agent_moves = []

            self.public_goods = 0

            for n in self.world.neighborhoods.values():
                neighborhood_contributions = 0

                for agent in n.agents:
                    agent.decide_contribution()
                    neighborhood_contributions += agent.contribution
                    total_cooperation_rate += self.cooperation_rate(agent)

                n.local_pot = neighborhood_contributions * (self.factor + 1 if self.factor < 1 else self.factor)

                self.public_goods  += n.local_pot

                for agent in n.agents:
                    payoff = self.calculate_payoffs(agent)
                    total_world_payoff += payoff
                    total_world_contributions += agent.contribution

                    agent_moves.append({
                        "id": agent.identifier,
                        "payoff": agent.payoff,
                        "contribution": agent.contribution,
                        "strategy": agent.strategy
                    })

            self.record_round(
                round_number=self.number_of_turns,
                factor=self.factor,
                average_contribution=total_world_contributions / self.n_agents,
                average_cooperation=total_cooperation_rate / self.n_agents,
                average_payoff=total_world_payoff / self.n_agents,
                public_goods=self.public_goods,
                agents= agent_moves
            )

            if councils:
                self.run_council_steps(
                    mutation_enabled=mutation_enabled,
                    mutation_strength=mutation_strength,
                    mutation_probability=mutation_probability
                )

            self.number_of_turns += 1


    def run_council_steps(
            self,
            mutation_enabled: bool = True,
            mutation_strength: float = 0.05,
            mutation_probability: float = 1.0) -> None:
        """
        Run council phases after contributions and payoffs:
        votes, acceptance, then strategy updates.
        """
        neighborhoods = list(self.world.neighborhoods.values())

        for neighborhood in neighborhoods:
            neighborhood.council.hold_vote()

        for neighborhood in neighborhoods:
            neighborhood.council.accept_expelled()

        for agent in self.agents:
            if agent.neighborhood is not None:
                agent.update_strategy(
                    mutation_enabled=mutation_enabled,
                    mutation_strength=mutation_strength,
                    mutation_probability=mutation_probability
                )


    def run_turns(
            self,
            turns: int,
            councils: bool = False,
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
            self.run_round(
                councils=councils,
                mutation_enabled=mutation_enabled,
                mutation_strength=mutation_strength,
                mutation_probability=mutation_probability
            )

            if show_map:
                self.world.to_string(
                    show_neighborhood_details=show_neighborhood_details
                )

            if show_stats:
                self.game_stats()


    @classmethod
    def run_simulation(
            cls,
            turns: int,
            endowment: int = 10,
            factor: float = 2,
            strategy: dict | None = None,
            width: int = 6,
            height: int = 6,
            num_neighborhoods: int = 4,
            local_game: bool = True,
            councils: bool = True,
            show_stats: bool = True,
            show_map: bool = True,
            show_neighborhood_details: bool = False,
            mutation_enabled: bool = True,
            mutation_strength: float = 0.05,
            mutation_probability: float = 1.0):
        """
        Create and run a game with configurable world size and turn count.
        """
        if strategy is None:
            strategy = {"adaptive": 12}

        game = cls(
            endowment=endowment,
            factor=factor,
            strategy=strategy,
            width=width,
            height=height,
            num_neighborhoods=num_neighborhoods,
            local_game=local_game
        )

        game.run_turns(
            turns=turns,
            councils=councils,
            show_stats=show_stats,
            show_map=show_map,
            show_neighborhood_details=show_neighborhood_details,
            mutation_enabled=mutation_enabled,
            mutation_strength=mutation_strength,
            mutation_probability=mutation_probability
        )

        return game


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
        print(f"\tLocal mode: {self.local_game}")
        print(f"\tAverage contribution: {round(average_contribution, 2)}")
        print(f"\tAverage cooperation: {round(average_cooperation, 2)}")
        print(f"\tAverage payoff: {round(average_payoff, 2)}")
        print(f"\tPublic goods: {round(public_goods, 2)}")

        if self.local_game:
            print("\tNeighborhood stats:")
            for neighborhood in self.world.neighborhoods.values():
                agents = neighborhood.agents

                if not agents:
                    print(
                        f"\t\tNeighborhood {neighborhood.identifier}: "
                        "agents=0"
                    )
                    continue

                average_wealth = sum(
                    agent.endowment for agent in agents
                ) / len(agents)
                neighborhood_average_contribution = sum(
                    agent.contribution for agent in agents
                ) / len(agents)
                average_contribution_rate = sum(
                    self.cooperation_rate(agent) for agent in agents
                ) / len(agents)

                print(
                    f"\t\tNeighborhood {neighborhood.identifier}: "
                    f"agents={len(agents)}, "
                    f"wealth={round(average_wealth, 2)}, "
                    f"contribution={round(neighborhood_average_contribution, 2)}, "
                    f"contribution rate={round(average_contribution_rate, 2)}, "
                    f"local pot={round(neighborhood.local_pot, 2)}"
                )

        return average_payoff, average_contribution, average_cooperation, n_rounds

