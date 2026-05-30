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
        pgg.run_global_round()
    payoff, contribution, coop, n_turns = pgg.game_stats()

    # check the results
    assert payoff == 124 # (20 + 40 + 80 + 160 + 320)/5 = 124
    assert contribution == 62  # (20 + 40 + 80 + 160)/5 = 62
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
        pgg.run_global_round()
    payoff, contribution, coop, n_turns = pgg.game_stats()

    assert payoff == 0
    assert contribution == 0
    assert coop == 0
    assert n_turns == 5


if __name__ == "__main__":
    test_1()
    test_2()