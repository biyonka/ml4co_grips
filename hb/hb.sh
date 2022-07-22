#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=liang@zib.de
#SBATCH -p small
#SBATCH -t 50:00:00
#SBATCH -n 1
#SBATCH -o hb.log 
#SBATCH --job-name hb_new

python main_scip.py
