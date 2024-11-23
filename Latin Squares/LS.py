import numpy as np
import sys
import timeit

COUNT = 0

# This function generates all the Latin Squares of order n
# It does so using random backtracking
def ls_random_backtracking(n, save=False):
    # Make a list to store all the Latin Squares and initialize the first one
    LSs = []
    LS = np.zeros((n, n), dtype=int) - 1

    # Initialize the index for first row and column
    row, column = 1, 0

    # Keeps track of the numbers which are still available in the current row
    current = [i for i in range(n)]

    # Half-normalize the Latin Square
    for i in current:
        LS[0, i] = i
    
    # Recursively generates all Latin Squares of order n
    ls_rb(n, row, column, current, LS, LSs, save=save)

    return LSs

# Recursive function to generate all Latin Squares of order n
def ls_rb(n, i_row, i_column, current, LS, LSs, save=False):
    # If we have reached the end of the column, we have a Latin Square
    if i_row == n:
        global COUNT
        COUNT += 1
        return
        if save:
            LSs.append(LS.copy())
        return
    
    for num in current:
        # Get the current column
        column = LS[:, i_column]

        # Check if the number is already in the column
        if num in column:
            continue

        # Removes the number from the current list and updates the Latin Square
        new_current = [new_num for new_num in current if new_num != num]
        new_LS = LS.copy()
        new_LS[i_row, i_column] = num

        # Update the row and column indices
        new_i_column = i_column + 1
        new_i_row = i_row

        # If the end of the row is reached, reset indices and current list
        if new_i_column == n:
            new_i_row += 1
            new_i_column = 0
            new_current = np.array([i for i in range(n)])

        ls_rb(n, new_i_row, new_i_column, new_current, new_LS, LSs)


if __name__ == "__main__":
    n_min = int(sys.argv[1])
    n_max = int(sys.argv[2])
    file = open("Count/LS_count.txt", "w")

    # Calculate number of Latin Squares of order up to n_max
    for n in range(n_min, n_max, 2):
        # Running and timing the generation of all Latin Squares of order n
        start_time = timeit.default_timer()
        ls_random_backtracking(n)
        stop_time = timeit.default_timer()
        elapsed_time = stop_time - start_time

        # Format the time
        if elapsed_time < 1:
            time = f"{elapsed_time * 1000:.2f} ms"
        elif elapsed_time < 60:
            time = f"{elapsed_time:.2f} s"
        elif elapsed_time < 3600:
            time = f"{elapsed_time / 60:.2f} min"
        else:
            time = f"{elapsed_time / 3600:.2f} h"

        file.write(f"n={n}: {COUNT}, {time}\n")

        print(f"n={n}:", COUNT, time)
        COUNT = 0
        