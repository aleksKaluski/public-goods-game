class Neighborhood:

    def __init__(self, identifier):

        self.identifier = identifier

        self.agents = []

        self.coordinates = set()

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

    def get_agents_in_neighborhood(self):
        """
        Function that returns all agents in a given neighborhood.
        """
        return self.agents

    def to_string(self):
        """
        Prints the current state of the neighborhood.
        """
        print(f"\n\033[94mNeighborhood: {self.identifier}\033[0m")
        print(f"Agents: {[agent.identifier for agent in self.agents]}")
        print(f"Local pot: {self.local_pot}")

