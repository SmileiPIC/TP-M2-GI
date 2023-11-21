######### Validate laser waist evolution in vacuum against Rayleigh law for diffraction
import happi
import numpy as np
import matplotlib.pyplot as plt
import math


####### load simulation
S    = happi.Open(".")

###### conversion factor from 1/k0=lambda0/2pi to um
lambda0           = S.namelist.lambda0*1e6                        # laser wavelength, um 
conversion_factor = lambda0/(2.*math.pi)

####### create grid
dx   = S.namelist.Main.cell_length[0]                             # resolution on the x direction
nx   = S.namelist.Main.number_of_cells[0]                         # number of grid points in the x direction
x    = np.arange(0,(nx+1)*dx,dx)                                  # mesh points in the x direction

Ly   = S.namelist.Lr                                              # simulation window size in the y direction
Diag = S.Probe.Probe1("Env_A_abs",timesteps=0).getData()          # get diagnostic data from timestep = 0
Diag = np.asarray(Diag)                                           # export to numpy array the diagnostic
ny   = np.size(Diag[0,0,:])                                       # number of grid points in the y direction
y    = np.linspace(0.,2.*Ly,num=ny)-Ly                            # mesh points in the x direction

###### array with output timesteps
iters= S.Probe.Probe1("Env_A_abs").getAvailableTimesteps()        # array with the output iterations

######  simulation timestep
dt   = S.namelist.Main.timestep

###### Auxiliary Lists for waist diagnostic
half_waist_simulated  = []				                          # laser transerse size standard deviation, um
waist_analytical      = []  	                                  # waist according to Rayleigh formula, um


###### Auxiliary variables
waist0                = S.namelist.laser_waist  			      # laser initial waisti in normalized units
Zr                    = waist0*waist0/2.                          # Rayileigh length in normalized units
Rayleigh_length       = Zr                                        # Rayleigh length in normalized units
focal_plane           = S.namelist.x_focus                        # position of the laser focal plane in normalized units

###### Loop over iterations in field diagnosic and compute the waist
for iter in iters:
        grid_data = S.Probe.Probe1("Env_A_abs",timesteps=iter)    # get grid data
        grid_data = grid_data.getData()                           # export to numpy array
        grid_data = np.asarray(grid_data)                       
        grid_data = grid_data[0,:,:]
        
        grid_data=np.square(grid_data)                            # envelope squared defined at each grid point
        Total_energy = np.sum( grid_data)                         # total energy of  the laser
        print('reading iteration = '+str(iter) )
        for i in range(0,nx):
                grid_data[i,:] = grid_data[i,:]*y[:]*y[:]
                
        # compute half waist of laser pulse
        half_waist = np.sqrt( np.sum(grid_data) / Total_energy  ) # apply waist formula
        half_waist_simulated.append(  half_waist )
                 
        # analytical waist, Rayleigh formula 
        waist_analytical.append(waist0*math.sqrt(1.+((S.namelist.center_laser+iter*dt-S.namelist.x_focus)/Zr)**2))

waist_analytical= np.asarray(waist_analytical)                
waist_simulated = 2.*np.asarray(half_waist_simulated)

####### Plot
fig = plt.figure()
plt.title("Comparison between simulated \n and theoretical Gaussian bunch diffraction")
fig.set_facecolor('w')
plt.plot(iters*dt*conversion_factor,waist_analytical*conversion_factor,label="theory",color='b',linewidth=2)
plt.plot(iters*dt*conversion_factor,waist_simulated*conversion_factor,label="simulation",linewidth=2,color='r',linestyle="--")
plt.legend(bbox_to_anchor=(0.2, 0.9), loc=2, borderaxespad=0.)
plt.xlabel('x (um)')
plt.ylabel('waist (um)')
plt.xlim(0., np.amax(iters)*dt*conversion_factor)
plt.ylim(waist0*conversion_factor, np.amax(waist_simulated*conversion_factor))
plt.show()




