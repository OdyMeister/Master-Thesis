import sys
import numpy as np
import copy

COUNT = 0

# Debugging function to count the number of times a function is called
def counter(print=True):
    global COUNT
    COUNT += 1
    if print:
        print(COUNT)


# Debugging function to print the schedules
def print_schedules(n, schedules, first=20):
    print("First %d TTP schedules (out of %d) for %d teams:" % (first, len(schedules), n))
    for schedule in schedules[:first]:
        print("", schedule)


# Debugging function to print the all possible matchups
def print_matchups(matchups, first=20):
    print("First %d matchups:" % first)
    for m in matchups[:first]:
        print("", m)


# Debugging function to print the all possible rounds
def print_rounds(rounds, first=20):
    print("First %d rounds:" % first)
    for r in list(rounds)[:first]:
        print("", tuple(r))


# Function to generate all possible rows
def generate_rounds(n, matchups, rounds, round=set()):
    if len(round) == n // 2:
        rounds.add(frozenset(round))
        return
    
    for m in matchups:
        duplicate = False

        for r in round:
            if m[0] in r or m[1] in r:
                duplicate = True
                break

        if duplicate:
            continue

        new_matchups = matchups.copy()
        new_matchups.remove(m)
        new_round = round.copy()
        new_round.add(m)
        # new_row.append(m)
        generate_rounds(n, new_matchups, rounds, new_round)


# Generate all possible matchups
def generate_matchups(n, matchups):
    for i in range(n):
        for j in range(n):
            if i != j:
                matchups.append((i, j))


# Generate all possible schedules given all possible rounds
# def generate_schedule(n, rounds, schedules, schedule=[]):



def generate_schedules(n, matchups, schedules, schedule=[]):
    if len(schedule) is (n-1) * n:
        schedules.append(schedule)
        return

    prev = []
    index = len(schedule) % (n // 2)

    if index != 0:
        temp = schedule[-index:]
        for t in temp:
            prev.append(t[0])
            prev.append(t[1])

    for m in matchups:
        if len(prev) > 0 and (m[0] in prev or m[1] in prev):
            continue

        new_matchups = matchups.copy()
        new_matchups.remove(m)
        new_schedule = schedule.copy()
        new_schedule.append(m)

        generate_schedules(n, new_matchups, schedules, new_schedule)


def generate_TTP(n):
    schedules = []
    rounds = set()
    matchups = []

    generate_matchups(n, matchups)
    print_matchups(matchups)

    generate_rounds(n, matchups, rounds)
    print_rounds(rounds)

    generate_schedules(n, matchups, schedules)
    print_schedules(n, schedules, 5)


if __name__ == "__main__":
    # Set n_start and n_end equal to first and second command line arguments
    try:
        n_start = int(sys.argv[1])
    except:
        print("Usage:\n python TTP.py n_start n_end\n python TTP.py n")
    
    # If n_end is not provided, set it equal to n_start
    try:
        n_end = int(sys.argv[2])
    except:
        n_end = n_start

    # Check if n_start or n_end is odd
    if n_start % 2 != 0 or n_end % 2 != 0:
        print("n_start and n_end must be even")
        sys.exit(1)
    elif n_start > n_end:
        print("n_start must be less than or equal to n_end")
        sys.exit(1)

    # Run generate_TTP for each n in the range
    for n in range(n_start, n_end + 1, 2):
        generate_TTP(n)