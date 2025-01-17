########## Purpose: print the evolution of the electron bunch parameters over the simulation
########## Use (from the simulation folder): python Follow_electron_bunch_evolution.py


########## loading libraries
import os,sys
import happi
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants

########## Open the simulation

S          = happi.Open(".", show=False)

########## Constants
c                       = scipy.constants.c              # lightspeed in vacuum,  m/s
epsilon0                = scipy.constants.epsilon_0      # vacuum permittivity, Farad/m
me                      = scipy.constants.m_e            # electron mass, kg
q                       = scipy.constants.e              # electron charge, C
electron_mass_MeV       = scipy.constants.physical_constants["electron mass energy equivalent in MeV"][0]


########## Species name
species_name            = "electronbunch"

########## Variables used for conversions
lambda0                 = S.namelist.lambda0             # laser central wavelength, m
um                      = S.namelist.um                  # 1 micron in normalized units             
nc                      = S.namelist.ncrit               # critical density in m^-3 for lambda0
n0                      = nc*S.namelist.n0               # plasma density, m^-3  



########## Auxiliary functions
def weighted_std(values, weights):
    """
    Return the weighted standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    variance = np.average((values-average)**2, weights=weights)
    return math.sqrt(variance)

def weighted_covariance(values1, values2, weights):
    """
    Return the weighted covariance

    values1, values2 weights -- Numpy ndarrays with the same shape.
    """
    average1 = np.average(values1, weights=weights)
    average2 = np.average(values2, weights=weights)
    # Fast and numerically precise:
    covariance = np.average((values1-average1)*(values2-average2), weights=weights)
    return covariance

def normalized_emittance(transv_coordinate,transv_momentum,weights):
    sigma_transv          = weighted_std(transv_coordinate, weights)
    sigma_p_transv        = weighted_std(transv_momentum, weights)
    sigma_transv_p_transv = weighted_covariance(transv_coordinate,transv_momentum,weights)
    norm_emittance        = (sigma_transv**2)*(sigma_p_transv**2)-sigma_transv_p_transv**2
    return math.sqrt(norm_emittance) 

########## Open the DiagTrackParticles

chunk_size = 60000

track_part = S.TrackParticles(species = species_name, chunksize=chunk_size, sort=False)

print (" ")
print ("Reading simulation from "+str(os.getcwd()))
print (" ")

iters = track_part.getAvailableTimesteps()

######### Define the auxiliary arrays
bunch_position= np.zeros(np.size(iters))
Sigma_y       = np.zeros(np.size(iters))
Sigma_z       = np.zeros(np.size(iters))
Energy        = np.zeros(np.size(iters))
Energy_spread = np.zeros(np.size(iters))
Emittance_y   = np.zeros(np.size(iters))
Emittance_z   = np.zeros(np.size(iters))
Divergence_y  = np.zeros(np.size(iters))
Divergence_z  = np.zeros(np.size(iters))

######### Read the DiagTrackParticles data, for each available timestep
i = 0
for timestep in iters:
	for particle_chunk in track_part.iterParticles(timestep, chunksize=chunk_size):
		### Read particles arrays with positions and momenta
		# positions
		x            = particle_chunk["x"]
		y            = particle_chunk["y"]
		z            = particle_chunk["z"]
		# momenta
		px           = particle_chunk["px"]
		py           = particle_chunk["py"]
		pz           = particle_chunk["pz"]
		w            = particle_chunk["w"]
		#w            = np.ones(np.shape(x))*S.namelist.weight                 # Particles weights
		p            = np.sqrt((px**2+py**2+pz**2))                            # Particles Momentum 
		E            = np.sqrt((1.+p**2))                                      # Particles energy
		
# 		Nparticles   = np.size(w)                                              # Number of particles read   	
# 		total_weight = w.sum()
# 		Q            = total_weight* q * nc * (S.namelist.c_over_omega0)**3 * 10**(12) # Total charge in pC
# 		print(" ")
# 		print("Total charge = ",Q," pC")
# 		print(" ")
		
		### Save the bunch parameters
		bunch_position[i]= np.average(x,weights=w)/um           # um
		Sigma_y[i]       = weighted_std(y,w)/um                 # um
		Sigma_z[i]       = weighted_std(z,w)/um                 # um
		Energy[i]        = np.average(E,weights=w)              # normalized
		Energy_spread[i] = weighted_std(E,w)/Energy[i]*100      # %
		Energy[i]        = Energy[i]*electron_mass_MeV          # MeV
		Emittance_y[i]   = normalized_emittance(y,py,w)/um      # mm-mrad
		Emittance_z[i]   = normalized_emittance(z,pz,w)/um      # mm-mrad

		i = i + 1
		
		del x,y,z,px,py,pz,w,p,E
		
######### Plot
	
fig = plt.figure(figsize=(12,4))
plt.title("Evolution of the Electron Bunch Parameters")
fig.set_facecolor('w')


plt.subplot(131)
plt.plot(bunch_position/1e3,Sigma_y,c="b",label="y")
plt.plot(bunch_position/1e3,Sigma_z,c="r",linestyle="--",label="z")
plt.xlabel("x [mm]")
plt.ylabel("Rms Transverse Size\n[um]")
plt.ylim(0,2.5)
plt.xticks([0.,0.1,0.2,0.3,0.4,0.5])
plt.legend()
plt.grid("on")

plt.subplot(132)
plt.plot(bunch_position/1e3,Emittance_y,c="b",label="y")
plt.plot(bunch_position/1e3,Emittance_z,c="r",linestyle="--",label="z")
plt.xlabel("x [mm]")
plt.ylabel("Normalized Emittance\n[mm-mrad]")
plt.ylim(0,3.2)
plt.xticks([0.,0.1,0.2,0.3,0.4,0.5])
plt.legend()
plt.grid("on")

plt.subplot(133)
plt.plot(bunch_position/1e3,Energy,c="b")
plt.xlabel("x [mm]")
plt.ylabel("Energy\n[MeV]")
plt.xticks([0.,0.1,0.2,0.3,0.4,0.5])
plt.grid("on")

plt.subplots_adjust(hspace=2.,wspace=0.4)

plt.savefig('Electron_bunch_evolution.png', format='png')
plt.show()