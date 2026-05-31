from game.public_goods_game import PublicGoodsGame
import pandas as pd

strategies = {"coop": 4, "defect": 4, "random": 0}
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
# pgg.world.to_string()

# hoods = pgg.world.neighborhoods
# for n in hoods.values():
#     print(n.to_string())

for i in range(5):
    pgg.run_round()

pgg.world.to_string()
pgg.game_stats()
# pgg.world.to_string_neighborhoods()


df = pd.DataFrame(pgg.history)
print(df.head(3))