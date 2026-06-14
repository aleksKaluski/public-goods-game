"""
This file implements some experiences that were made within PGG framework.
"""
from game.public_goods_game import PublicGoodsGame

#########################################################################
"""
I Experiment: Nash equilibrium vs simple cooperation

In order to check how our PGG framework works we will do a very simple task. Let's compare which environment will leve 
the agents better off - radical lack of cooperation, mixed cooperation or total cooperation.
"""

print(f"{15*'='} Experiment I {15*'='}")

# set the params of the experiment
turns = 100
width = 8
height = 8
num_neighbourhoods = 1
endowment = 100
factor = 1.5
councils = False
mutation_enabled = False
show_map = False

# first condition: just defectors
strategies = {"defect": 58}

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

pgg.game_stats.plot_history(title="[EXP 1] Only defectors", save_path=r'plots/plot1.png')


# second condition: 50/50 split
strategies = {"defect": 29, "coop": 29}

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

pgg.game_stats.plot_history(title="[EXP 1] 50/50 split", save_path=r'plots/plot2.png')

# third condition: just coop
strategies = {"coop": 58}

pgg = PublicGoodsGame.run_simulation(turns=turns,
                                      width=width,
                                      height=height,
                                      num_neighborhoods=num_neighbourhoods,
                                      endowment=endowment,
                                      factor=factor,
                                      strategy=strategies,
                                     councils=councils,
                                     mutation_enabled=mutation_enabled,
                                     show_map=show_map
                                     )

pgg.game_stats.plot_history(title="[EXP 1] Only cooperators", save_path=r'plots/plot3.png')

#########################################################################