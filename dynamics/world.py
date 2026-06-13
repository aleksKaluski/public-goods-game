import random
from collections import deque
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

        self.expelled_agents = [] # for expelled agents obviously

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

        # keeps info who was expelled from where
        self.expelled_from = {}

        # compute neighborhoods
        self.neighborhoods = {}
        for i in range(1, num_neighborhoods + 1):
            self.neighborhoods[i] = Neighborhood(i, self)

            # avoid circularity
            from dynamics.council import Council
            self.neighborhoods[i].council = Council(self.neighborhoods[i])
        self.generate_neighborhoods()


    def to_string(self, show_neighborhood_details=False):
        """
        Prints an aligned grid where each column width matches the longest Agent ID.
        Colors symbolize neighborhoods, while agents are displayed as their IDs.
        """
        max_id_len = 1
        for row in self.grid:
            for agent in row:
                if agent is not None:
                    max_id_len = max(max_id_len, len(str(agent.identifier)))


        col_width = max_id_len + 1

        def get_color_code(n_id):
            if n_id is None: return "\033[0m"
            return f"\033[38;5;{(n_id * 40) % 230 + 1}m"

        reset = "\033[0m"
        print("\n" + "=" * (self.width * (col_width + 1)))
        for y in range(self.height):
            row_str = []
            for x in range(self.width):
                n_id = self.map[y][x]
                agent = self.grid[y][x]

                # text content
                content = str(agent.identifier) if agent is not None else "#"

                padded_content = content.ljust(col_width)
                color = get_color_code(n_id)
                row_str.append(f"{color}{padded_content}{reset}")

            print("".join(row_str))
        print("=" * (self.width * (col_width + 1)) + "\n")

        if show_neighborhood_details:
            for v in self.neighborhoods.values():
                v.to_string()


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


    def fill_with_agents(self, agents):
        #  all possible coordinates
        all_coords = [
            (x, y) for y in range(self.height)
            for x in range(self.width)
            if self.grid[y][x] is None
        ]

        # random shuffle
        random.shuffle(all_coords)

        for agent in agents:
            if not all_coords:
                print("Warning: No more room in the world for agents!")
                break

            x, y = all_coords.pop()

            # place on grid
            self.grid[y][x] = agent
            agent.x = x
            agent.y = y

            # register in neighborhood
            n_id = self.map[y][x]
            if n_id is not None:
                self.neighborhoods[n_id].add_agent(agent)
                # not necessary as function already points to the object
                # agent.neighborhood = n_id


    def get_agents_in_range(self, center_agent, sight: int):
        """
        Gets agents in range defined by sight but only if they are from the same
        neighborhood.
        """

        nearby_agents = []

        # center agent the agent that observes
        cx = center_agent.x
        cy = center_agent.y

        # compute sight range
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

        # filter by the same neighborhood
        same_neighborhood_agents = [a for a in nearby_agents if a.neighborhood == center_agent.neighborhood]

        return same_neighborhood_agents


    def remove_agent_from_grid(self, agent):
        if agent.x is not None and agent.y is not None:
            self.grid[agent.y][agent.x] = None

        agent.x = None
        agent.y = None
        agent.neighborhood = None
