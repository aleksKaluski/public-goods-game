# Public Goods Game
This repo implements the [Public Goods Game](https://en.wikipedia.org/wiki/Public_goods_game) (PGG) - a well-know model 
f everyday situations (e.g. paying taxes) described by the language of the game theory. The goal of the repo is to 
provide a set of tools for running scientific  experiments. 

## Project Structure
```pycon
public_goods_game/
├── main.py                 # Entry point: run simulations, collect results
├── config.py               # Game parameters (endowment, factor, rounds, etc.)
├── agents/
│   ├── __init__.py
│   ├── agent.py            # Base Agent class
│   ├── strategies.py       # Strategy implementations (Cooperate, Defect, TitForTat, etc.)
│   └── memory.py           # Optional: track agent history, past interactions
├── game/
│   ├── __init__.py
│   ├── public_goods_game.py  # Core PGG logic: contribution, payoff calculation
│   └── payoff.py            # Payoff computation (global vs local)
├── network/
│   ├── __init__.py
│   ├── graph.py             # Agent population as graph structure
│   └── topology.py          # Graph layouts, neighbor queries
├── dynamics/
│   ├── __init__.py
│   ├── strategy_update.py   # How agents update strategies based on payoffs
│   ├── voting.py            # Voting/exclusion mechanism
│   └── learning.py          # Imitation, best-response, etc.
├── simulation/
│   ├── __init__.py
│   └── simulator.py         # Main loop: run rounds, aggregate results
├── analysis/
│   ├── __init__.py
│   ├── metrics.py           # Calculate cooperation rate, Gini, efficiency
│   └── statistics.py        # Aggregate statistics across runs
├── visualization/
│   ├── __init__.py
│   ├── plot.py              # Graph rendering, heatmaps
│   └── animate.py           # Animation over rounds
└── tests/
    ├── __init__.py
    ├── test_payoff.py
    ├── test_strategies.py
    └── test_simulator.py
```