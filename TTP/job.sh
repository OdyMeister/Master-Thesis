#!/bin/bash
#Set job requirements
#SBATCH -t 120:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --partition=rome

#Loading modules
module load 2022
#module load Python/3.10.4-GCCore-11.3.0

# Run the python script
python3 run.py --count=100000 -N 8 16
