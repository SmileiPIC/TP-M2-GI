########## Purpose: print the electron bunch parameters at timestep =  iter
########## Use (from the simulation folder): python Compute_bunch_parameters.py iter 


########## loading libraries
import os,sys
import happi
import math
import numpy as np
from sys import exit
import scipy.constants

########## Read the input and open the simulation
inputs     = sys.argv
timestep   = int(inputs[1])                              # the iteration to analyze

S          = happi.Open(".", show=False)

########## Constants
c                       = scipy.constants.c              # lightspeed in vacuum,  m/s
epsilon0                = scipy.constants.epsilon_0      # vacuum permittivity, Farad/m
me                      = scipy.constants.m_e            # electron mass, kg
q                       = scipy.constants.e              # electron charge, C

########## Species name
species_name            = "electronbunch"

########## Laser-plasma Params
lambda0                 = S.namelist.lambda0              # laser central wavelength, m
conversion_factor       = lambda0/2./math.pi*1.e6        # from c/omega0 to um, corresponds to laser wavelength 0.8 um
nc                      = epsilon0*me/q/q*(2.*math.pi/lambda0*c)**2 #critical density in m^-3 for lambda0

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

def print_bunch_params(x,y,z,px,py,pz,E,weights,conversion_factor):
    # conversion factor converts from normalized units to um
    print("average position = ",np.average(x,weights=weights)*conversion_factor," um")
    print("----------------")
    print("")
    print("sigma_x   = ",weighted_std(x,weights)*conversion_factor," um")
    print("sigma_y   = ",weighted_std(y,weights)*conversion_factor," um")
    print("sigma_z   = ",weighted_std(z,weights)*conversion_factor," um")
    print("E         = ",np.average(E,weights=weights)*0.511," MeV")
    print("DE/E(rms) = ",weighted_std(E,weights)/np.average(E,weights=weights)*100, "%")
    print("eps_ny    = ",normalized_emittance(y,py,weights)*conversion_factor," mm-mrad")
    print("eps_nz    = ",normalized_emittance(z,pz,weights)*conversion_factor," mm-mrad")
    print("")
    print("sigma_i (i=x,y,z): rms size along the coordinate i")
    print("E                : mean energy")
    print("DE/E (rms)       : relative rms energy spread")
    print("eps_ni (i=y,z)   : normalized emittance (phase space plane i-p_i)")
    print("")
    print("----------------")

########## Open the DiagTrackParticles

chunk_size = 60000

track_part = S.TrackParticles(species = species_name, chunksize=chunk_size)

if (timestep not in track_part.getAvailableTimesteps()):
	print(" ")
	print("Selected timestep not available in the DiagTrackParticles output")
	print("Available timesteps = ",track_part.getAvailableTimesteps())
	print(" ")
	exit()


print(" ")
print("Reading timestep ",timestep,"from ",os.getcwd())

# Read the DiagTrackParticles data
for particle_chunk in track_part.iterParticles(timestep, chunksize=chunk_size):
	### Read particles arrays with positions and momenta
        
    # positions
    x            = particle_chunk["x"]
    y            = particle_chunk["y"]
    z            = particle_chunk["z"]
    # moments
    px           = particle_chunk["px"]
    py           = particle_chunk["py"]
    pz           = particle_chunk["pz"]
    w            = particle_chunk["w"]
    #w            = np.ones(np.shape(x))*S.namelist.weight               # Particles weights
    p            = np.sqrt((px**2+py**2+pz**2))                         # Particles Momentum 
    E            = np.sqrt((1.+p**2))                                   # Particles energy
        
    Nparticles   = np.size(w)                                           # Number of particles read
    print(" ")
    print("Read ",Nparticles," particles from the file")
    print(" ")
    total_weight = w.sum()
    Q            = total_weight* q * nc * (conversion_factor*1e-6)**3 * 10**(12) # Total charge in pC
    print(" ")
    print("Total charge = ",Q," pC")

    ### Print the bunch parameters
    print_bunch_params(x,y,z,px,py,pz,E,w,conversion_factor)

    