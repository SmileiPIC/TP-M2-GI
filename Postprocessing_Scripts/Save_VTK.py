import happi
import os,sys
import numpy as np


# Use: python Save_VTK.py iteration
# takes data from a simulation in data_folder, iteration specified at input and writes the vtk in the folder from which this script is used

iteration = sys.argv[1]
data_folder = os.getcwd() 
vtk_folder  = os.getcwd()

# 3D Cartesian space interval where the cylindrical data are reconstructed
# format: [ [x_min,x_max,dx], [y_min,y_max,dy] [z_min,z_max,dz] ]
build3d_interval_Rho = [[0.,400.,0.8],[-140,140,1.5],[-140,140,1.5]]
build3d_interval_E = [[0.,400,0.8],[-140,140,1.5],[-140,140,1.5]]


#### Read the data
S = happi.Open(data_folder)
timesteps = S.Field.Field0("Env_E_abs",theta=0).getAvailableTimesteps()
timesteps = timesteps.tolist()

if iteration not in timesteps:
	print("Selected iteration not available")
	print("Available iterations:")
	print(timesteps)
	sys.exit()

### Read data and export to vtk
os.chdir(vtk_folder)

# export laser field
for timestep in mytimesteps:
	print("Reading iteration ",timesteps.index(timestep)," of ",len(timesteps))
	E = S.Field.Field0("Env_E_abs",timesteps=timestep,build3d=build3d_interval_E)
	E.toVTK()
	del(E)
	print("Env_E exported")

	# export plasma electron density
	Rho_plasma = S.Field.Field1("-Rho_plasmaelectrons",timesteps=timestep,build3d=build3d_interval_Rho)
	Rho_plasma.toVTK()
	del(Rho_plasma)
	print("Rho_plasma exported")

	# export electron bunch density
	Rho_bunch = S.Field.Field1("-Rho_electronbunch",timesteps=timestep,build3d=build3d_interval_Rho)
	Rho_bunch.toVTK()
	del(Rho_bunch)
	print("Rho_bunch exported")
	os.system(write_file_command)
