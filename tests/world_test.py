import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from dynamics.world import World

world = World(
    width=20,
    height=20,
    num_neighborhoods=5
)

world.to_string()