from helper import *
import random


# Generate all possible matchups of teams
def generate_matchups(n, matchups):
    for i in range(n):
        for j in range(n):
            if i != j:
                matchups.append((i, j))
    # Matchups are shuffled to prevent a certain order of teams from occuring every time
    random.shuffle(matchups)


# Function to check if a team plays the same team back-to-back
def prevent_back_to_back(m, prev_round):
    if (m[1], m[0]) in prev_round:
        return True
    return False


# Function to generate the home/away (streak) count for each team
def generate_streak_count(n, streaks):
    matches = n-1

    for i in range(n):
        streaks[i] = (matches, matches, (0, "home"))


# Checks if a future streak violation will occur for each team in the current matchup
# This will happen if (x + s) / 3 <= y + 1 is violated for either team
# where x is max(home_games left, away_games left) and y is min(home_games left, away_games left)
# s is the number of games played at home or on the road in a row
def check__future_streak_violation(m, streaks):
    x = max(streaks[m[0]][0] - 1, streaks[m[0]][1])
    y = min(streaks[m[0]][0] - 1, streaks[m[0]][1])
    s = streaks[m[0]][2][0] if (streaks[m[0]][2][1] == "home" and streaks[m[0]][0] - 1 > streaks[m[0]][1]) else 0

    if (x + s) / 3 > y + 1:
        #print(f"Future home streak violation for team {m[0]}, \t {streaks[m[0]]} \t x: {x}, y: {y}, s: {s}")
        return True

    x = max(streaks[m[1]][0], streaks[m[1]][1] - 1)
    y = min(streaks[m[1]][0], streaks[m[1]][1] - 1)
    s = streaks[m[1]][2][0] if (streaks[m[1]][2][1] == "away" and streaks[m[1]][1] - 1 > streaks[m[1]][0]) else 0

    if (x + s) / 3 > y + 1:
        #print(f"Future away streak violation for team {m[1]}, \t {streaks[m[1]]} \t x: {x}, y: {y}, s: {s}")
        return True

    return False


# Function to check if the teams in the current matchups will play at home or on the road more than three times in a row
def prevent_four_in_a_row(m, streaks):
    # Get the current streaks for the two teams in the matchup
    streakA = streaks[m[0]][2]
    streakB = streaks[m[1]][2]

    # If the first team already played at home or, the second team on already played on the road three times in a row, skip this round
    if (streakA[0] == 3 and streakA[1] == "home") or (streakB[0] == 3 and streakB[1] == "away"):
        return True
    return False


def update_streaks(m, streaks):
    if streaks[m[0]][2][1] == "home":
        streaks[m[0]] = (streaks[m[0]][0]-1, streaks[m[0]][1], (streaks[m[0]][2][0] + 1, "home"))
    else:
        streaks[m[0]] = (streaks[m[0]][0]-1, streaks[m[0]][1], (1, "home"))

    if streaks[m[1]][2][1] == "away":
        streaks[m[1]] = (streaks[m[1]][0], streaks[m[1]][1]-1, (streaks[m[1]][2][0] + 1, "away"))
    else:
        streaks[m[1]] = (streaks[m[1]][0], streaks[m[1]][1]-1, (1, "away"))


# Generate all possible cannonical schedules given all possible rounds
def generate_cannonical_schedules(n, matchups, streaks, schedules, args, schedule=[]):
    first_round = []

    for i in range(0, n, 2):
        first_round.append((i, i+1))
        matchups.remove((i, i+1))
        update_streaks((i, i+1), streaks)

    # Generate all possible schedules given this cannonical first round
    generate_schedules(n, matchups, streaks, schedules, args, first_round)


# Checks if a team in the current matchup is already playing in the current round
def check_repeat(m, current):
    # Also puts the matchup with the team with the lowest index first
    # This prevents duplicate rounds due to order of teams in a round being different
    for p in current:
        if m[0] in p or m[1] in p or m[0] < p[0]:
            return True
    return False


# Function to check if a schedule meets the constraints
def check_constraints(schedule, streaks, n, m):
    # Gets the index to find the matchups in the current round
    index = len(schedule) % (n//2)
    current = schedule[-index:] if index > 0 else []
    prev_round = schedule[-index-(n//2):-index] if len(schedule) >= (n-1) else []
    prev_rounds = [schedule[-index-(n//2*i):-index-(n//2*(i-1))] for i in range(1, 4)] if len(schedule) >= (2*n-1) else []

    # Checks if a team is playing in the current round
    if check_repeat(m, current):
        return True

    # If the current team is playing the same team back-to-back, skip this round
    if prevent_back_to_back(m, prev_round) if prev_round else False:
        return True

    # If the last three rounds have a team playing at home or away three times in a row, skip this round
    if prevent_four_in_a_row(m, streaks):
        return True
    
    # If the current matchup creates a future streak violation, skip this round
    if check__future_streak_violation(m, streaks):
        return True

    return False


def handle_complete_schedule(n, schedule, schedules, args):
    # Handle the schedule if counter is provided
    if args.count != None:
        if args.count != 0 and get_count() % args.count == 0:
            print("Current schedule count:", get_count())

    # Handle the schedule if verbose is provided
    if args.verbose != None:
        schedules.append(schedule)

    # Handle the schedule if save is not provided
    if args.save != None:
        _, _, path = generate_paths(n, args)

        # Append the current schedule to the file
        with open(path, "a") as file:
            file.write(','.join([str(matchup) for matchup in schedule]) + "\n")


# Generate all possible schedules given all possible matchups
def generate_schedules(n, matchups, streaks, schedules, args, schedule=[]):
    #print("Streaks: ", streaks)
    # If the maximum number of schedules has been reached, return
    if len(schedules) == args.max or get_count() == args.max:
        return

    # If there are no more matchups, the schedule is complete
    if len(matchups) == 0:
        counter()
        handle_complete_schedule(n, schedule, schedules, args)
        return

    # For each round still possible, generate a new schedule
    for m in matchups:
        # Checks if a team plays back to back or a team is on the road or at home more than three times in a row
        if check_constraints(schedule, streaks, n, m):
            continue

        new_matchups = [new_m for new_m in matchups if new_m != m]
        new_schedule = [s for s in schedule] + [m]
        new_streaks = streaks.copy()

        update_streaks(m, new_streaks)
                
        # Generate all possible schedules given this round
        generate_schedules(n, new_matchups, new_streaks, schedules, args, new_schedule)