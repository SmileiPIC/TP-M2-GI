#!/bin/bash
#SBATCH --job-name=mpi_openmp
#SBATCH --output=smilei.log
#SBATCH --time=00:20:00
#SBATCH --ntasks=10
#SBATCH --nodes=1 
#SBATCH --cpus-per-task=2
#SBATCH --partition=cpu_short

# available partitions: cpu_short|cpu_med|cpu_prod|cpu_long
# To clean and to load the same modules at the compilation phases
module purge

#module purge
module load anaconda2/2019.10/gcc-9.2.0
module load intel/20.0.2/gcc-4.8.5 intel-mpi/2019.8.254/intel-20.0.2
module load hdf5/1.10.6/intel-19.0.3.199-intel-mpi
export LANG=en_US.utf8
export LC_ALL=en_US.utf8
export I_MPI_CXX=icpc
export HDF5_ROOT_DIR=/gpfs/softs/spack/opt/spack/linux-centos7-cascadelake/intel-19.0.3.199/hdf5-1.10.6-na3ilncuwbx2pdim2xaqwf23sgqza6qo


# echo of commands
set -x

# To compute in the submission directory
cd ${SLURM_SUBMIT_DIR}

# number of OpenMP threads
#export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export OMP_NUM_THREADS=2

# Binding OpenMP Threads of each MPI process on cores
export OMP_PLACES=cores

# Dynamic scheduling of patch-species loops
export OMP_SCHEDULE=dynamic

# execution
# with 'ntasks' MPI processes
# with 'cpus-per-task' OpenMP threads per MPI process
srun ./smilei InputNamelist.py