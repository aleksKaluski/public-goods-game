from game.public_goods_game import PublicGoodsGame


def test_1():
    pgg = PublicGoodsGame(n_agents=5, endowment=20)


    for i in range(5):
        pgg.run_round()