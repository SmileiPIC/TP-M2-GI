######### Validate laser waist evolution in vacuum against Rayleigh law for diffraction
import happi
import numpy as np
import matplotlib.pyplot as plt
import math


####### load simulation
S                     = happi.Open()

###### Auxiliary variables
um                    = S.namelist.um                                       # 1 um in normalized units
c_normalized          = S.namelist.c_normalized                             # normalized speed of light

####### Create grid in the transverse direction
Ly                    = S.namelist.Lr                                       # simulation window size in the y direction
Diag                  = S.Probe.Probe1("Env_A_abs",timesteps=0).getData()   # get diagnostic data from timestep = 0
Diag                  = np.asarray(Diag)                                    # export to numpy array the diagnostic
ny                    = np.size(Diag[0,0,:])                                # number of grid points in the y direction
y                     = np.linspace(-Ly,Ly,num=ny)                          # mesh points in the x direction

####### Simulation timestep
dt                    = S.namelist.dt

####### Array with output timesteps
iters                 = S.Probe.Probe1("Env_A_abs").getAvailableTimesteps() # array with the output iterations

###### Extract laser parameters
waist0                = S.namelist.laser_waist  			                 # laser initial waisti in normalized units
Zr                    = waist0*waist0/2.                                     # Rayileigh length in normalized units
Rayleigh_length       = Zr                                                   # Rayleigh length in normalized units
focal_plane           = S.namelist.x_focus                                   # position of the laser focal plane in normalized units

###### Loop over iterations in Probe diagnosic and compute the simulated and analytical waist

waist_simulated       = []				                                     # laser transerse size standard deviation, normalized units
waist_analytical      = []  	                                             # waist according to Rayleigh formula, normalized units

for iter in iters:
    
    # get |Env_A| on the xy plane, export to numpy array      
    Env_A_abs         = np.asarray(S.Probe.Probe1("Env_A_abs",timesteps=iter).getData())
    
    # compute the intensity at this iteration as |Env_A|^2 
        
    intensity         = np.square(Env_A_abs[0,:,:])                         
    # apply waist integral formula
    waist             = np.sqrt( np.sum(intensity*np.square(y)[np.newaxis,:])/np.sum(intensity ) ) 
    waist_simulated.append( 2*waist )
    
    # analytical waist, Rayleigh formula 
    waist_analytical.append(waist0*math.sqrt(1.+((S.namelist.center_laser+iter*dt-S.namelist.x_focus)/Zr)**2))

waist_analytical      = np.asarray(waist_analytical)                
waist_simulated       = np.asarray(waist_simulated)

####### Plot
fig = plt.figure()
plt.title("Comparison between simulated \n and theoretical Gaussian bunch diffraction")
fig.set_facecolor('w')
plt.plot(iters*c_normalized*dt/um,waist_analytical/um,label="theory",color='b',linewidth=2)
plt.plot(iters*c_normalized*dt/um,waist_simulated/um,label="simulation",linewidth=2,color='r',linestyle="--")
plt.legend(bbox_to_anchor=(0.2, 0.9), loc=2, borderaxespad=0.)
plt.xlabel('x (um)')
plt.ylabel('waist (um)')
plt.xlim(0., np.amax(iters)*c_normalized*dt/um)
plt.ylim(0.99*waist0/um, np.amax(waist_simulated/um))
plt.show()




