class Neighborhood:

    def __init__(self, identifier):

        self.identifier = identifier

        self.agents = []

        self.coordinates = set()

    def add_coordinate(self, x, y):

        self.coordinates.add((x, y))

    def add_agent(self, agent):

        self.agents.append(agent)

        agent.neighborhood = self

    def remove_agent(self, agent):

        if agent in self.agents:
            self.agents.remove(agent)