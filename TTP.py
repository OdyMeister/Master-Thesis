import sys
import numpy as np
import copy

COUNT = 0

def counter():
    global COUNT
    COUNT += 1
    print(COUNT)

def print_schedules(n, schedules):
    print("TTP for %d teams:" % n)
    for schedule in schedules:
        print("", schedule)

def generate_matchups(n):
    # Initialize matchups array
    matchups = []

    # Generate all possible matchups
    for i in range(n):
        for j in range(n):
            if i != j:
                matchups.append((i, j))
    return matchups

def generate_schedules(n, matchups, schedules, schedule=[]):
    if len(schedule) is (n-1) * n:
        schedules.append(schedule)
        return

    prev = []
    index = len(schedule) % (n // 2)
    
    if index is not 0:
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
    matchups = generate_matchups(n)
    print("Matchups:\n", matchups)
    generate_schedules(n, matchups, schedules)

    #print(len(schedules))
    print_schedules(n, schedules[:20])

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