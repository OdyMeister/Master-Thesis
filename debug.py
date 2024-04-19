COUNT = 0

# Debugging function to count the number of times a function is called
def counter(print=True):
    global COUNT
    COUNT += 1
    if print:
        print(COUNT)


# Debugging function to print the count if counter() is not continually printing
def print_count():
    print(COUNT)


# Debugging function to show progress of a function
def progress():
    print("#", end="", flush=True)


# Debugging function to print the schedules
def print_schedules(n, schedules, first=20):
    print("First %d possible TTP schedules (out of %d) for %d teams:" % (first, len(schedules), n))
    for schedule in schedules[:first]:
        print("", schedule)


# Debugging function to print the all possible rounds
def print_rounds(rounds, first=20):
    first = min(first, len(rounds))
    print("First %d possible rounds (out of %d):" % (first, len(rounds)))
    for r in list(rounds)[:first]:
        print("", tuple(r))


# Debugging function to print the all possible matchups
def print_matchups(matchups, first=20):
    first = min(first, len(matchups))
    print("First %d possible matchups (out of %d):" % (first, len(matchups)))
    for m in matchups[:first]:
        print("", m)

