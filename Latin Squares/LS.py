import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Generate a random Latin Square of size n
# Since each row is random, the LS is not guaranteed to be valid
def random_LS(n):
    LS = np.array([])

    for _ in range(n):
        row = np.arange(n)
        np.random.shuffle(row)
        LS = np.append(LS, row)
    
    return LS.reshape(n, n)



def check_column(n, column):
    violations = 0

    for i in range(n):
        if i not in column:
            violations += 1
    
    return violations


def check_LS(n, LS):
    violations = 0

    for i in range(n):
        violations += n - len(set(LS[:, i]))
    
    return violations


def calc_violations(n_lower, n_upper, power):
    results = {}

    for n in range(n_lower, n_upper + 1, 2):
        results[n] = []

        for _ in range(10**power):
            ls = random_LS(n)
            violations = check_LS(n, ls)
            results[n].append(violations)
    
    return results


def plot_violations(results, power, show=False):
    for n, violations in results.items():
        x = range(min(violations), max(violations) + 1)
        x_axis_curve = np.linspace(min(violations), max(violations), 1000)
        amount = "10^" + str(power)

        mean_diff = np.mean(violations)
        std_diff = np.std(violations)

        freqs, _, _ = plt.hist(violations, bins=x, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)
        
        plt.axvline(x=mean_diff, color='blue', linestyle='--', linewidth=2, label=f"Mean difference: {mean_diff:.2f}")
        plt.axvline(x=(mean_diff - std_diff), color='green', linestyle='--', linewidth=2, label=f"Std of difference: {std_diff:.2f}")
        plt.axvline(x=(mean_diff + std_diff), color='green', linestyle='--', linewidth=2)

        # pdf_fitted = norm.pdf(x_axis_curve, mean_diff, std_diff)
        # plt.plot(x_axis_curve, pdf_fitted * max(freqs) * (1 / max(pdf_fitted)), color='black', linestyle='-', linewidth=1, label="Normal dist. curve")
        
        plt.grid(alpha=0.5)
        plt.xlabel("Violations")
        plt.ylabel("Frequency")
        plt.legend()
        plt.savefig(f"Plots/no_title/Violations_LS_{n}.png")
        plt.title(f"Violations for row-generated Latin Squares of size {n}, for {amount} latin squares")
        plt.savefig(f"Plots/Violations_LS_{n}.png")
        if show:
            plt.show()


if __name__ == "__main__":
    sample_size_power = 3
    result = calc_violations(50, 50, sample_size_power)
    plot_violations(result, sample_size_power, False)