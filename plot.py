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


def plot_diff_norm(file_path, n, plot_ID, title_add=""):
    distances = [int(dist) for dist in open(file_path, "r").read()[:-1].split(",")]
    name = file_path.split("\\")[-1].split(".")[0].split(" ")[-1]

    max_dist = calc_matchups(n) - (n//2)
    min_dist = min(distances)

    x_axis = range(min_dist, max_dist + 2)

    plt.figure(figsize=(12, 6))
    plt.hist(distances, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.axvline(x=max_dist, color='red', linestyle='--', linewidth=2, label="Max possible difference")
    plt.xticks(x_axis)
    plt.xlabel("Differences between normalized schedules")
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.legend()

    if plot_ID == 0:
        plt.title(f"Distribution of differences between {title_add}normalized schedules for n = {n}")
        plt.savefig(f"Plots/Diff-Norm_{name}.png")
    elif plot_ID == 1:
        plt.title(f"Distribution of differences between {title_add}normalized schedules for n = {n}, disregarding home/away assignments")
        plt.savefig(f"Plots/Diff-Norm-Reduced_{name}.png")
    # Special cases
    elif plot_ID == 2:
        plt.title(f"Distribution of differences between \"top 8\" normalized schedules for n = {n}")
        plt.savefig(f"Plots/Diff-Top8_{name}.png")
    elif plot_ID == 3:
        plt.title(f"Distribution of differences between \"top 8\" normalized schedules for n = {n}, disregarding home/away assignments")
        plt.savefig(f"Plots/Diff-Reduced-Top8_{name}.png")

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
    file_path = sys.argv[1]
    n = int(sys.argv[2])
    plot_ID = int(sys.argv[3])
    title_add = sys.argv[4]
    plot_diff_norm(file_path, n, plot_ID, title_add)

    # plot_uniformity_4()
    # plot_uniformity_n()

    # plot_matchups(50)
    # plot_rounds(50)
    # plot_upper_bound(50)