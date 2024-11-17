import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Plot the histogram of the frequency of violations for randomly generated Latin Squares
def plot_histogram(n, violations, power, mean_diff, std_diff, show=False):
    x = range(min(violations), max(violations) + 1)
    x_axis_curve = np.linspace(min(violations), max(violations), 1000)
    amount = "10^" + str(power)
    
    plt.figure(figsize=(10, 6))
    freqs, _, _ = plt.hist(violations, bins=x, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
    
    plt.axvline(x=mean_diff, color='blue', linestyle='--', linewidth=2, label=f"Mean difference: {mean_diff:.2f}")
    plt.axvline(x=(mean_diff - std_diff), color='green', linestyle='--', linewidth=2, label=f"Std of difference: {std_diff:.2f}")
    plt.axvline(x=(mean_diff + std_diff), color='green', linestyle='--', linewidth=2)

    pdf_fitted = norm.pdf(x_axis_curve, mean_diff, std_diff)
    plt.plot(x_axis_curve, pdf_fitted * max(freqs) * (1 / max(pdf_fitted)), color='black', linestyle='-', linewidth=1, label="Normal dist. curve")
    
    plt.grid(alpha=0.5)
    plt.xlabel("Violations")
    plt.ylabel("Frequency")
    plt.legend()
    plt.savefig(f"Plots/no_title/Violations_LS_{n}.png", bbox_inches='tight')
    plt.title(f"Violations for {amount} row-wise generated Latin Squares of size {n}")
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
    plt.title(f"Violations for {amount} row-generated Latin Squares of size n: [{lower}, {upper}]")
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