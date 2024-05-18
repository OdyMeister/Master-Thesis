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
def prevent_back_to_back(round, prev_round):
    for m in round:
        if (m[1], m[0]) in prev_round:
            return True
    return False


# Function to check if a team, in the current round, will play at home or on the road more than three times in a row
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


# Generate all possible cannonical schedules given all possible rounds
def generate_cannonical_schedules(n, matchups, schedules, args, schedule=[]):
    first_round = []

    for i in range(0, n, 2):
        first_round.append((i, i+1))
        matchups.remove((i, i+1))

    # Generate all possible schedules given this cannonical first round
    generate_schedules(n, matchups, schedules, args, first_round)



# Checks if a team in the current matchup is already playing in the current round
def check_repeat(m, current):
    # Also puts the matchup with the team with the lowest index first
    # This prevents duplicate rounds due to order of teams in a round being different
    for p in current:
        if m[0] in p or m[1] in p or m[0] < p[0]:
            return True
    return False


# Function to check if a schedule meets the constraints
def check_constraints(schedule, current, index, n, m):
    round = current + [m]
    prev_round = schedule[-index-(n//2):-index] if len(schedule) >= (n-1) else []
    prev_rounds = [schedule[-index-(n//2*i):-index-(n//2*(i-1))] for i in range(1, 4)] if len(schedule) >= (2*n-1) else []

    # If the last round and this round have a team playing back-to-back, skip this round
    if prevent_back_to_back(round, prev_round) if prev_round else False:
        return True

    # If the last three rounds have a team playing at home or away three times in a row, skip this round
    if prevent_four_in_a_row(round, prev_rounds) if prev_rounds else False:
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
def generate_schedules(n, matchups, schedules, args, schedule=[]):
    # If the maximum number of schedules has been reached, return
    if len(schedules) == args.max or get_count() == args.max:
        return

    # If there are no more matchups, the schedule is complete
    if len(matchups) == 0:
        counter()
        handle_complete_schedule(n, schedule, schedules, args)
        return
    
    # Gets the index to find the matchups in the current round
    index = len(schedule) % (n//2)
    current = schedule[-index:] if index > 0 else []

    # For each round still possible, generate a new schedule
    for m in matchups:
        # Checks if a team is playing in the current round
        if check_repeat(m, current):
            continue

        # Checks if a team plays back to back or a team is on the road or at home more than three times in a row
        if check_constraints(schedule, current, index, n, m):
            continue

        new_matchups = [new_m for new_m in matchups if new_m != m]
        new_schedule = [s for s in schedule] + [m]
                
        # Generate all possible schedules given this round
        generate_schedules(n, new_matchups, schedules, args, new_schedule)