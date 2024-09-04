import matplotlib.pyplot as plt
import numpy as np
import sys
from calc import *


def plot_matchups(max):
    x = range(0, max + 1, 2)
    y = [calc_matchups(n) for n in x]

    plt.plot(x, y)
    plt.xlabel("Teams")
    plt.ylabel("Matchups")
    plt.grid(alpha=0.5)
    plt.title("Number of possible matchups given n teams")
    plt.savefig("Plots/matchups.png")
    plt.show()

def plot_rounds(max):
    x = range(0, max + 1, 2)
    y = [calc_rounds(n) for n in x]

    plt.plot(x, y)
    plt.xlabel("Teams")
    plt.ylabel("Rounds")
    plt.grid(alpha=0.5)
    plt.yscale("log")
    plt.title("Number of possible rounds given n teams")
    plt.savefig("Plots/rounds.png")
    plt.show()

def plot_upper_bound(max):
    x = range(0, max + 1, 2)
    y = [calc_drr_schedules(n) for n in x]

    plt.plot(x, y)
    plt.xlabel("Teams")
    plt.ylabel("Schedules")
    plt.grid(alpha=0.5)
    plt.yscale("log")
    plt.title("Upper bound of possible schedules given n teams")
    plt.savefig("Plots/upper_bound.png")
    plt.show()


def plot_distances(file_path,n):
    distances, separate = calc_distance(file_path, n)
    name = file_path.split("\\")[-1].split(".")[0]

    # x = [np.mean(distances[s]) for s in distances]

    # plt.hist(x)
    # plt.xlabel("Average distances")
    # plt.ylabel("Frequency")
    # plt.title("Distribution of average distances per schedule")
    # plt.savefig(f"Plots/Mean dist per schedule {name}.png")
    # plt.show()

    max_dist = max([max(distances[s]) for s in distances]) + 2
    min_dist = min([min(distances[s]) for s in distances])
    x_axis = range(min_dist, max_dist)

    plt.hist(separate, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.xticks(x_axis)
    plt.xlabel("Distances")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.title("Distribution of distances")
    plt.savefig(f"Plots/General distribution of distances {name}.png")
    plt.show()


if __name__ == "__main__":
    file_path = sys.argv[1]
    n = int(sys.argv[2])
    plot_distances(file_path, n)

    # plot_matchups(50)
    # plot_rounds(50)
    # plot_upper_bound(50)