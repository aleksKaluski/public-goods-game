from game.public_goods_game import PublicGoodsGame

TURNS = 10
WIDTH = 6
HEIGHT = 6
NUM_NEIGHBORHOODS = 4
ENDOWMENT = 20
FACTOR = 2
STRATEGIES = {"adaptive": 8, "coop": 8, "defect": 6}
SHOW_NEIGHBORHOOD_DETAILS = False
MUTATION_ENABLED = True
MUTATION_STRENGTH = 0.1
MUTATION_PROBABILITY = 0.5
VOTE_SIGHT = 3
UPDATE_SIGHT = 3
LEARNING_RATE = 0.2

pgg = PublicGoodsGame.run_simulation(
                                    turns=TURNS,
                                    endowment=ENDOWMENT,
                                    factor=FACTOR,
                                    strategy=STRATEGIES,
                                    width=WIDTH,
                                    height=HEIGHT,
                                    num_neighborhoods=NUM_NEIGHBORHOODS,
                                    councils=True,
                                    vote_sight=VOTE_SIGHT,
                                    update_sight=UPDATE_SIGHT,
                                    learning_rate=LEARNING_RATE,
                                    show_stats=True,
                                    show_map=True,
                                    show_neighborhood_details=SHOW_NEIGHBORHOOD_DETAILS,
                                    mutation_enabled=MUTATION_ENABLED,
                                    mutation_strength=MUTATION_STRENGTH,
                                    mutation_probability=MUTATION_PROBABILITY
)


# for agent in pgg.agents:
#     agent.to_string()

# display the state of the board
# pgg.world.to_string()

# hoods = pgg.world.neighborhoods
# for n in hoods.values():
#     print(n.to_string())

# pgg.world.to_string_neighborhoods()
