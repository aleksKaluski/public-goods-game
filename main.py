from game.public_goods_game import PublicGoodsGame

strategies = {"coop": 2, "defect": 5, "random": 2}
pgg = PublicGoodsGame(endowment=10, factor=0.5, strategy=strategies)
pgg.run_round()
pgg.game_stas()