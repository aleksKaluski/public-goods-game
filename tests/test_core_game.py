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
    payoff, contribution, coop, n_turns = pgg.game_stas()

    # check the results
    assert sum(payoff)/n_turns == 484.00
    assert sum(contribution)/n_turns == 242
    assert statistics.mean(coop) == 1
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
    payoff, contribution, coop, n_turns = pgg.game_stas()

    assert sum(payoff)/n_turns == 0
    assert sum(contribution)/n_turns == 0
    assert statistics.mean(coop) == 0
    assert n_turns == 5


if __name__ == "__main__":
    test_1()
    test_2()