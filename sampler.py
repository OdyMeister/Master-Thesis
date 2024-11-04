import numpy as np
from TTP import generate_matchups

def generete_random_schedule(n):
    matchups = []
    schedule = [[(0,0) for i in range(n//2)] for j in range(2*(n-1))]
    indexes = [(i,j) for i in range(n//2) for j in range(2*(n-1))]
    
    generate_matchups(n, matchups)

