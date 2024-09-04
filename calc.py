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


def calc_distance(filepath, n):
    with open(filepath, "r") as file:
        schedules = []
        distances = []

        for line in file:
            raw_schedule = ast.literal_eval("[" + line + "]")
            schedule_chunks = [raw_schedule[i:i+n//2] for i in range(0, len(raw_schedule), n//2)]
            schedules.append(schedule_chunks)
        
        for s in range(len(schedules)):
            for c in range(s+1, len(schedules)):
                distance = 0
                for r in range(len(schedules[s])):
                    for m in schedules[s][r]:
                        if m not in schedules[c][r]:
                            distance += 1
                distances.append(distance)
        
        return distances
    

def calc_distance_reduced(filepath, n):
    with open(filepath, "r") as file:
        schedules = []
        distances = []

        count = 1

        for line in file:
            raw_schedule = ast.literal_eval("[" + line + "]")
            schedule_chunks = [raw_schedule[i:i+n//2] for i in range(0, len(raw_schedule), n//2)]
            schedules.append(schedule_chunks)
            if count % 100000 == 0:
                print(count)
            count += 1
        
        for s in range(len(schedules)):
            for c in range(s+1, len(schedules)):
                distance = 0
                for r in range(len(schedules[s])):
                    for m in schedules[s][r]:
                        if not (m in schedules[c][r] or (m[1], m[0]) in schedules[c][r]):
                            distance += 1
                distances.append(distance)
        
        return distances


if __name__ == "__main__":
    print("...")