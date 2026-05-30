from game.public_goods_game import PublicGoodsGame

strategies = {"coop": 4, "defect": 4, "random": 4}
pgg = PublicGoodsGame(endowment=10,
                      factor=2,
                      strategy=strategies,
                      width=4,
                      height=4,
                      num_neighborhoods=7,
                      local_game=True)


# for agent in pgg.agents:
#     agent.to_string()

# display the state of the board
pgg.world.to_string()

# hoods = pgg.world.neighborhoods
# for n in hoods.values():
#     print(n.to_string())

for i in range(5):
    pgg.run_round()
# pgg.game_stats()
# print(pgg.history)