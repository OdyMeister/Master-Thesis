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


# Generate all possible cannonical schedules given all possible rounds
def generate_cannonical_schedules(n, rounds, schedules, args, schedule=[]):
    # Picks a round to be the first cannonoical round
    first_round = rounds.pop()
    new_rounds = []

    # Remove rounds with duplicate matchups which occur in the first round
    remove_duplicates(first_round, rounds, new_rounds)

    # Generate all possible schedules given this cannonical first round
    generate_schedules(n, new_rounds, schedules, args, [first_round])


# Generate all possible schedules given all possible rounds
def generate_schedules(n, rounds, schedules, args, schedule=[]):
    #print(f"rounds: {len(rounds)}, schedules: {len(schedules)}, schedule: {len(schedule)}", flush=True)

    # If the schedule is complete, add it to the list of schedules
    if len(schedule) == (n - 1) * 2:
        if args and args.count:
            counter()
            if args.count!= 0 and get_count() % args.count == 0:
                print("Current schedule count:",get_count())
        if args and args.verbose:
            schedules.append(schedule)
        return

    # For each round still possible, generate a new schedule
    for round in rounds:
        # If the last round and this round have a team playing back-to-back, skip this round
        if prevent_back_to_back(round, schedule[-1]) if schedule else False:
            continue

        # If the last three rounds have a team playing at home or away three times in a row, skip this round
        if prevent_four_in_a_row(round, schedule[-3:]) if len(schedule) >= 3 else False:
            continue

        new_rounds = []
        new_schedule = schedule.copy()
        new_schedule.append(round)

        # Remove rounds with duplicate matchups which occur in this round
        remove_duplicates(round, rounds, new_rounds)
        
        # Generate all possible schedules given this round
        generate_schedules(n, new_rounds, schedules, args, new_schedule)