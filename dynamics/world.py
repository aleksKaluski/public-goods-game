import random
from collections import deque

from agents.agent import Agent
from dynamics.neighborhood import Neighborhood

class World:
    """
    A class that keeps the topology of the game, meaning the location of agents and
    their neighborhoods.
    """
    def __init__(self, width:int, height: int, num_neighborhoods: int):

        self.width = width
        self.height = height
        self.num_neighborhoods = num_neighborhoods

        # agents grid
        self.grid = [
            [None for _ in range(width)]
            for _ in range(height)
        ]

        # neighborhood map
        self.map = [
            [None for _ in range(width)]
            for _ in range(height)
        ]

        self.neighborhoods = {}

        for i in range(1, num_neighborhoods + 1):
            self.neighborhoods[i] = Neighborhood(i)

        self.generate_neighborhoods()

    def generate_neighborhoods(self):
        """
        Generates connected blob-like neighborhoods.
        """

        # ---------------------------------------------------
        # STEP 1:
        # randomly place one seed for each neighborhood
        # ---------------------------------------------------

        seeds = []

        used = set()

        for n_id in range(1, self.num_neighborhoods + 1):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)

                if (x, y) not in used:
                    used.add((x, y))
                    self.map[y][x] = n_id
                    self.neighborhoods[n_id].add_coordinate(x, y)
                    seeds.append((x, y, n_id))
                    break

        # ---------------------------------------------------
        # STEP 2:
        # grow blobs outward
        # ---------------------------------------------------

        frontier = deque(seeds)

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        while frontier:

            x, y, n_id = frontier.popleft()

            random.shuffle(directions)

            for dx, dy in directions:

                nx = x + dx
                ny = y + dy

                if (0 <= nx < self.width and
                    0 <= ny < self.height and
                    self.map[ny][nx] is None):

                    self.map[ny][nx] = n_id

                    self.neighborhoods[n_id].add_coordinate(nx, ny)

                    frontier.append((nx, ny, n_id))


    def to_string(self):
        for row in self.map:
            print(" ".join(str(cell) for cell in row))

    def is_connected(self, neighborhood_id):
        """
        Debug checker: verifies neighborhood is one connected blob.
        """

        coords = self.neighborhoods[
            neighborhood_id
        ].coordinates

        if not coords:
            return True

        start = next(iter(coords))

        visited = set([start])

        queue = deque([start])

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        while queue:

            x, y = queue.popleft()

            for dx, dy in directions:

                nx = x + dx
                ny = y + dy

                if (
                    (nx, ny) in coords and
                    (nx, ny) not in visited
                ):

                    visited.add((nx, ny))

                    queue.append((nx, ny))

        return len(visited) == len(coords)


    def fill_with_agents(self, agents: list[Agent]):
        """
        Fills every tile with an agent. Each agent is placed at (x, y) and registered in its neighborhood.
         The agents are provided with the list and randomly placed in the neighborhood.
        """

        for agent in agents:
            i = 0
            # sample as long as we won't find a free position
            while True:
                y = random.randrange(len(self.grid))
                x = random.randrange(len(self.grid[0]))

                if self.grid[y][x] is None:
                    self.grid[y][x] = agent

                    # assign agent to the neighborhood
                    n_id = self.map[y][x]
                    if n_id is not None:
                        self.neighborhoods[n_id].add_agent(agent)
                    break

                # avoid infinite loops
                if i > 10:
                    break

    def get_agents_in_range(self, center_agent, sight):

        nearby_agents = []

        cx = center_agent.x
        cy = center_agent.y

        min_x = max(0, cx - sight)
        max_x = min(self.width - 1, cx + sight)

        min_y = max(0, cy - sight)
        max_y = min(self.height - 1, cy + sight)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):

                agent = self.grid[y][x]

                if agent is None:
                    continue

                if agent == center_agent:
                    continue

                nearby_agents.append(agent)

        return nearby_agents