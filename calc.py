import math

# Calculate the number of possible rounds for a given number of teams
def calc_rounds(n):
    return math.factorial(n) // math.factorial(n//2)

# Calculate the number of possible matchups for a given number of teams
def calc_matchups(n):
    return n**2 - n

# Calculate the number of possible Double Round Robbin schedules for a given number of teams
def calc_drr_schedules(n):
    return math.factorial(calc_rounds(n)) // math.factorial(calc_rounds(n) - (n-1)*2)

if __name__ == "__main__":
    for n in range(4, 51, 2):
        #print(f"Teams: {n}\t Matchups: {calc_matchups(n)}\t Rounds: {calc_rounds(n)}")
        print(f"Teams: {n}\t DRR Schedules: {calc_drr_schedules(n)}")