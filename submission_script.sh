#!/bin/bash
#SBATCH --job-name=smilei
#SBATCH --nodes=1
#SBATCH --output=smilei.out
#SBATCH --error=smilei.err
#SBATCH --time=00:10:00
#SBATCH --ntasks=4           # number of MPI processes
#SBATCH --cpus-per-task=5    # number of threads per MPI process

#source /gpfs/workdir/labotm/miniconda3/smilei_env.sh
source /gpfs/workdir/labotm/Installations/miniconda3/smilei_env.sh

# Dynamic scheduling for patch-spec loop
export OMP_SCHEDULE=dynamic
# number of OpenMP threads per MPI process
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
# Binding OpenMP Threads of each MPI process on cores
export OMP_PLACES=cores


cp ${WORKDIR}/Smilei/smilei .
cp ${WORKDIR}/Smilei/smilei_test .

set -x
cd ${SLURM_SUBMIT_DIR}

srun ./smilei InputNamelist.py