import math
import ast
import sys
from TTP import *
from plot import *

# Calculate the number of possible rounds for a given number of teams
def calc_rounds(n):
    return math.factorial(n) // math.factorial(n//2)


# Calculate the number of possible matchups for a given number of teams
def calc_matchups(n):
    return n**2 - n

# Calculate the number of possible Double Round Robbin schedules for a given number of teams
def calc_drr_schedules(n):
    return math.factorial(calc_rounds(n)) // math.factorial(calc_rounds(n) - (n-1)*2)


def verify(schedule, matchups, n, count):
    current = []
    prev_round1 = []
    streak = {i: {"home": 0, "away": 0} for i in range(n)}

    for matchup in schedule:
        if matchup not in matchups:
            print("Matchup used multiple times", matchup)
        else:
            matchups.remove(matchup)

        if streak[matchup[0]]["home"] == 3:
            print(f"Home streak violation: {matchup}, Schedule#: {count}")
        streak[matchup[0]]["home"] += 1
        streak[matchup[0]]["away"] = 0

        if streak[matchup[1]]["away"] == 3:
            print("Away streak violation", matchup)
        streak[matchup[1]]["away"] += 1
        streak[matchup[1]]["home"] = 0

        
        if len(current) < n//2:
            current.append(matchup)
        else:
            prev_round1 = current
            current = [matchup]

        for m in current:
            if (matchup[0] in m or matchup[1] in m) and m != matchup:
                print("Same team plays multiple times in one round", current, matchup, schedule)

        if (matchup[1], matchup[0]) in prev_round1:
            print(f"Back-to-back matchup, prev_round: {prev_round1}, current: {current}, schedule#: {count}")


def verify_schedules(n, path):
    with open(path, "r") as file:
        count = 1
        for line in file:
            matchups = []
            generate_matchups(n, matchups)
            schedule = ast.literal_eval("[" + line + "]")
            verify(schedule, matchups, n, count)
            count += 1


def calc_distance(filepath):
    with open(filepath, "r") as file:
        schedules = []
        count = 0
        distances = {}
        distances_separate = []

        for line in file:
            schedules.append(ast.literal_eval("[" + line + "]"))
            distances[count] = []
            count += 1
        
        for i in range(len(schedules)):
            for j in range(i+1, len(schedules)):
                distance = 0
                for k in range(len(schedules[i])):
                    if schedules[i][k] != schedules[j][k]:
                        distance += 1
                distances[i].append(distance)
                distances[j].append(distance)
                distances_separate.append(distance)
        
        return distances, distances_separate


if __name__ == "__main__":
    distances, distances_separate = calc_distance(sys.argv[1])
    plot_distances(distances, distances_separate)