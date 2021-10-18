# Environment to compile the code Smilei on the cluster Ruche

module purge
module load anaconda2/2019.10/gcc-9.2.0
module load intel/20.0.2/gcc-4.8.5 intel-mpi/2019.8.254/intel-20.0.2
module load hdf5/1.10.6/intel-19.0.3.199-intel-mpi
export LANG=en_US.utf8
export LC_ALL=en_US.utf8
export I_MPI_CXX=icpc
export HDF5_ROOT_DIR=/gpfs/softs/spack/opt/spack/linux-centos7-cascadelake/intel-19.0.3.199/hdf5-1.10.6-na3ilncuwbx2pdim2xaqwf23sgqza6qo