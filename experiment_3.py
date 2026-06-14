from game.public_goods_game import PublicGoodsGame

#########################################################################
"""
III Experiment: Local or global pot

How should we pay taxes? Which model is better? A global model where the whole society puts some money to the
public pot, or a framework where you contribute to your local community?
"""


# set the params of the experiment
turns = 500
width = 10
height = 10
endowment = 100
factor = 1.05
councils = True
mutation_enabled = True
show_map = True

# first condition
num_neighbourhoods = 7
strategies = {"defect": 3,
              "adaptive": 80,
              "coop": 3}

pgg = PublicGoodsGame.run_simulation(turns=turns,
                                      width=width,
                                      height=height,
                                      num_neighborhoods=num_neighbourhoods,
                                      endowment=endowment,
                                      factor=factor,
                                      strategy=strategies,
                                     councils=councils,
                                     mutation_enabled=mutation_enabled,
                                     show_map=show_map)

pgg.game_stats.plot_history(title="[EXP 3] 7 local pots", save_path=r'plots/7_local_pots.png')

# second condition
num_neighbourhoods = 1
pgg = PublicGoodsGame.run_simulation(turns=turns,
                                      width=width,
                                      height=height,
                                      num_neighborhoods=num_neighbourhoods,
                                      endowment=endowment,
                                      factor=factor,
                                      strategy=strategies,
                                     councils=councils,
                                     mutation_enabled=mutation_enabled,
                                     show_map=show_map)

pgg.game_stats.plot_history(title="[EXP 3] 1 global pot", save_path=r'plots/1_global_pot.png')
