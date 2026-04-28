class Council:
    def __init__(self, neighborhood, threshold):
        self.neighborhood = neighborhood
        self.threshold = threshold
        self.expelled_agents = []  # list of kicked agents

    def hold_vote(self):
        votes = {}  # target_agent -> count

        # collect votes
        for agent in self.neighborhood.agents:
            target = agent.vote() #should return a neighbour after searching the perimeter
            if target is None:
                continue

            # only allow voting against neighbors
            if target in agent.neighbors:
                votes[target] = votes.get(target, 0) + 1

        # determine who gets kicked
        to_remove = []
        for agent, count in votes.items():
            if count > self.threshold:
                to_remove.append(agent)

        # remove agents
        for agent in to_remove:
            self.neighborhood.remove_agent(agent)
            self.expelled_agents.append(agent)

        return to_remove  # useful for debugging / tracking

    def accept_expelled(self):
        """
        Placeholder for logic where expelled agents
        could be re-accepted or processed further.
        """
        pass