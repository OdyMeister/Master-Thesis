import math
import ast
import sys
import numpy as np
from TTP import *
from plot import *
from scipy.stats import beta, betabinom
from sklearn.metrics import r2_score


# Calculate the number of possible rounds for a given number of teams
def calc_rounds(n):
    return math.factorial(n) // math.factorial(n//2)


# Calculate the number of possible matchups for a given number of teams
def calc_matchups(n):
    return n**2 - n


# Calculate the number of possible Double Round Robbin schedules for a given number of teams
def calc_drr_schedules(n):
    return math.factorial(calc_rounds(n)) // math.factorial(calc_rounds(n) - (n-1)*2)

def adjusted_R2(x, expected, max_diff, a, b):
    pdf = beta.pdf(x, a, b, loc=0, scale=max_diff)
    r2 = r2_score(expected, pdf)
    return r2

def diff_beta_binom_fit(x, expected, max_diff, a, b):
    pdf = betabinom.pmf(x, max_diff, a, b, loc=0)
    score = np.sum((expected - pdf)**2)
    return score

def fit_beta_binom(x, data, max_diff):
    x = list(x)
    best_fit = np.inf
    best_pmf = None
    expected = data / np.sum(data)

    for a in np.arange(1, 1000, 1):
        for b in np.arange(0.1, 30, 0.1):
            result = diff_beta_binom_fit(x, expected, max_diff, a, b)
            if result < best_fit:
                best_fit = result
                best_pmf = (a, b)

    print(f"Score: {best_fit}, a: {best_pmf[0]}, b: {best_pmf[1]}")
    return best_pmf


# Verifies one given schedule
def verify(schedule, matchups, n, count):
    current = []
    prev_round1 = []
    streak = {i: {"home": 0, "away": 0} for i in range(n)}

    # Goes through each matchup in the schedule and checks for violations
    for matchup in schedule:
        # Matchups keeps track of all matchups that have not been used yet, if it is not in matchups, it has been used before
        if matchup not in matchups:
            print("Matchup used multiple times:", matchup)
        else:
            matchups.remove(matchup)

        # Check if a team is playing more than three times in a row at home
        if streak[matchup[0]]["home"] == 3:
            print(f"Home streak violation: {matchup}, Schedule#: {count}")
        streak[matchup[0]]["home"] += 1
        streak[matchup[0]]["away"] = 0

        # Check if a team is playing more than three times in a row on the road
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


# Verifies all schedules in a file
def verify_schedules(n, path):
    with open(path, "r") as file:
        count = 1
        for line in file:
            matchups = []
            generate_matchups(n, matchups)
            schedule = ast.literal_eval("[" + line + "]")
            verify(schedule, matchups, n, count)
            count += 1


# Samples from all solutions to get a uniform distribution
def sample_schedules(n, path, sample_size):
    with open(path, "r") as file:
        count = 0
        schedules = []

        for line in file:
            if line == "\n":
                continue
            count += 1

        # Generate uniform unique indexes to sample from
        indexes = np.random.choice(count, sample_size, replace=False)
        count = 0

    with open(path, "r") as file:
        with open(f'Schedules/Uniform/Uniform-{n}.csv', 'w') as dest:
            for line in file:
                if count in indexes:
                    dest.write(line)
                    indexes = np.delete(indexes, np.where(indexes == count))
                count += 1


# Calculate the distance between all schedules in a file
def calc_diff(filepath, n):
    with open(filepath, "r") as file:
        schedules = []
        name = filepath.split("\\")[-1].split(".")[0]

        dest = open(f"Distances/Distances {name}.csv", "w")
        dest_reduced = open(f"Distances/Distances Reduced {name}.csv", "w")
        dest_teamless = open(f"Distances/Distances Teamless {name}.csv", "w")

        # Read schedules from file and convert them to a list containing each round in the schedule
        for line in file:
            # Skip empty lines, such as the last line in a file
            if len(line) < 2:
                continue
            matchups = "(" + line.replace(" ", "),(").replace("\n", ")")
            raw_schedule = ast.literal_eval("[" + matchups + "]")
            schedule_chunks = [raw_schedule[i:i+n//2] for i in range(0, len(raw_schedule), n//2)]
            schedules.append(schedule_chunks)
        
        # Calculate the distance between all schedules
        # Both for the 'normal' schedules and the reduced schedules
        for s in range(len(schedules)):
            for c in range(s+1, len(schedules)):
                diff = 0            # Difference in matchups
                reduced_diff = 0    # Difference in matchups, disregarding home/away
                HA_diff = 0         # Difference in home/away assignments, i.e. disregarding the teams themselves

                for r in range(len(schedules[s])):
                    for m in schedules[s][r]:
                        if m not in schedules[c][r]:
                            diff += 1
                        if not (m in schedules[c][r] or (m[1], m[0]) in schedules[c][r]):
                            reduced_diff += 1

                        # Comparing each round to see if each team has the same home/away assignment
                        # The difference is thus round based, not matchup based
                        team1 = False
                        team2 = False
                        for m2 in schedules[c][r]:
                            if m[0] == m2[0]:
                                team1 = True
                                break
                            if m[1] == m2[1]:
                                team2 = True
                                break
                        if not team1:
                            HA_diff += 1
                        if not team2:
                            HA_diff += 1

                dest.write(f"{diff},")
                dest_reduced.write(f"{reduced_diff},")
                dest_teamless.write(f"{HA_diff},")

        #return distances, reduced
        print("Distances calculated")


def calc_uniformity(filepath, limit=0):
    with open(filepath, "r") as file:
        matchup_freq = {}
        count = 0

        # Read schedules from file and convert them to a list containing each round in the schedule
        for line in file:
            count += 1
            # Skip empty lines, such as the last line in a file
            if len(line) < 2:
                continue
            if matchup_freq.get(line) == None:
                matchup_freq[line] = 1
            else:
                matchup_freq[line] += 1

        if limit != 0:
            for key in matchup_freq.keys():
                if matchup_freq[key] > limit:
                    with open("Distances/Top-8_n=4.csv", "a") as dest:
                        dest.write(key)
        
        return matchup_freq


if __name__ == "__main__":
    filepath = sys.argv[1]
    n = int(sys.argv[2])
    calc_diff(filepath, n)
    # calc_uniformity(filepath)
    # sample_schedules(n, filepath, 10000)