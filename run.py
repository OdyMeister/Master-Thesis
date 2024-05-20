from TTP import *
from helper import *
import sys
import argparse


# Main function to generate all possible TTP schedules
def generate_TTP(n, args=None):
    schedules = []
    matchups = []
    streaks = {}

    # Create the folder path if save is provided
    if args.save != None:
        _, folder, path = generate_paths(n, args)

        # Create the folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Clear the file if it already exists
        with open(path, "w") as file:
            file.write("")

    # Generate all possible matchups given n teams
    generate_matchups(n, matchups)
    if args.verbose != None:
        print_matchups(matchups, args.verbose)

    # Fills the streaks dict with the number of home/away games for each team
    # and the number of back-to-back games counter
    generate_streak_count(n, streaks)

    # Generate all possible schedules given all possible rounds
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


# Function to validate the arguments and their values
def validate_arguments(args):
    # Check if n_end is provided, if not set it equal to n_start
    if args.n_end == None:
        args.n_end = args.n_start

    # Check if n_start or n_end is odd, TTP is only possible for even n
    if args.n_start % 2 != 0 or args.n_end % 2 != 0:
        print("Number of teams must be even")
        sys.exit(1)
    # Check if n_start is less than n_end
    elif args.n_start > args.n_end:
        print("n_start must be less than or equal to n_end")
        sys.exit(1)
    # Check if n_start is less than 4, TTP is only possible for n >= 4
    elif args.n_start < 4:
        print("Number of teams must be greater than or equal to 4")
        sys.exit(1)
    # Check if verbose is less than or equal to 0
    elif args.verbose != None and args.verbose < 0:
        print("Verbose must be greater than or equal to 0")
        sys.exit(1)
    # Check if count is less than 0
    elif args.count and args.count < 0:
        print("Count must be greater than or equal to 0")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate all possible TTP schedules for n teams")
    # Required arguments
    parser.add_argument("n_start", type=int, help="Number of teams")
    parser.add_argument("n_end", type=int, nargs="?", help="Number of teams")
    # Optional boolean arguments
    parser.add_argument("-c", "--cannonical", action="store_true", help="Generate cannonical schedules")
    parser.add_argument("-p", "--parallel", action="store_true", help="Enable parallel processing") # Not implemented
    # Optional arguments with values
    parser.add_argument("-v", "--verbose", type=int, help="Prints first VERBOSE rounds of all schedules, possible rounds and matchups\nSet to 0 to print all schedules, rounds and matchups")
    parser.add_argument("--count", type=int, help="Print the count of schedules generated\nEvery COUNT schedules, the count is printed\nSet to 0 to only print the final count")
    parser.add_argument("-m", "--max", type=int, help="Maximum number of schedules to generate")
    parser.add_argument("-s", "--save", type=str, help="Save the schedules to a file")
    args = parser.parse_args()

    # Validate the arguments
    validate_arguments(args)

    # Run generate_TTP for each n in the range
    for n in range(args.n_start, args.n_end + 1, 2):
        if args.verbose:
            print(f"\nGenerating TTP schedules for {n} teams")
        generate_TTP(n, args)