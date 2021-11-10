import happi
import numpy as np
import scipy.constants
import math 

############ read the outputs files
S = happi.Open()

############ the iteration you want to export
timestep = 1000

########### Some conversion factors

## Physical constants
lambda0             = S.namelist.lambda0        # laser wavelength, m
c                   = scipy.constants.c         # lightspeed, m/s
omega0              = 2*math.pi*c/lambda0       # laser frequency
eps0                = scipy.constants.epsilon_0 # Vacuum permittivity, F/m
e                   = scipy.constants.e         # Elementary charge, C
me                  = scipy.constants.m_e       # Electron mass, kg
ncrit               = eps0*omega0**2*me/e**2    # Plasma critical number density [m-3]
c_over_omega0       = lambda0/2./math.pi        # converts from c/omega0 units to m
reference_frequency = omega0                    # reference frequency (s-1)
E0                  = me*omega0*c/e             # reference electric field (V/m)

# conversion factors - command for conversion: array_SI = np.multiply(array_normalized,conversion_factor)

length_to_um        = c_over_omega0*1.e6                             # (for lenghts  )
E_field_to_GV_ov_m  = E0/1.e9                                        # (for E fields )
time_to_fs          = 1./omega0*1.e15                                # (for time     )
charge_to_pC        = e * ncrit * (c_over_omega0*1e-6)**3 * 10**(12) # (for charges  )
Lorentz_fact_to_MeV = 0.51099895                                     # (for energies )
density_to_cm_minus3= ncrit/1.e6                                     # (for densities)


############ Export the x axis
x_mesh = np.linspace(0.,S.namelist.Lx,num=S.namelist.nx)
np.savetxt("x_mesh.txt",x_mesh.T)


############ Export the y axis (all the plane)
y_mesh = np.linspace(-S.namelist.Lr,S.namelist.Lr,num=2*S.namelist.nr)
np.savetxt("y_mesh.txt",y_mesh.T)


############ Export 1D Probe, instert the field you want to export
my_1D_array = S.Probe.Probe0("Ex",timesteps=timestep).getData()
my_1D_array = np.asarray(my_1D_array)

# choose a filename
filename1D = "Ex_1D.txt"
# export the 1D data as single column file 
np.savetxt(filename1D,my_1D_array.T)


############ Export 2D Probe, instert the field you want to export
my_2D_array = S.Probe.Probe1("Ex",timesteps=timestep).getData()
my_2D_array = np.asarray(my_2D_array)[0,:,:]

# choose a filename
filename2D = "Ex_2D.txt"
# export the 2D data as file containing a 2D matrix 
np.savetxt(filename2D,my_2D_array.T)

########### Export particles data of the electron bunch
species_name           = "electronbunch"
chunk_size             = 60000
track_part             = S.TrackParticles(species = species_name, chunksize=chunk_size, sort=False)

# choose filename
filename_particle_data = "Particles_iter_"+str(timestep)+".txt"
# read particle data
for particle_chunk in track_part.iterParticles(timestep, chunksize=chunk_size):
	### Read particles arrays with positions and momenta
	# positions, normalized by c/omega0
	x            = particle_chunk["x"]
	y            = particle_chunk["y"]
	z            = particle_chunk["z"]
	# momenta, normalized by m_e*c
	px           = particle_chunk["px"]
	py           = particle_chunk["py"]
	pz           = particle_chunk["pz"]
	
	w            = particle_chunk["w"] # normalized charge

# export to file with 7 columns: normalized x,y,z,px,py,pz,w
np.savetxt(filename_particle_data,zip(x,y,z,px,py,pz,w))
