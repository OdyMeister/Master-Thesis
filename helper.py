import os

COUNT = 0

# Counts the number of times a schedule is completed
def counter(print=False):
    global COUNT
    COUNT += 1
    if print:
        print(COUNT)


# Returns value of the counter
def get_count():
    return COUNT


# Reset the counter
def reset_count():
    global COUNT
    COUNT = 0


# Shows progress of a function
def progress():
    print("#", end="", flush=True)


# Prints the schedules, each round seperated by a new line
def print_schedules(n, schedules, first=20):
    first = min(first, len(schedules)) if first else len(schedules)
    print("First %d possible TTP schedules (out of %d):" % (first, len(schedules)))

    for schedule in schedules[:first]:
        count = 0
        for matchup in schedule:
            print("", matchup, end="")
            count += 1
            if count % (n//2) == 0:
                print()
        print()


# Prints all possible matchups, each row contains 6 matchups for better readability
def print_matchups(matchups, first=20):
    count = 0
    per_row = 6

    first = min(first, len(matchups)) if first else len(matchups)
    print("First %d possible matchups (out of %d):" % (first, len(matchups)))

    for m in matchups[:first]:
        print("", m, end="")
        count += 1
        if count % per_row == 0:
            print()

    if count % per_row != 0:
        print()
    print()


# Generate the path names for the schedules if save is provided
def generate_paths(n, args):
    file_name = args.save + "-" + str(n) + ".csv"
    folder_path = "Schedules_" + args.save
    file_path = folder_path + "/" + file_name
    return file_name, folder_path, file_path


# Initiates saving the schedule to a file if save is provided
def init_save(n, args):
    _, folder, path = generate_paths(n, args)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Clear the file if it already exists
    with open(path, "w") as file:
        file.write("")


# Function which appends the current schedule to the file
def handle_save(n, schedule, args):
    _, _, path = generate_paths(n, args)

    # Append the current schedule to the file
    with open(path, "a") as file:
        file.write(' '.join([str(matchup[0]) + ',' + str(matchup[1]) for matchup in schedule]) + "\n")
        #file.write(' '.join([str(matchup[0]) + ',' + str(matchup[1]) for matchup in schedule]) + "\n")