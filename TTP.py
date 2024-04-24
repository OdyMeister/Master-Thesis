import sys
import multiprocessing
from debug import *

# Generate all possible matchups of teams
def generate_matchups(n, matchups):
    for i in range(n):
        for j in range(n):
            if i != j:
                matchups.append((i, j))


# Function to generate all possible rounds given the set of matchups
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
        generate_rounds(n, new_matchups, rounds, new_round)


# Function which removes rounds with duplicate matchups
def remove_duplicates(round, rounds, new_rounds):
    for r in rounds:
        duplicate = False
        for m in r:
            if m in round:
                duplicate = True
                break
        if not duplicate:
            new_rounds.append(r)


# Function to check if a team plays the same team back-to-back
def prevent_back_to_back(round, prev_round):
    for m in round:
        if (m[1], m[0]) in prev_round:
            return True
    return False


# Function to check if a team plays at home or away more than three times in a row
def prevent_four_in_a_row(round, prev_rounds):
    for m in round:
        countA = 0
        countB = 0

        for r in prev_rounds:
            for p in r:
                if m[0] == p[0]:
                    countA += 1
                if m[1] == p[1]:
                    countB += 1

        if countA == 3 or countB == 3:
            return True
    return False


# Generate all possible schedules given all possible rounds
def generate_schedules(n, rounds, schedules, schedule=[]):
    print(f"rounds: {len(rounds)}, schedules: {len(schedules)}, schedule: {len(schedule)}", flush=True)

    if len(schedule) == (n - 1) * 2:
        #schedules.append(schedule)
        counter(print=False)
        return

    for round in rounds:
        if prevent_back_to_back(round, schedule[-1]) if schedule else False:
            continue

        if prevent_four_in_a_row(round, schedule[-3:]) if len(schedule) >= 3 else False:
            continue

        new_rounds = []
        new_schedule = schedule.copy()
        new_schedule.append(round)

        remove_duplicates(round, rounds, new_rounds)
        
        generate_schedules(n, new_rounds, schedules, new_schedule)


def parallel_generate_schedules(n, rounds, schedules):
    pool = multiprocessing.Pool()
    for r in rounds:
        new_rounds = rounds.copy()
        new_rounds.remove(r)
        pool.apply_async(generate_schedules, (n, new_rounds, schedules, [r]))


# Main function to generate all possible TTP schedules
def generate_TTP(n):
    schedules = []
    matchups = []
    rounds = set()

    generate_matchups(n, matchups)
    #print_matchups(matchups)

    generate_rounds(n, matchups, rounds)
    #print_rounds(rounds)

    generate_schedules(n, rounds, schedules)
    # parallel_generate_schedules(n, rounds, schedules)
    print_count()
    #print_schedules(n, schedules, 5)


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