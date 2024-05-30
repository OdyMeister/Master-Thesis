from helper import *
import random
import numpy as np
import sys


# Generate all possible matchups of n teams
def generate_matchups(n):
    matchups = np.array([], dtype=[("team1", np.int32), ("team2", np.int32)])

    for i in range(n):
        for j in range(n):
            if i != j:
                matchups = np.append(matchups, np.array([(i, j)], dtype=matchups.dtype))

    return matchups


# Function to generate the home/away (streak) count for each team
def generate_streak_count(n):
    streaks = np.array([], dtype=[("home", np.int32), ("away", np.int32), ("streak", np.int32), ("type", np.dtype("U5"))])
    matches = n-1

    for i in range(n):
        streaks = np.append(streaks, np.array([(matches, matches, 0, "home")], dtype=streaks.dtype))

    return streaks


# Function to update the streaks for the two teams in the current matchup m
def update_streaks(m, streaks):
    if streaks[m[0]]["type"] == "home":
        streaks[m[0]]["streak"] += 1
    else:
        streaks[m[0]]["streak"] = 1
        streaks[m[0]]["type"] = "home"
    streaks[m[0]]["home"] -= 1

    if streaks[m[1]]["type"] == "away":
        streaks[m[1]]["streak"] += 1
    else:
        streaks[m[1]]["streak"] = 1
        streaks[m[1]]["type"] = "away"
    streaks[m[1]]["away"] -= 1


# Checks if a future streak violation will occur for each team in the current matchup m
# This will happen if x / 3 <= y + 1 is violated for either team,
# where x is max(home_games left, away_games left) and y is min(home_games left, away_games left), i.e. x >= y
def check_future_streak_violation(m, streaks):
    x = max(streaks[m[0]]["home"] - 1, streaks[m[0]]["away"])
    y = min(streaks[m[0]]["home"] - 1, streaks[m[0]]["away"])

    if x / 3 > y + 1:
        return True

    x = max(streaks[m[1]]["home"], streaks[m[1]]["away"] - 1)
    y = min(streaks[m[1]]["home"], streaks[m[1]]["away"] - 1)

    if x / 3 > y + 1:
        return True

    return False


# Function to check if the teams in the current matchups will play at home or on the road more than three times in a row
def prevent_four_in_a_row(m, streaks):
    # If the first team already played at home or, the second team on already played on the road three times in a row, skip this round
    if (streaks[m[0]]["streak"] >= 3 and streaks[m[0]]["type"] == "home") or (streaks[m[1]]["streak"] >= 3 and streaks[m[1]]["type"] == "away"):
        return True
    return False


# Function to check if a team plays the same team back-to-back
def prevent_back_to_back(m, prev_round):
    if np.any(np.logical_and(prev_round["team1"] == m[1], prev_round["team2"] == m[0])):
        return True
    return False


# Checks if a team in the current matchup is already playing in the current round
# Also sorts the matchup to prevent duplicate rounds due to order of teams in a round being different,
# since the order of matchups within a round doesn't matter
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
    index = np.size(schedule) % (n//2)
    current = schedule[-index:] if index != 0 else np.array([])
    prev_round = np.array([], dtype=schedule.dtype)

    # If the index is 0, we can't slice until and index of -0, so we need to handle this case separately
    if index == 0:
        prev_round = schedule[-(n//2):]
    elif len(schedule) >= (index+(n//2)):
        prev_round = schedule[-index-(n//2):-index]

    # print("Schedule: ", schedule)
    # print("Matchup: ", m)
    # print("Current: ", current)
    # print("Prev: ", prev_round)
    # print("Index: ", index)
    # print()

    # Checks if a team is playing in the current round
    if check_repeat(m, current):
        return True

    # If the current team is playing the same team back-to-back, skip this round
    if prevent_back_to_back(m, prev_round) if np.size(prev_round) > 0 else False:
        return True

    # If the last three rounds have a team playing at home or away three times in a row, skip this round
    if prevent_four_in_a_row(m, streaks) if np.size(prev_round) > 0 else False:
        return True
    
    # If the current matchup creates a future streak violation, skip this round
    if check_future_streak_violation(m, streaks):
        return True

    return False


# Function to handle completed schedules
def handle_complete_schedule(n, schedule, schedules, args):
    # Handle the schedule if counter is provided
    if args.count != None:
        if args.count != 0 and get_count() % args.count == 0:
            print("Current schedule count:", get_count())

    # Handle the schedule if verbose is provided
    if args.verbose != None:
        schedules.append(schedule)

    # Handle the schedule if save is provided
    if args.save != None:
        handle_save(n, schedule, args)


# Generate all possible cannonical schedules given all possible rounds
def generate_cannonical_schedules(n, matchups, streaks, schedules, args):
    first_round = np.array([], dtype=[("team1", np.int32), ("team2", np.int32)])

    for i in range(0, n, 2):
        first_round = np.append(first_round, np.array([(i, i+1)], dtype=first_round.dtype))
        matchups = np.delete(matchups, np.where((matchups["team1"] == i) & (matchups["team2"] == i+1)))
        update_streaks((i, i+1), streaks)

    # Generate all possible schedules given this cannonical first round
    generate_schedules(n, matchups, streaks, schedules, args, first_round)


# Generate all possible schedules given all possible matchups
def generate_schedules(n, matchups, streaks, schedules, args, schedule=np.array([], dtype=[("team1", np.int32), ("team2", np.int32)])):
    # If the maximum number of schedules has been reached, return
    if len(schedules) == args.max or get_count() == args.max:
        return

    # If there are no more matchups, the schedule is complete
    if len(matchups) == 0:
        counter()
        handle_complete_schedule(n, schedule, schedules, args)
        return

    # For each matchup still possible, generate a new schedule
    for m in matchups:
        # Checks all TTP constraints for the current matchup
        if check_constraints(schedule, streaks, n, m):
            continue

        new_matchups = np.delete(matchups, np.where((matchups["team1"] == m["team1"]) & (matchups["team2"] == m["team2"])))
        new_schedule = np.append(schedule, np.array([m], dtype=schedule.dtype))
        new_streaks = np.copy(streaks)

        update_streaks(m, new_streaks)
                
        # Generate all possible schedules given this round
        generate_schedules(n, new_matchups, new_streaks, schedules, args, new_schedule)


# Main function to generate all possible TTP schedules for each given number of teams
def generate_TTP(n, args=None):
    schedules = []
    matchups = generate_matchups(n)
    streaks = generate_streak_count(n)

    if args.verbose:
        print(f"\nGenerating TTP schedules for {n} teams:")

    # Create the folder path if save is provided
    if args.save != None:
        init_save(n, args)

    # Prints the matchups if verbose is provided
    if args.verbose != None:
        print_matchups(matchups, args.verbose)

    # Generate all possible schedules given all possible rounds
    # If cannonical is provided, generate all possible cannonical schedules (i.e. schedules with the same first round)
    if args.cannonical:
        generate_cannonical_schedules(n, matchups, streaks, schedules, args)
    else:
        generate_schedules(n, matchups, streaks, schedules, args)

    # Print the schedules if verbose is provided
    if args.verbose != None:
        print_schedules(n, schedules, args.verbose)

    # Print the number schedules
    if args.count != None and args.verbose == None:
        print(f"Final schedule count ({n} teams): {get_count()}")
    
    reset_count()