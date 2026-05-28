from game.public_goods_game import PublicGoodsGame

strategies = {"coop": 2, "defect": 10, "random": 2}
pgg = PublicGoodsGame(endowment=10, factor=2, strategy=strategies, width=10, height=10,num_neighborhoods=3)
pgg.world.display()

# for i in range(5):
#     pgg.run_round()
# pgg.game_stats()
# print(pgg.history)