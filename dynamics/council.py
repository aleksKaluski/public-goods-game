class Council:
    def __init__(self, neighborhood, threshold=0):
        self.neighborhood = neighborhood
        self.threshold = threshold

    def hold_vote(self):
        votes = {}  # target_agent -> count

        # collect votes
        for agent in self.neighborhood.agents:
            target = agent.vote() # should return a neighbour after searching the perimeter
            if target is None:
                continue

            # only allow voting against agents represented by this council
            if target in self.neighborhood.agents:
                votes[target] = votes.get(target, 0) + 1

        # determine who gets kicked
        to_remove = []
        if votes:
            agent, count = max(
                votes.items(),
                key=lambda vote: vote[1]
            )

            if count > self.threshold:
                to_remove.append(agent)

        # remove agents
        for agent in to_remove:
            self.neighborhood.remove_agent(agent)
            self.neighborhood.world.expelled_agents.append(agent)
        
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

        empty_coordinate = None
        for x, y in self.neighborhood.coordinates:
            if self.neighborhood.world.grid[y][x] is None:
                empty_coordinate = (x, y)
                break

        if empty_coordinate is None:
            return None

        x, y = empty_coordinate
        self.neighborhood.world.grid[y][x] = candidate
        candidate.x = x
        candidate.y = y
        self.neighborhood.add_agent(candidate)
        expelled_agents.remove(candidate)

        return candidate

    def strategy_check(self):
        for agent in self.neighborhood.agents:
            agent.update_strategy()
