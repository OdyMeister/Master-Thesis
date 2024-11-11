import multiprocessing as mp
from itertools import  permutations
import numpy as np

def gen_permutations(x):
    return list(permutations(x))

if __name__ == '__main__':
    data = [0,1,2]

    pool = mp.Pool(mp.cpu_count())

    chunks = [np.delete(data, i) for i in range(len(data))]

    result = pool.map(gen_permutations, chunks)

    pool.close()
    pool.join()

    for i in range(len(result)):
        for j in range(len(result[i])):
            print(i, end=' ')
            for e in result[i][j]:
                print(e, end=' ')
            print()