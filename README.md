# Public Goods Game  
This repository implements the [Public Goods Game](https://en.wikipedia.org/wiki/Public_goods_game).

**AI statement:** a local model Quen3 4B 2507 was used solely for simple grammatical correction of README file. Although 
very long, the documentation is not AI-generated slop, so please read it ;) Mistral, Gemini 2.5 flash and Clause Sonnet 4.6 
were employed to help with the implementation, but their help was mostly 
conceptual and based on code refinement, designing project structure and finding errors.  


## 1) Theoretical introduction  
### What is the Public Goods Game?  
The **Public Goods Game (PGG)** is a classic of game theoretical modelling — a framework for describing and analyzing people's behaviour, initialized by the famous book *Theory of Games and Economic Behavior* written by Morgenstern and von Neumann. Of course, the central concept of this framework is *a game* – a model of a situation which can be applied to many other situations with a similar structure. A game always has two players at minimum. Actions available to these players are called *strategies*. Based on their strategies, players receive *payoffs* that are outcomes of the game.  

Trivially speaking, there are various games and various ways of classifying them. The type of games that we are interested in are **simultaneous games with cooperation combined with agent-based modelling**. In simultaneous games, when a player makes a decision, she does not know all the factors that will determine the outcomes (e.g. behaviour of other players). If a simultaneous game is also a cooperative one, then the outcome of the game heavily relies on relations with others, since the payoff is distributed among all.  

The Public Goods Game applies this framework to model how people pay taxes, contribute to social services, etc. Thus, PGG can be described as follows: there is a number of players in the game. Each of these players starts with a certain sum of money (e.g. $20) and in each turn decides how much she would like to contribute to the public pot. The money from the pot is then multiplied by a factor (e.g. 2), divided by the number of players, and distributed equally among them. Of course, whether or not PGG describes any actual phenomenon relies on what the public good is. Intuitively, that is **a good that can be shared by many agents** (Kurz), like public transport, street lighting, or radio waves.  

### The theory behind paying taxes  
There are a few important theoretical remarks that we have to make in order to understand PGG. Our approach to PGG focuses on **agent-based modelling**. Agents are autonomous, embedded in the environment, and they interact with each other. The goal of each agent is to maximize her payoff. Of course, the best situation — speaking economically, not ethically — is the one when you do not contribute at all but still receive the payoff, since every other agent contributes.  

This leads us to the state of the game called **Nash equilibrium** — a situation when no player can unilaterally improve her outcome, since for every possible available strategy, the player will end up worse off or equally well compared to the original payoff (assuming that everyone else stays the same). Sadly, the only Nash equilibrium for public goods games is the situation when no one contributes — the best response to any contribution is to take the money and leave.  

But how is it possible that people pay taxes? We have organized a complex system of rewards and punishments. We incentivize the players to contribute, since free riding is severely punished.  

If you are interested in how we modelled all of these phenomena, please refer to the technical documentation below.

## 2) Project Structure  
This simulation is created within the Object-Oriented Programming paradigm. We believe that it is both intuitive and readable way of implementing the Public Goods Game.  

### The bird's eye view of the project  
The PGG was implemented with the following structure:  
```
├── agents # keeps agent's implementation
│   ├── __init__.py
│   ├── agent.py
│   └── strategies.py
│
├── dynamics # interactions among agents 
│   ├── __init__.py
│   ├── council.py
│   ├── neighborhood.py
│   └── world.py
│
├── game # the core of simulation
│   ├── __init__.py
│   └── public_goods_game.py
│
├── tests # tests for basic compatibility
│   ├── __init__.py
│   ├── test_core_game.py
│   └── world_test.py
│
├── experiments2.ipynb
├── main.py
├── README.md
└── requirements.txt
```

### Detailed description  
#### Folder: `agents`  
Agents are the basic elements of the game that interact with each other. Each agent is a class with a set of attributes. The most important ones are:  
* `identifier` — a unique ID of an agent  
* `endowment` — current amount of money of an agent  
* `contribution` — the amount of money that will be contributed to the public pot  
* `strategy` — the behaviour of an agent  

Agents can use various strategies. Some of them, such as `AlwaysCooperate` or `AlwaysDefect`, are self-explanatory and correspond to classical approaches outlined in Axelrod's tournaments. However, we also implemented an adaptive strategy. Since the key element of this strategy relies on other mechanisms, we will first explain other parts of the code.  

#### Folder: `dynamics`  
The folder `dynamics` keeps the vital mechanisms of the game. We now shall describe each of the most important classes.  

Consider the `world.py` as the board of this game. It is a 2D grid where the agents are placed.  
* Each agent is placed at X and Y coordinates.  
* Each grid stores its neighborhood ID.  
* Keeps the list of expelled agents.  

The world is divided into neighborhoods (`neighborhood.py`) — groups of agents that can share a common pot with local communities, depending on the parameters of the world.  
* Each neighborhood is a connected region of the world with a separate pot.  
* Neighborhoods can expel and accept agents.  

The `council.py` consists of one of these systems of rewards and punishments that we mentioned in the introduction. It is a voting system that expels free-riders from the neighborhoods.  
* Within a certain neighborhood, agents hold votes to accept or expel an agent.  
* There is a `threshold` of votes (default = 5) that must be exceeded to expel someone. It means that in small neighborhoods it might be hard to expel someone, while in large neighborhoods it is very easy.  
* Agents vote for the lowest contributor in their `vote_sight` range, however only the votes within the neighborhood count. It means that an agent can vote for someone from another neighborhood, but the vote will be ignored.  
* The council accepts the richest expelled agent (if there is a place on the board).  

#### Strategy: `AdaptiveStrategy`  
##### Basic principles  
Since we outlined the core mechanisms of the game, we can now return to the `AdaptiveStrategy`. An agent that implements it learns from its neighbors by **adjusting contribution rate**. However, since we have a built-in voting mechanism, a naive imitation would be unreasonable. The richest agents are those who never contribute anything, so they get kicked out quickly.  

Therefore, the adaptive agent computes **the risk of being voted out** for each of her neighbors — that is, the fraction of neighbors with higher contributions — and imitates only the neighbors whose risk is below 50%. Then, the agent adjusts her `contribution_rate` towards the richest neighbor with a learning rate of 0.2.  

##### Mutation  
To ensure diversity in strategies and prevent early stagnations in the game we included a mutation function. In each turn every agent mutates their contribution rate by a given mutation change (eg. 50%). Then the mutations occur in either towards less or mor contribution given by a mutation rate (eg. %10).  

## 3) Quick Start  
You can run a mock game by using `python main.py`. You can edit the given varibales to see what kind of results you can achieve.

# Configuration

|                             |                                 |                                                                       |
| --------------------------- | ------------------------------- | --------------------------------------------------------------------- |
| `TURNS`                     | `200`                           | Total number of turns in the simulation.                              |
| `WIDTH`                     | `10`                            | Width of the map.                                                     |
| `HEIGHT`                    | `10`                            | Height of the map.                                                    |
| `NUM_NEIGHBORHOODS`         | `4`                             | Number of neighborhoods on the map.                                   |
| `ENDOWMENT`                 | `20`                            | Initial wealth assigned to each agent.                                |
| `FACTOR`                    | `2`                             | Multiplier applied to the public pool before redistribution.          |
| `STRATEGIES`                | `{"adaptive": 80, "coop": 100}` | Initial number of agents using each strategy.                         |
| `SHOW_NEIGHBORHOOD_DETAILS` | `False`                         | Print neighborhood statistics after each round.                       |
| `MUTATION_ENABLED`          | `True`                          | Enable evolutionary mutations.                                        |
| `MUTATION_STRENGTH`         | `0.1`                           | Magnitude of change introduced by mutation.                           |
| `MUTATION_PROBABILITY`      | `0.5`                           | Probability that an agent mutates.                                    |
| `VOTE_SIGHT`                | `3`                             | Maximum distance an agent can inspect others while voting.            |
| `UPDATE_SIGHT`              | `3`                             | Maximum distance an adaptive agent can inspect others while learning. |
| `LEARNING_RATE`             | `0.2`                           | Learning rate used when updating the adaptive strategy.               |


## 4) Experiments
