#!/bin/bash
#PBS -l nodes=1:ppn=24
#PBS -q default
#PBS -j oe

#Set the correct modules available (see environment configuration)

. /usr/share/Modules/init/bash

source /usr/share/Modules/init/bash #Set the correct modules available
unset MODULEPATH; module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7

#Load compilers
module load compilers/icc/17.4.196 # for centos7
module load mpi/openmpi/4.1.1-ib-icc
module load hdf5/1.10.5-icc-omp4.1.1
module load python/3.7.0
module load compilers/gcc/4.9.2
module load h5py/hdf5_1.10.5-icc-omp4.1.1-py3.7.0


export OMPI_CC=icc
export OMPI_CXX=icpc
export OMPI_F90=ifort
export OMPI_F77=ifort
export OMPI_FC=ifort
export CC=mpicc
export CXX=mpicxx
export FC=mpif77


export PS1="\A \u \[\033[01;34m\]\h:\w\[\033[01;31m\] > \[\033[00m\]"



#Go to current directory
cd $PBS_O_WORKDIR

# -bind-to-core to fix a given MPI process to a fixed set of cores.
export OMP_NUM_THREADS=12
export OMP_SCHEDULE=DYNAMIC


export KMP_AFFINITY=granularity=fine,compact,1,0

export PATH=$PATH:/opt/exp_soft/vo.llr.in2p3.fr/GALOP/beck

#Specify the number of sockets per node in -mca orte_num_sockets
#Specify the number of cores per sockets in -mca orte_num_cores
mpirun -mca orte_num_sockets 2 -mca orte_num_cores 12  -map-by ppr:1:socket:pe=12 -n 2 -x OMP_NUM_THREADS -x OMP_SCHEDULE ./smilei InputNamelist.py 2>&1 | tee smilei.log

