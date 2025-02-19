######### Validate laser wakefield longitudinal electric field against 1D linear theory

import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.constants
import happi

########################## Preliminary  calculations

########## Constants
c                       = scipy.constants.c              # lightspeed in vacuum         , m/s
epsilon0                = scipy.constants.epsilon_0      # vacuum permittivity          , F/m
me                      = scipy.constants.m_e            # electron mass                , kg
q                       = scipy.constants.e              # electron charge             , C

########## Open the Simulation
S                       = happi.Open(".")
iter                    = 2000                           # iteration used for the comparison

########## Variables used for conversions
lambda0                 = S.namelist.lambda0             # laser central wavelength    , m
nc                      = S.namelist.ncrit               # critical density for lambda0, m^-3
n0                      = nc*S.namelist.n0               # plasma density              , m^-3  
wp                      = math.sqrt(q**2*n0/epsilon0/me) # plasma frequency            , rad/s
kp                      = wp/c                           # plasma wavenumber           , rad/m
lambda_p                = 2*math.pi/kp                   # plasma wavelength           , m
E0                      = me*wp*c/q                      # cold wavebreaking limit     , V/m

########################## Read simulation mesh and fields on grid

########## Read mesh parameters
dx                      = S.namelist.Main.cell_length[0]*S.namelist.c_over_omega0 # cell size along x, m
dx_prime                = dx
Nx                      = S.namelist.nx

# Read laser envelope |A| on axis
Diag                    = S.Probe.Probe0("Env_A_abs",timesteps=iter)
A_abs_val_SMILEI        = Diag.getData()
A_abs_val_SMILEI        = np.asarray(A_abs_val_SMILEI)
A_abs_val_SMILEI        = A_abs_val_SMILEI[0,:]

# Read longitudinal electric field Ex on axis                 
Diag                    = S.Probe.Probe0("Ex",timesteps=iter)
Ex_SMILEI               = Diag.getData()
Ex_SMILEI               = np.asarray(Ex_SMILEI)
Ex_SMILEI               = Ex_SMILEI[0,:]

# Auxiliary quantities for the comparison
x_mesh                  = np.arange(0,(Nx)*dx,dx)
Nx                      = np.size(x_mesh)
Ex_analytical           = np.zeros(Nx)

########################## Validation


######### Compute Ex with integral of convolution with Green's function cos[kp(x)], 
######### trapezoidal rule for the integral (remember that source term is zero at the beginning of the interval)
for i in range(Nx-2,1,-1):
	for i_prime in range(Nx-2,i,-1):
		if (i_prime == i): 
			Ex_analytical[i]   = Ex_analytical[i] + me*c**2/q*kp**2/4*0.25*(A_abs_val_SMILEI[i_prime]+A_abs_val_SMILEI[i_prime+1])**2*math.cos(kp*(x_mesh[i]-x_mesh[i_prime])  )*dx_prime/2
		else:
			Ex_analytical[i]   = Ex_analytical[i] + me*c**2/q*kp**2/4*0.25*(A_abs_val_SMILEI[i_prime]+A_abs_val_SMILEI[i_prime+1])**2*math.cos(kp*(x_mesh[i]-x_mesh[i_prime])  )*dx_prime
           

######## Plot
fig=plt.figure()
plt.title("Comparison between simulated \n and theoretical 1D linear laser wakefield")
fig.set_facecolor('w')
plt.plot(x_mesh/1e-6,Ex_analytical/1e9,'-b',linewidth=2.,label='theory')
plt.plot(x_mesh/1e-6,Ex_SMILEI*S.namelist.E0/1e9,'--r',linewidth=2.,label='simulation')
plt.ylabel('Ex (GV/m)')
plt.xlabel('x (um)')
plt.xlim(1.,50)
plt.ylim(-0.007,0.007)
plt.legend()
plt.show()