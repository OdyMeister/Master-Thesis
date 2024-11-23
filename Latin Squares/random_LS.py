import numpy as np
from plot import plot_violations

# Generate a random Latin Square of size n
# Row-wise generation, thus columns are most likely invalid
def random_LS(n):
    LS = np.array([])

    for _ in range(n):
        row = np.arange(n)
        np.random.shuffle(row)
        LS = np.append(LS, row)
    
    return LS.reshape(n, n)

# Check the number of violations in a Latin Square
def check_LS(n, LS):
    violations = 0

    # Turning each column into a set and subtracting the length
    # from n tells us how many numbers are missing
    for i in range(n):
        violations += n - len(set(LS[:, i]))
    
    return violations

# Main funcion to generate and check Latin Squares for violations
def calc_violations(n_lower, n_upper, power):
    results = {}

    # Outer loop for the size of the Latin Square
    for n in range(n_lower, n_upper + 1, 2):
        results[n] = []

        # Inner loop saving the number of violations for each Latin Square
        for _ in range(10**power):
            ls = random_LS(n)
            violations = check_LS(n, ls)
            results[n].append(violations)
    
    return results
        
if __name__ == "__main__":
    sample_size_power = 5
    result = calc_violations(4, 50, sample_size_power)
    plot_violations(result, sample_size_power, hist=False, line=True, show=False)