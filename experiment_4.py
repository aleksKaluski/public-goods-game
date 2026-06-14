"""
Experiment 3: raw contribution voting vs social contribution-rate voting.
"""
from game.public_goods_game import PublicGoodsGame

print(f"{15*'='} Experiment IV {15*'='}")

# set the params of the experiment
turns = 500
width = 8
height = 8
num_neighbourhoods = 3
endowment = 100
factor = 1.1
councils = True
mutation_enabled = True
show_map = False

# mixed condition: cooperators can punish by money amount or by contribution rate
strategies = {
    "coop": 20,
    "defect": 20,
    "adaptive": 24
}

pgg = PublicGoodsGame.run_simulation(
    turns=turns,
    width=width,
    height=height,
    num_neighborhoods=num_neighbourhoods,
    endowment=endowment,
    factor=factor,
    strategy=strategies,
    councils=councils,
    mutation_enabled=mutation_enabled,
    show_map=show_map,
    social_voting=False
)

pgg.game_stats.plot_history(
    title="[EXP 4] Raw contribution voting",
    save_path=r"plots/plot_exp4_raw.png"
)

pgg = PublicGoodsGame.run_simulation(
    turns=turns,
    width=width,
    height=height,
    num_neighborhoods=num_neighbourhoods,
    endowment=endowment,
    factor=factor,
    strategy=strategies,
    councils=councils,
    mutation_enabled=mutation_enabled,
    show_map=show_map,
    social_voting=True
)

pgg.game_stats.plot_history(
    title="[EXP 4] Social contribution-rate voting",
    save_path=r"plots/plot_exp4_social.png"
)
