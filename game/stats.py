"""
This file is the stats center of the game. Keeps the info about all important stats of the game, neighbourhoods and
experiments.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from collections import defaultdict
import matplotlib.pyplot as plt
from typing import List, Optional


@dataclass
class NeighborhoodStats:
    """
    Statistics for a single neighborhood
    """
    neighborhood_id: int
    agent_count: int
    avg_wealth: float
    avg_contribution: float
    avg_contribution_rate: float
    total_contribution: int
    local_pot: int
    expelled_count: int


@dataclass
class GameStats:
    """
    Complete game statistics for a round
    """
    round_number: int
    global_avg_cooperation: float
    global_avg_wealth: float
    global_public_goods: int
    factor: float


class GameStatistics:
    def __init__(self, game):
        self.game = game

        # all stas of the game cumulated
        self.history = []

    def calculate_round_stats(self) -> GameStats:
        """
        Calculate all statistics for current round
        """

        # round number
        round_number = self.game.number_of_turns

        # iterate through agents
        coop_count = 0
        cumualted_wealth = 0
        for agent in self.game.agents:
            if agent.contribution_history[-1] != 0 or agent.strategy.name == "Cooperative":
                coop_count += 1

            cumualted_wealth += agent.endowment

        # % of free riders
        global_avg_cooperation = coop_count / len(self.game.agents)

        # avg wealth of an agent
        global_avg_wealth = cumualted_wealth / len(self.game.agents)

        # public pot
        global_avg_contribution = self.game.public_goods

        # factor
        factor = self.game.factor

        stats = GameStats(round_number=round_number,
                          global_avg_cooperation=global_avg_cooperation,
                          global_avg_wealth=global_avg_wealth,
                          global_public_goods=global_avg_contribution,
                          factor=factor)
        # append history
        self.history.append(stats)
        return stats


    def calculate_neighborhood_stats(self, neighborhood) -> NeighborhoodStats:
        """Calculate stats for a single neighborhood"""
        # Implementation here

    def get_cooperation_rate(self, agent) -> float:
        """Unified cooperation rate calculation"""
        # Use the same logic everywhere

    def export_to_dict(self) -> dict:
        """Export all stats as a dictionary for experiments"""
        # For easy comparison between runs

    def export_to_dataframe(self):
        """Export stats as pandas DataFrame (if pandas available)"""
        # For analysis and plotting

    ####################################################################################################################
    # Visualization created with Mistral Vibe

    def print_history(self, rounds: Optional[List[int]] = None):
        """
        Print a nicely formatted table of the game history.

        Args:
            rounds: List of specific rounds to print. If None, prints all.
        """
        if not self.history:
            print("No history available.")
            return

        # Determine which rounds to print
        if rounds is None:
            stats_to_print = self.history
        else:
            stats_to_print = [s for s in self.history if s.round_number in rounds]

        if not stats_to_print:
            print(f"No data for rounds: {rounds}")
            return

        # Print header
        print("\n" + "=" * 80)
        print(f"{'Round':<10} | {'Cooperation':<15} | {'Avg Wealth':<12} | {'Public Goods':<14} | {'Factor':<8}")
        print("-" * 80)

        # Print each round's data
        for stats in stats_to_print:
            print(f"{stats.round_number:<10} | {stats.global_avg_cooperation:<15.3f} | "
                  f"{stats.global_avg_wealth:<12.2f} | {stats.global_public_goods:<14} | "
                  f"{stats.factor:<8.2f}")

        print("=" * 80 + "\n")


    def print_summary(self):
        """
        Print a summary of the entire game history.
        """
        if not self.history:
            print("No history available.")
            return

        last = self.history[-1]
        first = self.history[0]

        print("\n" + "=" * 60)
        print("GAME SUMMARY")
        print("=" * 60)
        print(f"Total Rounds: {last.round_number}")
        print(f"Initial Cooperation: {first.global_avg_cooperation:.3f}")
        print(f"Final Cooperation: {last.global_avg_cooperation:.3f}")
        print(f"Change in Cooperation: {last.global_avg_cooperation - first.global_avg_cooperation:+.3f}")
        print(f"Initial Avg Wealth: {first.global_avg_wealth:.2f}")
        print(f"Final Avg Wealth: {last.global_avg_wealth:.2f}")
        print(f"Change in Wealth: {last.global_avg_wealth - first.global_avg_wealth:+.2f}")
        print(f"Final Public Goods: {last.global_public_goods}")
        print(f"Factor: {last.factor}")
        print("=" * 60 + "\n")

    def plot_history(self, figsize=(12, 8), save_path: Optional[str] = None, title: Optional[str] = None):
        """
        Plot the complete history with all metrics in subplots.
        """
        if not self.history:
            print("No history to plot.")
            return

        fig, axes = plt.subplots(2, 2, figsize=figsize)

        suptitle_text = title if title is not None else 'Public Goods Game Evolution'
        fig.suptitle(suptitle_text, fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.95])

        # Extract data
        rounds = [s.round_number for s in self.history]
        cooperation = [s.global_avg_cooperation for s in self.history]
        wealth = [s.global_avg_wealth for s in self.history]
        public_goods = [s.global_public_goods for s in self.history]
        factors = [s.factor for s in self.history]

        # Plot 1: Cooperation Rate
        axes[0, 0].plot(rounds, cooperation, 'b-o', markersize=4, linewidth=2)
        axes[0, 0].set_title('Cooperation Rate')
        axes[0, 0].set_xlabel('Round')
        axes[0, 0].set_ylabel('Rate')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim(0, 1)

        # Plot 2: Average Wealth
        axes[0, 1].plot(rounds, wealth, 'g-s', markersize=4, linewidth=2)
        axes[0, 1].set_title('Average Wealth')
        axes[0, 1].set_xlabel('Round')
        axes[0, 1].set_ylabel('Wealth')
        axes[0, 1].grid(True, alpha=0.3)

        # Plot 3: Public Goods
        axes[1, 0].plot(rounds, public_goods, 'r-^', markersize=4, linewidth=2)
        axes[1, 0].set_title('Public Goods')
        axes[1, 0].set_xlabel('Round')
        axes[1, 0].set_ylabel('Amount')
        axes[1, 0].grid(True, alpha=0.3)

        # Plot 4: All metrics (normalized)
        self._plot_normalized_metrics(axes[1, 1], rounds, cooperation, wealth, public_goods)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")

        plt.show()

    def _plot_normalized_metrics(self, ax, rounds, cooperation, wealth, public_goods):
        """
        Helper to plot normalized metrics on the same scale.
        """

        # Normalize each metric to [0,1]
        def normalize(values):
            if not values:
                return []
            min_val, max_val = min(values), max(values)
            if max_val == min_val:
                return [0.5] * len(values)
            return [(v - min_val) / (max_val - min_val) for v in values]

        norm_wealth = normalize(wealth)
        norm_public_goods = normalize(public_goods)

        ax.plot(rounds, cooperation, 'b-', label='Cooperation', linewidth=2)
        ax.plot(rounds, norm_wealth, 'g-', label='Wealth (norm)', linewidth=2)
        ax.plot(rounds, norm_public_goods, 'r-', label='Public Goods (norm)', linewidth=2)

        ax.set_title('All Metrics (Normalized)')
        ax.set_xlabel('Round')
        ax.set_ylabel('Normalized Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
    ####################################################################################################################


