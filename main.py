from game.public_goods_game import PublicGoodsGame

strategies = {"coop": 2, "defect": 5, "random": 2}
pgg = PublicGoodsGame(endowment=10, factor=2, strategy=strategies)



for i in range(5):
    pgg.run_round()
pgg.game_stats()
print(pgg.history)