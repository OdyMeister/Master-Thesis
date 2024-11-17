import numpy as np
from plot import plot_violations

# Generate a random Latin Square of size n row-wise
# I.e. each row is valid, but the columns are most likely not
def random_rowwise_LS(n):
    LS = np.array([])

    for _ in range(n):
        row = np.arange(n)
        np.random.shuffle(row)
        LS = np.append(LS, row)
    
    return LS.reshape(n, n)

# Generate a random Latin Square of size n
# Both rows and columns are most likely invalid
def random_LS(n):
    LS = np.array([[i for i in range(n)] for _ in range(n)])
    np.random.shuffle(LS)
    return LS.reshape(n, n)

# Check the number of violations in a Latin Square
def check_LS(n, LS):
    violations = 0

    for i in range(n):
        violations += n - len(set(LS[i]))
        violations += n - len(set(LS[:, i]))

    return violations

# Check the number of violations in the columns of a Latin Square
def check_columns_LS(n, LS):
    violations = 0

    for i in range(n):
        violations += n - len(set(LS[:, i]))
    
    return violations

# Main funcion to generate and check Latin Squares for violations
def calc_violations(n_lower, n_upper, power):
    results = {}

    for n in range(n_lower, n_upper + 1, 2):
        results[n] = []

        for _ in range(10**power):
            ls = random_rowwise_LS(n)
            violations = check_columns_LS(n, ls)
            results[n].append(violations)
    
    return results
        

if __name__ == "__main__":
    sample_size_power = 3
    result = calc_violations(4, 50, sample_size_power)
    plot_violations(result, sample_size_power, line=True, show=True)