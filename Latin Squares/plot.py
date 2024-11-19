import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Plot the histogram of the frequency of violations for randomly generated Latin Squares
def plot_histogram(n, violations, power, mean_diff, std_diff, show=False):
    # Initialize x axis and amount string for the title
    x = range(min(violations), max(violations) + 1)
    amount = "10^" + str(power)

    # Fit a normal distribution curve with more points for a smoother curve
    x_norm = np.linspace(min(violations), max(violations), 1000)
    pdf_fitted = norm.pdf(x_norm, mean_diff, std_diff)
    
    # Plots the histogram of the frequency of violations
    fig, ax1 = plt.subplots(figsize=(10, 6))
    freqs, _, _ = ax1.hist(violations, bins=x, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    
    # Plots the mean and standard deviation of the frequency of violations
    ax1.axvline(x=mean_diff, color='blue', linestyle='--', linewidth=2, label=f"Mean difference: {mean_diff:.2f}")
    ax1.axvline(x=(mean_diff - std_diff), color='green', linestyle='--', linewidth=2, label=f"Std of difference: {std_diff:.2f}")
    ax1.axvline(x=(mean_diff + std_diff), color='green', linestyle='--', linewidth=2)

    # Plots the normal distribution on a second y-axis
    ax2 = ax1.twinx()
    ax2.plot(x_norm, pdf_fitted, color='black', linestyle='-', linewidth=1, label="Normal distribution")
    # plt.plot(x_axis_curve, pdf_fitted * max(freqs) * (1 / max(pdf_fitted)), color='black', linestyle='-', linewidth=1, label="Normal distribution")
    
    # Add labels to all axes
    ax1.set_xlabel("Violations")
    ax1.set_ylabel("Frequency")
    ax2.set_ylabel("Probability density")

    # Makes sure both y-axes starts at 0
    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2)

    # Add a grid, legend and save plot both with and without title
    plt.grid(alpha=0.5)
    plt.savefig(f"Plots/no_title/Violations_LS_{n}.png", bbox_inches='tight')
    plt.title(f"Violations for {amount} randomly generated Latin Squares of size {n}")
    plt.savefig(f"Plots/Violations_LS_{n}.png", bbox_inches='tight')
    if show:
        plt.show()

# Plot the line graph of the mean and standard deviation of
# the frequency of violations for randomly generated Latin Squares
def plot_line(violations, power, show=False):
    n = violations[:, 0]
    means = violations[:, 1]
    stds = violations[:, 2]
    amount = "10^" + str(power)

    lower = int(n[0])
    upper = int(n[-1])

    plt.figure(figsize=(10, 6))
    plt.plot(n, means, color='black', linestyle='-', label="Mean difference")
    plt.fill_between(n, means - stds, means + stds, color='orange', alpha=0.5, label="Std of difference")
        
    plt.grid(alpha=0.5)
    plt.xlabel("Violations")
    plt.ylabel("Mean frequency")
    plt.legend()
    plt.savefig(f"Plots/no_title/All_violations({lower}-{upper}).png", bbox_inches='tight')
    plt.title(f"Violations for {amount} Latin Squares with n: [{lower}, {upper}]")
    plt.savefig(f"Plots/All_violations({lower}-{upper}).png", bbox_inches='tight')
    if show:
        plt.show()

# Main plotting function
def plot_violations(results, power, hist=False, line=False, show=False):
    all_violations = np.array([])
    
    for n, violations in results.items():
        mean_diff = np.mean(violations)
        std_diff = np.std(violations)

        if line:
            data = np.array([n, mean_diff, std_diff])
            all_violations = np.append(all_violations, data)

        if hist:
            plot_histogram(n, violations, power, mean_diff, std_diff, show)
    
    if line:
        all_violations = all_violations.reshape(len(results), 3)
        plot_line(all_violations, power, show)