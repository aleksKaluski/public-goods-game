from game.public_goods_game import PublicGoodsGame

# set the params of the experiment
turns = 500
width = 8
height = 8
num_neighbourhoods = 1
endowment = 100
factor = 1.1
councils = True
mutation_enabled = True
show_map = True

# first condition: just defectors
strategies = {"defect": 4,
              "adaptive": 60}

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

pgg.game_stats.plot_history(title="[EXP 1] Only defectors", save_path=r'plots/plot4.png')
