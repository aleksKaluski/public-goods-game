"""
This file implements the institution of Council: agents cen vote in order to expel the agents that contribute too
little.
"""

from dynamics.neighborhood import Neighborhood

class Council:
    """
    Council system for neighborhood voting and expulsion. Each neighborhood has its own council that:
    - conducts votes to expel free-riders
    - accepts expelled agents
    - tracks expelled agents to prevent re-acceptance
    """
    def __init__(self, neighborhood: Neighborhood, threshold: int=5):

        # place where the voting takes place
        # (each neighborhood gets council when created)
        self.neighborhood = neighborhood

        # how many votes one needs to be expelled?
        self.threshold = threshold

        # tract who was expelled
        self.last_expelled_agents = []


    def hold_vote(self, vote_sight: int=3):
        """
        Decide which agents should be expelled. Radios of the vote = vote_sight.
        """
        self.last_expelled_agents = []
        votes = {}  # target_agent -> count

        # note on logic:
        # agent's vote() method finds the agent with minimum contribution in range, but
        # only votes for agents in the same neighborhood are counted, so
        # an agent might vote for someone outside their neighborhood, but that vote is ignored
        for agent in self.neighborhood.agents:
            # should return a neighbor after searching the perimeter
            target = agent.vote(sight=vote_sight)

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
            self.neighborhood.world.expelled_from[agent] = self.neighborhood.identifier

        self.last_expelled_agents = to_remove
        
        return to_remove  # useful for debugging / tracking


    def accept_expelled(self):
        """
        Accept expelled agents from other neighborhoods into this neighborhood.
        In this case, we expel the richest agent (eat the rich ;))
        - call this after turn 2 or something
        - don't accept the ones expelled this turn
        """
        expelled_agents = self.neighborhood.world.expelled_agents

        if not expelled_agents:
            return None

        eligible_agents = [
            agent for agent in expelled_agents
            if agent not in self.last_expelled_agents
               and self.neighborhood.world.expelled_from.get(agent) != self.neighborhood.identifier
        ]

        if not eligible_agents:
            return None

        # example: accept the richest eligible expelled agent
        candidate = max(
            eligible_agents,
            key=lambda agent: agent.endowment
        )

        # iterate through all the
        # coords in the neighbourhood and find the empty spot
        empty_coordinate = None
        for x, y in self.neighborhood.coordinates:
            if self.neighborhood.world.grid[y][x] is None:
                empty_coordinate = (x, y)
                break

        # place agent on the grid of empty coordinate
        if empty_coordinate is None:
            return None

        x, y = empty_coordinate
        self.neighborhood.world.grid[y][x] = candidate

        # modify agent's position
        candidate.x = x
        candidate.y = y

        self.neighborhood.add_agent(candidate)
        expelled_agents.remove(candidate)

        # return the accepted agent
        return candidate

    def strategy_check(self):
        """
        Update strategies for all agents in the neighborhood.
        """
        for agent in self.neighborhood.agents:
            agent.update_strategy()
