from game.public_goods_game import PublicGoodsGame

strategies = {"coop": 50, "defect": 10, "random": 40}
pgg = PublicGoodsGame(endowment=10,
                      factor=2,
                      strategy=strategies,
                      width=10,
                      height=10,
                      num_neighborhoods=7)


# for agent in pgg.agents:
#     agent.to_string()

# display the state of the board
pgg.world.to_string()

# for i in range(5):
#     pgg.run_round()
# pgg.game_stats()
# print(pgg.history)