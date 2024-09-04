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


def plot_distances(file_path, n):
    distances = calc_distance(file_path, n)
    name = file_path.split("\\")[-1].split(".")[0]

    max_dist = calc_matchups(n)
    min_dist = 2

    x_axis = range(min_dist, max_dist)

    plt.hist(distances, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.xticks(x_axis)
    plt.xlabel("Distances")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.title("Distribution of distances between all schedules")
    plt.savefig(f"Plots/Distribution of distances {name}.png")
    plt.show()


def plot_distances_reduced(file_path, n):
    distances = calc_distance_reduced(file_path, n)
    name = file_path.split("\\")[-1].split(".")[0]

    max_dist = calc_matchups(n) + 1
    min_dist = 0

    x_axis = range(min_dist, max_dist)

    plt.hist(distances, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.xticks(x_axis)
    plt.xlabel("Distances")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.title("Distribution of distances between all schedules (disregarding home/away)")
    plt.savefig(f"Plots/Distribution of distances for reduced schedueles {name}.png")
    plt.show()


if __name__ == "__main__":
    file_path = sys.argv[1]
    n = int(sys.argv[2])

    # plot_distances(file_path, n)
    plot_distances_reduced(file_path, n)

    # plot_matchups(50)
    # plot_rounds(50)
    # plot_upper_bound(50)