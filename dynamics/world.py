import random
from collections import deque
from dynamics.neighborhood import Neighborhood

class World:

    def __init__(self, width, height, num_neighborhoods):

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

                if (
                    0 <= nx < self.width and
                    0 <= ny < self.height and
                    self.map[ny][nx] is None
                ):

                    self.map[ny][nx] = n_id

                    self.neighborhoods[n_id].add_coordinate(nx, ny)

                    frontier.append((nx, ny, n_id))

        # fully connected guaranteed

    def print_map(self):

        for row in self.map:

            print(" ".join(str(cell) for cell in row))

    def is_connected(self, neighborhood_id):
        """
        Debug checker:
        verifies neighborhood is one connected blob.
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

    def fill_with_agents(self, AgentClass, endowment=10, strategy="coop"):
        """
        Fills every tile with an agent.
        Each agent is placed at (x, y) and registered in its neighborhood.
        """

        agent_id = 0

        for y in range(self.height):
            for x in range(self.width):
                # choose strategy from the options randomly or not
                agent = AgentClass(
                    identifier=agent_id,
                    endowment=endowment,
                    strategy=strategy
                )

                agent.x = x
                agent.y = y

                self.grid[y][x] = agent

                # assign to neighborhood
                n_id = self.map[y][x]

                if n_id is not None:
                    self.neighborhoods[n_id].add_agent(agent)

                agent_id += 1