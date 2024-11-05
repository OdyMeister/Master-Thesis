import numpy as np
import sys
from copy import copy
from TTP import generate_matchups


FOUND = False


def print_schedule(schedule):
    print("Schedule found:")
    for i in range(len(schedule)):
        print(schedule[i])


def handle_schedule(n, schedule):
    formated = ""

    for i in range(len(schedule)):
        temp = sorted(schedule[i], key=lambda x: x[0])
        for m in temp:
            formated += f" {m[0]},{m[1]}"
    
    with open(f"Schedules/Sampler/{n}.csv", "a") as file:
        file.write(formated[1:] + "\n")


def same_round(schedule, matchup, index):
    round = schedule[index[1]]

    for m in round:
        if m[0] in matchup or m[1] in matchup:
            return True
        
    return False


def back_to_back(schedule, matchup, index):
    if index[1] != 0:
        prev_round = schedule[index[1]-1]
        if (matchup[1], matchup[0]) in prev_round:
            return True
    if index[1] < len(schedule)-1:
        next_round = schedule[index[1]+1]
        if (matchup[1], matchup[0]) in next_round:
            return True

    return False


def home_away_streak(schedule, matchup, index):
    lower = max(0, index[1]-3)
    upper = min(len(schedule)-1, index[1]+3)
    rounds = schedule[lower:upper+1]
    streaks = {"home1": 0, "home2": 0, "away1": 0, "away2": 0}

    for round in rounds:
        for m in round:
            if m[0] == matchup[0]:
                streaks["home1"] += 1
                streaks["away1"] = 0
            if m[0] == matchup[1]:
                streaks["away1"] += 1
                streaks["home1"] = 0
            if m[1] == matchup[0]:
                streaks["home2"] += 1
                streaks["away2"] = 0
            if m[1] == matchup[1]:
                streaks["away2"] += 1
                streaks["home2"] = 0
        
        for key in streaks:
            if streaks[key] == 3:
                return True

    return False


def check_constraints(schedule, matchup, index):
    if same_round(schedule, matchup, index):
        return True
    if back_to_back(schedule, matchup, index):
        return True
    if home_away_streak(schedule, matchup, index):
        return True
    return False


def gen_rand(n, matchups, schedule, indexes):
    if len(matchups) == 0:
        global FOUND
        FOUND = True
        handle_schedule(n, schedule)
        return
    
    current = matchups[0]
    
    for i in indexes:
        if FOUND:
            return
        if check_constraints(schedule, current, i):
            continue

        new_schedule = [[m for m in r] for r in schedule]
        new_matchups = matchups[1:]
        new_indexes = [j for j in indexes if j != i]

        new_schedule[i[1]][i[0]] = current

        gen_rand(n, new_matchups, new_schedule, new_indexes)


def normalize_schedule(schedule, matchups):
    for i in range(0, len(schedule[0])*2, 2):
        schedule[0][i//2] = (i, i+1)
        matchups.remove((i, i+1))


def gen_rand_init(n):
    matchups = []
    schedule = [[(-1,-1) for _ in range(n//2)] for _ in range(2*(n-1))]
    indexes = [(i,j) for i in range(n//2) for j in range(1, 2*(n-1))]

    generate_matchups(n, matchups)
    np.random.shuffle(indexes)

    normalize_schedule(schedule, matchups)

    gen_rand(n, matchups, schedule, indexes)


if __name__ == '__main__':
    n = int(sys.argv[1])

    # with open(f"Schedules/Sampler/{n}.csv", "w") as file:
    #     file.write("")

    for _ in range(10000000):
        FOUND = False
        gen_rand_init(n)