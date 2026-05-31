class Council:
    def __init__(self, neighborhood, threshold):
        self.neighborhood = neighborhood
        self.threshold = threshold

    def hold_vote(self):
        votes = {}  # target_agent -> count

        # collect votes
        for agent in self.neighborhood.agents:
            target = agent.vote() # should return a neighbour after searching the perimeter
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
            self.neighborhood.world.expelled_agents.append(agent)
        
        self.strategy_check() # make update strategy calls for all agents 

        return to_remove  # useful for debugging / tracking

    #call this after turn 2 or something
    def accept_expelled(self):
        expelled_agents = self.neighborhood.world.expelled_agents

        if not expelled_agents:
            return None

        # example: accept richest expelled agent
        candidate = max(
            expelled_agents,
            key=lambda agent: agent.endowment
        )

        self.neighborhood.add_agent(candidate)
        expelled_agents.remove(candidate)

        return candidate

    def strategy_check(self):
        for agent in self.neighborhood.agents:
            agent.update_strategy()