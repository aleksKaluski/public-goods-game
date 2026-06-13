"""
This file implements the neigbourhood: a subset of the world
that can compute the payoffs locally.
"""

# from dynamics.council import Council

class Neighborhood:

    def __init__(self, identifier, world):

        self.identifier = identifier
        self.world = world
        self.agents = []
        self.coordinates = set()
        self.council = None

        # current amount of money
        # within one neighborhood
        self.local_pot = 0

    def add_coordinate(self, x, y):
        self.coordinates.add((x, y))

    def add_agent(self, agent):
        self.agents.append(agent)
        agent.neighborhood = self

    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)
            self.world.remove_agent_from_grid(agent)

    def reset_local_pot(self):
        """
        Reset the local pot at the start of a new round.
        """
        self.local_pot = 0

    def add_contribution(self, amount: int):
        """
        Add an agent's contribution to the local pot.
        """
        self.local_pot += amount


    def to_string(self, color_code="\033[94m"):
        """
        Prints the current state of the neighborhood.
        """
        print(f"\n{color_code}Neighborhood: {self.identifier}\033[0m")
        print(f"{color_code}Agents: {[(agent.identifier, agent.strategy.to_string())for agent in self.agents]}\033[0m")
        print(f"{color_code}Local pot: {self.local_pot}\033[0m")

