import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, lognorm
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

def plot_diff_norm(file_path, n, plot_ID, title_add="", show=False):
    differences = [int(diff) for diff in open(file_path, "r").read()[:-1].split(",")]
    name = file_path.split("\\")[-1].split(".")[0].split(" ")[-1]
    fontsize = 18

    if name == "":
        name = title_add + " " + str(n)

    # Plot type 2 is based on home/away assignments
    # The max difference is 2 * (n-1) * n - n
    # since the maximum difference is 2 * (n-1) * n and the first round is fixed
    if plot_ID == 2:
        max_diff = 2 * (n-1) * n - n
    # The max difference is the number of matchups - n//2
    # since the first round is fixed and there are n//2 matchups in each round
    else:
        max_diff = calc_matchups(n) - (n//2)
    min_diff = min(differences)
    mean_diff = np.mean(differences)
    std_diff = np.std(differences)

    x_axis = range(min_diff, max_diff + 2)

    # Create the plot and histogram
    fig, ax = plt.figure(figsize=(12, 6))
    freqs, _, _ = plt.hist(differences, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)

    # Add vertical lines for the max difference
    plt.axvline(x=max_diff, color='red', linestyle='--', linewidth=2, label="Max. possible difference")

    # Plot a curve to match the distribution of the differences
    if plot_ID < 3 and (plot_ID != 1 or n > 4):
        x_axis_curve = np.linspace(min_diff, max_diff, 1000)

        # curve = fit_curve(x_axis, freqs)
        # plt.plot(x_axis_curve, curve(x_axis_curve), color='black', linestyle='-', linewidth=2, label="Fitted curve")

        pdf_fitted = norm.pdf(x_axis_curve, mean_diff, std_diff)
        plt.plot(x_axis_curve, pdf_fitted * max(freqs) * (1 / max(pdf_fitted)), color='black', linestyle='-', linewidth=2, label="Normal dist. curve")

        # shape, loc, scale = lognorm.fit(differences)
        # pdf_fitted = lognorm.pdf(x_axis_curve, shape, loc, scale)
        # plt.plot(x_axis_curve, pdf_fitted * max(freqs) * (1 / max(pdf_fitted)), color='black', linestyle='-', linewidth=2, label="Lognormal dist.  curve")

        plt.axvline(x=mean_diff, color='blue', linestyle='--', linewidth=2, label=f"Mean difference: {mean_diff:.2f}")
        plt.axvline(x=(mean_diff - std_diff), color='green', linestyle='--', linewidth=2, label=f"Std of difference: {std_diff:.2f}")
        plt.axvline(x=(mean_diff + std_diff), color='green', linestyle='--', linewidth=2)

    # Code to only show every other x value
    # Checks to make sure the last value is the max difference
    x_values = x_axis[::2]
    if x_values[-1] != max_diff:
        x_values[-1] = max_diff

    # Set the labels and title
    plt.xticks(x_values)
    plt.xlabel("Differences between normalized schedules", fontsize=fontsize)
    plt.ylabel("Frequency", fontsize=fontsize)
    plt.grid(alpha=0.5)
    plt.legend(loc='upper left', bbox_to_anchor=(0,1))

    # Depending on the plot type, save the plot with a different name
    # Type 0 is jsut for the differences
    # Type 1 is for the differences disregarding home/away assignments
    # Type 2 is for the differences only considering home/away assignments
    # Type 3 is for the differences of the top 8 teams
    # Type 4 is for the differences of the top 8 teams disregarding home/away assignments
    # Type 5 is for the differences of the top 8 teams only considering home/away assignments
    if plot_ID == 0:
        plt.savefig(f"Plots/no_title/Diff-Norm_{name}.png", bbox_inches='tight')
        plt.title(f"Distribution of differences for {title_add}normalized schedules for n = {n}", fontsize=fontsize)
        plt.savefig(f"Plots/Diff-Norm_{name}.png", bbox_inches='tight')
    elif plot_ID == 1:
        plt.savefig(f"Plots/no_title/Diff-Norm-Reduced_{name}.png", bbox_inches='tight')
        plt.title(f"Distribution of differences for {title_add}normalized schedules for n = {n}\nDisregarding home/away assignments", fontsize=fontsize)
        plt.savefig(f"Plots/Diff-Norm-Reduced_{name}.png", bbox_inches='tight')
    elif plot_ID == 2:
        plt.legend(loc='upper left', bbox_to_anchor=(0.75,1))
        plt.savefig(f"Plots/no_title/Diff-Norm-Teamlesss_{name}.png", bbox_inches='tight')
        plt.title(f"Distribution of differences for {title_add}normalized schedules for n = {n}\nOnly considering home/away assignments", fontsize=fontsize)
        plt.savefig(f"Plots/Diff-Norm-Teamlesss_{name}.png", bbox_inches='tight')
    # Special cases
    elif plot_ID == 3:
        plt.savefig(f"Plots/no_title/Diff-Top8_{name}.png", bbox_inches='tight')
        plt.title(f"Distribution of differences for \"top 8\" normalized schedules for n = {n}", fontsize=fontsize)
        plt.savefig(f"Plots/Diff-Top8_{name}.png", bbox_inches='tight')
    elif plot_ID == 4:
        plt.savefig(f"Plots/no_title/Diff-Reduced-Top8_{name}.png", bbox_inches='tight')
        plt.title(f"Distribution of differences for \"top 8\" normalized schedules for n = {n}\nDisregarding home/away assignments", fontsize=fontsize)
        plt.savefig(f"Plots/Diff-Reduced-Top8_{name}.png", bbox_inches='tight')
    elif plot_ID == 5:
        plt.savefig(f"Plots/no_title/Diff-Teamless-Top8_{name}.png", bbox_inches='tight')
        plt.title(f"Distribution of differences for \"top 8\" normalized schedules for n = {n}\nOnly considering home/away assignments", fontsize=fontsize)
        plt.savefig(f"Plots/Diff-Teamless-Top8_{name}.png", bbox_inches='tight')
    if show:
        plt.show()

def plot_uniformity_4(show=False):
    freq = calc_uniformity("./Schedules/Schedules_Random-10m/Random-4.csv")
    freq = [freq[i] for i in freq.keys()]

    fontsize = 18

    plt.figure(figsize=(16, 6))
    plt.scatter(range(160), freq, color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.xlabel("Schedules", fontsize=fontsize)
    plt.ylabel("Frequency", fontsize=fontsize)
    plt.grid(alpha=0.5)
    plt.savefig("Plots/no_title/Uniformity_n=4.png", bbox_inches='tight')
    plt.title("Frequency of 10 million randomly generated initial schedules (n=4)", fontsize=fontsize)
    plt.savefig("Plots/Uniformity_n=4.png", bbox_inches='tight')
    if show:
        plt.show()

def plot_uniformity_sorted_4(show=False):
    freq = calc_uniformity("./Schedules/Schedules_Random-10m/Random-4.csv")
    freq = sorted([freq[i] for i in freq.keys()], reverse=True)

    fontsize = 18

    plt.figure(figsize=(16, 6))
    plt.bar(range(160), freq, color='orange', alpha=0.9, edgecolor='black', linewidth=1, width=1.1)
    plt.xlabel("Schedules", fontsize=fontsize)
    plt.ylabel("Frequency", fontsize=fontsize)
    plt.grid(alpha=0.5)
    plt.savefig("Plots/no_title/Uniformity_sorted_10M_n=4.png", bbox_inches='tight')
    plt.title("Sorted frequency of 10 million randomly generated schedules for n=4", fontsize=fontsize)
    plt.savefig("Plots/Uniformity_sorted_10M_n=4.png", bbox_inches='tight')
    if show:
        plt.show()

def plot_uniformity_sampler_4(show=False):
    freq = calc_uniformity("./Schedules/Sampler/4.csv")
    freq = [freq[i] for i in freq.keys()]

    fontsize = 18

    plt.figure(figsize=(16, 6))
    plt.scatter(range(160), freq, color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    plt.xlabel("Schedules", fontsize=fontsize)
    plt.ylabel("Frequency", fontsize=fontsize)
    plt.grid(alpha=0.5)
    plt.savefig("Plots/no_title/Uniformity_sampler_n=4.png", bbox_inches='tight')
    plt.title("Frequency of 10 million randomly sampled initial schedules for n=4", fontsize=fontsize)
    plt.savefig("Plots/Uniformity_sampler_n=4.png", bbox_inches='tight')
    if show:
        plt.show()

def plot_uniformity_sampler_sorted_4(show=False):
    freq = calc_uniformity("./Schedules/Sampler/4.csv")
    freq = sorted([freq[i] for i in freq.keys()], reverse=True)

    fontsize = 18

    plt.figure(figsize=(16, 6))
    plt.bar(range(160), freq, color='orange', alpha=0.9, edgecolor='black', linewidth=1, width=1.1)
    plt.xlabel("Schedules", fontsize=fontsize)
    plt.ylabel("Frequency", fontsize=fontsize)
    plt.grid(alpha=0.5)
    plt.savefig("Plots/no_title/Uniformity_sampler_sorted_10M_n=4.png", bbox_inches='tight')
    plt.title("Sorted frequency of 10 million randomly sampled schedules for n=4", fontsize=fontsize)
    plt.savefig("Plots/Uniformity_sampler_sorted_10M_n=4.png", bbox_inches='tight')
    if show:
        plt.show()


if __name__ == "__main__":
    plots = [
        ("./Distances/Distances All-4.csv", 4, 0, "all "),
        ("./Distances/Distances Reduced All-4.csv", 4, 1, "all "),
        ("./Distances/Distances Teamless All-4.csv", 4, 2, "all "),

        ("./Distances/Distances Top-8 n=4.csv", 4, 3, "top 8 "),
        ("./Distances/Distances Reduced Top-8 n=4.csv", 4, 4, "top 8 "),
        ("./Distances/Distances Teamless Top-8 n=4.csv", 4, 5, "top 8 "),

        ("./Distances/Distances Uniform-6.csv", 6, 0, "10k uniformly random "),
        ("./Distances/Distances Reduced Uniform-6.csv", 6, 1, "10k uniformly random "),
        ("./Distances/Distances Teamless Uniform-6.csv", 6, 2, "10k uniformly random "),

        ("./Distances/Distances Random-10k-8.csv", 8, 0, "10k random "),
        ("./Distances/Distances Reduced Random-10k-8.csv", 8, 1, "10k random "),
        ("./Distances/Distances Teamless Random-10k-8.csv", 8, 2, "10k random ")

        # ("./Distances/Distances Random-10k-10.csv", 10, 0, "10k random "),
        # ("./Distances/Distances Reduced Random-10k-10.csv", 10, 1, "10k random "),
        # ("./Distances/Distances Teamless Random-10k-10.csv", 10, 2, "10k random ")
    ]

    for plot in plots[0:1]:
        file_path, n, plot_ID, title_add = plot
        plot_diff_norm(file_path, n, plot_ID, title_add, True)

    # plot_uniformity_4()
    # plot_uniformity_sorted_4()
    # plot_uniformity_sampler_4()
    # plot_uniformity_sampler_sorted_4()

    # plot_matchups(50)
    # plot_rounds(50)
    # plot_upper_bound(50)