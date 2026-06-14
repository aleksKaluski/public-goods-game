from game.public_goods_game import PublicGoodsGame
import statistics

def test_1():
    """
    Test performance of 5 agents with full contribution in
    5 rounds.
    """
    strategies = {"coop": 5}
    pgg = PublicGoodsGame(endowment=10, factor=2, strategy=strategies)

    for i in range(5):
        pgg.run_round()
    coop, n_turns = pgg.game_stats()

    # check the results
    assert coop == 1
    assert n_turns == 5

def test_2():
    """
    Test performance of 5 agents with 0 contribution in
    5 rounds.
    """
    strategies = {"defect": 5}
    pgg = PublicGoodsGame(endowment=10, factor=2, strategy=strategies)

    for i in range(5):
        pgg.run_round()
    coop, n_turns = pgg.game_stats()

    assert coop == 0
    assert n_turns == 5


if __name__ == "__main__":
    test_1()
    test_2()