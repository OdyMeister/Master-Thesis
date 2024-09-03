import matplotlib.pyplot as plt
import numpy as np
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


def plot_distances(distances, separate):
    x = [np.mean(distances[s]) for s in distances]
    print(x)

    plt.hist(x)
    plt.xlabel("Average distances")
    plt.ylabel("Frequency")
    plt.title("Distribution of average distances per schedule")
    plt.savefig("Plots/distances per schedule.png")
    plt.show()

    plt.hist(separate)
    plt.xlabel("Distances")
    plt.ylabel("Frequency")
    plt.title("Distribution of distances")
    plt.savefig("Plots/distances.png")
    plt.show()


if __name__ == "__main__":
    plot_matchups(50)
    plot_rounds(50)
    #plot_upper_bound(50)