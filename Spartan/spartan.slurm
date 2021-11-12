#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=0-1:00:00

module load foss/2019b
module load python/3.7.4
module load textblob/0.15.3
module load Shapely/1.7.1

time srun -n 1 python3 extractor.py