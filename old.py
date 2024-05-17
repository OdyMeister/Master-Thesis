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


# Generate all possible schedules given all possible rounds
def generate_schedules_rounds(n, rounds, schedules, args, schedule=[]):
    # If the maximum number of schedules has been reached, return
    if args and (len(schedules) == args.max or get_count() == args.max):
        return

    # If the schedule is complete, add it to the list of schedules
    if len(schedule) == (n - 1) * 2:
        if args and args.count != None:
            counter()
            if args.count != 0 and get_count() % args.count == 0:
                print("Current schedule count:",get_count())
        if args and args.verbose != None:
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