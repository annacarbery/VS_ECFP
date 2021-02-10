#!/bin/bash
# My Script that contains the commands I want to run
# Arguments I want to give to qsub:
# Essentially requires 1Gb of RAM and expects to run for 1 minute h_cpu=h:m:s
#$ -cwd
#$ -j y
#$ -N ECFP
#$ -q medium.q
#$ -o /dls/science/users/tyt15771/DPhil/VS_ECFP/cluster.out
#$ -l h_cpu=0:3:0,mem_free=1G

conda activate VS_ECFP
python /dls/science/users/tyt15771/DPhil/VS_ECFP/get_pairs.py