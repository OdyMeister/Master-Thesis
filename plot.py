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
    distances = [int(dist) for dist in open(file_path, "r").read()[:-1].split(",")]
    name = file_path.split("\\")[-1].split(".")[0].split(" ")[-1]

    max_dist = calc_matchups(n)
    min_dist = min(distances)

    x_axis = range(min_dist, max_dist)


    plt.figure(figsize=(12, 6))
    hist = plt.hist(distances, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.xticks(x_axis)
    plt.xlabel("Distances")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.title("Distribution of distances between all schedules")
    plt.savefig(f"Plots/Distances {name}.png")
    plt.show()


def plot_distances_reduced(file_path, n):
    distances = [int(dist) for dist in open(file_path, "r").read()[:-1].split(",")]
    name = file_path.split("\\")[-1].split(".")[0].split(" ")[-1]

    max_dist = calc_matchups(n)
    min_dist = min(distances)

    x_axis = range(min_dist, max_dist)

    plt.figure(figsize=(12, 6))
    hist = plt.hist(distances, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.xticks(x_axis)
    plt.xlabel("Distances")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.title("Distribution of distances between all schedules (disregarding home/away)")
    plt.savefig(f"Plots/Reduced Distances {name}.png")
    plt.show()


def plot_uniformity_4():
    freq = calc_uniformity(".\Schedules\Schedules_Random-NoNorm\Random-NoNorm-4.csv")
    freq = [freq[i] for i in freq.keys()]

    plt.figure(figsize=(16, 6))
    plt.scatter(range(0, len(freq)), freq, color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.xlabel("Schedules")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.title("Frequency of 10 million randomly generated initial schedules (n=4)")
    plt.savefig("Plots/Uniformity_n=4.png")
    plt.show()


def plot_uniformity_n():
    freq = calc_uniformity(".\Schedules\Schedules_Random-NoNorm\Random-NoNorm-6.csv")
    freq = [freq[i] for i in freq.keys()]

    max_freq = max(freq)

    x_axis = range(1, max_freq + 1)

    plt.figure(figsize=(16, 6))
    plt.hist(freq, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.yscale("log")
    plt.xlabel("Schedule frequency")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.title("Frequency of frequencies of randomly generated initial schedules (n=6)")
    plt.savefig("Plots/Uniformity_n=6.png")
    plt.show()


if __name__ == "__main__":
    # file_path = sys.argv[1]
    # n = int(sys.argv[2])
    # plot_distances(file_path, n)
    # plot_distances_reduced(file_path, n)

    # plot_uniformity_4()
    plot_uniformity_n()

    # plot_matchups(50)
    # plot_rounds(50)
    # plot_upper_bound(50)