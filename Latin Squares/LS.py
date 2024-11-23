import numpy as np
import sys
import timeit
import random

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
    current = [num for num in range(n)]
    random.shuffle(current)

    # Half-normalize the Latin Square
    for i in current:
        LS[0, i] = i
    
    # Recursively generates all Latin Squares of order n
    ls_rb(n, row, column, current, LS, LSs, save=save)

    return LSs


# This function generates all the Latin Squares of order n
# It does so using double random backtracking
def ls_double_random_backtracking(n, save=False):
    # Make a list to store all the Latin Squares and initialize the first one
    LSs = []
    LS = np.zeros((n, n), dtype=int) - 1

    # Keeps track of all the empty spots in the LS
    indexes = [(i, j) for i in range(1, n) for j in range(n)]
    random.shuffle(indexes)

    # Half-normalize the Latin Square
    for i in range(n):
        LS[0, i] = i

    # Recursively generates all Latin Squares of order n
    ls_drb(n, indexes, LS, LSs, save=save)

    return LSs


# Recursive function to generate all Latin Squares of order n
def ls_rb(n, i_row, i_column, current, LS, LSs, save=False):
    # If we have reached the end of the column, we have a Latin Square
    if i_row == n:
        global COUNT
        COUNT += 1
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

        # Update the row and column indexes
        new_i_column = i_column + 1
        new_i_row = i_row

        # If the end of the row is reached, reset indexes and current list
        if new_i_column == n:
            new_i_row += 1
            new_i_column = 0
            new_current = np.array([i for i in range(n)])

        ls_rb(n, new_i_row, new_i_column, new_current, new_LS, LSs)


# Recursive function to generate all Latin Squares of order n using double random backtracking
def ls_drb(n, indexes, LS, LSs, save=False):
    if len(indexes) == 0:
        global COUNT
        COUNT += 1
        if save:
            LSs.append(LS.copy())
        return
    
    # Get the current row and column indexes
    i_row, i_column = indexes[0]

    # Check if we can place any of the numbers up to n
    for num in range(n):
        # Get the current column and row
        column = LS[:, i_column]
        row = LS[i_row]

        # Check if the number is already in the column
        if num in column or num in row:
            continue

        # Copy everything
        new_LS = LS.copy()
        new_LS[i_row, i_column] = num
        new_indexes = indexes[1:]

        ls_drb(n, new_indexes, new_LS, LSs)


# Runs and times a given generator function for generating all Latin Squares of order n
def timer(n, generator):
    # Running and timing the generation of all Latin Squares of order n
    start_time = timeit.default_timer()
    generator(n)
    stop_time = timeit.default_timer()
    runtime = stop_time - start_time

    # Format the time
    if runtime < 1:
        time = f"{runtime * 1000:.2f} ms"
    elif runtime < 60:
        time = f"{runtime:.2f} s"
    elif runtime < 3600:
        time = f"{runtime / 60:.2f} min"
    elif runtime < 3600 * 24:
        time = f"{runtime / 3600:.2f} h"
    else:
        time = f"{runtime / (3600 * 24):.2f} days"

    return time

# Main function which calls the timers and collects the resulst
def main(n_min, n_max):
    global COUNT
    file_rb = open("Count/LS_rb_count.txt", "w")
    file_drb = open("Count/LS_drb_count.txt", "w")

    # Calculate number of Latin Squares of order up to n_max
    for n in range(n_min, n_max + 1, 2):
        time = timer(n, ls_random_backtracking)
        file_rb.write(f"n={n}: {COUNT}, {time}\n")
        print(f"rb  n={n}:", COUNT, time)
        COUNT = 0

        time = timer(n, ls_double_random_backtracking)
        file_drb.write(f"n={n}: {COUNT}, {time}\n")
        print(f"drb n={n}:", COUNT, time)
        COUNT = 0

        print()


# Get arguments and run main function
if __name__ == "__main__":
    n_min = int(sys.argv[1])
    try:
        n_max = int(sys.argv[2])
    except:
        n_max = n_min
    main(n_min, n_max)
        