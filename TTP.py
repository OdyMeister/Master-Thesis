from debug import *
import sys


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


# Generate all possible cannonical schedules given all possible rounds
def generate_cannonical_schedules(n, rounds, schedules, args, schedule=[]):
    # Picks a round to be the first cannonoical round
    first_round = rounds.pop()
    new_rounds = []

    # Remove rounds with duplicate matchups which occur in the first round
    remove_duplicates(first_round, rounds, new_rounds)

    # Generate all possible schedules given this cannonical first round
    generate_schedules(n, new_rounds, schedules, args, [first_round])


# Generate all possible schedules given all possible matchups
def generate_schedules(n, matchups, schedules, args, schedule=[]):
    # If the maximum number of schedules has been reached, return
    if args and (len(schedules) == args.max or get_count() == args.max):
        return

    # If the schedule is complete, add it to the list of schedules
    if len(matchups) == 0:
        if args and args.count != None:
            counter()
            if args.count != 0 and get_count() % args.count == 0:
                print("Current schedule count:", get_count())
        if args and args.verbose != None:
            schedules.append(schedule)
        return
    
    # Gets the index to find the matchups in the current round
    index = len(schedule) % (n//2)
    current = schedule[-index:] if index > 0 else []

    # For each round still possible, generate a new schedule
    for m in matchups:
        repeat = False

        # Checks if a team in the current matchup is already playing in the current round
        # Also puts the matchup with the team with the lowest index first, this prevents duplicate rounds
        for p in current:
            if m[0] in p or m[1] in p or m[0] < p[0]:
                repeat = True
                break
        
        # If the repeat occured, skip this matchup
        if repeat:
            continue

        # Checks whether the current round is complete
        if len(current) + 1 == n//2:
            round = current + [m]
            prev = schedule[-index-3:-index] if len(schedule) >= (n-1) else [] # TODO: Check this, should take previous round
            # TODO: Also get the three previous rounds

            # # If the last round and this round have a team playing back-to-back, skip this round
            # if prevent_back_to_back(round, prev) if prev else False:
            #     continue

            # # If the last three rounds have a team playing at home or away three times in a row, skip this round
            # if prevent_four_in_a_row(round, schedule[-3:]) if len(schedule) >= 3 else False:
            #     continue

        new_matchups = matchups.copy()
        new_matchups.remove(m)
        new_schedule = schedule.copy()
        new_schedule.append(m)
        
        # Generate all possible schedules given this round
        generate_schedules(n, new_matchups, schedules, args, new_schedule)