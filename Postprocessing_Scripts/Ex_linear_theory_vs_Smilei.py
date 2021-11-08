######### Validate laser wakefield longitudinal electric field against 1D linear theory

import numpy as np
import math
import matplotlib.pyplot as plt
import happi


########################## Preliminary  calculations

########## Constants
c                       = 2.99792e8                      # lightspeed in vacuum,  m/s
epsilon0                = 8.854e-12                      # vacuum permittivity, Farad/m
me                      = 9.109e-31                      # electron mass, kg
q                       = 1.602e-19                      # electron charge, C

########## Open the Simulation
S                       = happi.Open(".")
iter                    = 1000                           # iteration used for the comparison

########## Laser-plasma Params
lambda0                 = 0.8e-6                         # laser central wavelength, m
conversion_factor       = lambda0/2./math.pi*1.e6        # from c/omega0 to um, corresponds to laser wavelength 0.8 um
nc                      = epsilon0*me/q/q*(2.*math.pi/lambda0*c)**2 #critical density in m^-3 for lambda0
n0                      = nc*S.namelist.n0               # plasma density, m^-3  
wp                      = math.sqrt(q**2*n0/epsilon0/me) # plasma frequency, rad/s
kp                      = wp/c                           # plasma wavenumber, rad/m
lambda_p                = 2*math.pi/kp                   # plasma wavelength, m
E0                      = me*wp*c/q                      # cold wavebreaking limit, V/m

########################## Read simulation mesh and fields on grid


########## Read mesh parameters
dx                      = S.namelist.Main.cell_length[0]*conversion_factor*1.e-6
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


# Auxiliaty quantities for the comparison
x_mesh                  = np.arange(0,(Nx)*dx,dx)
Nx                      = np.size(x_mesh)
Ex_analytical           = np.zeros(Nx)

########################## Validation


######### Compute Ex with integral of convolution with Green's function cos[kp(x)], trapezoidal rule for the integral (remember that source term is zero at the beginning of the interval)
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
plt.plot(np.multiply(x_mesh,1e6),np.multiply(Ex_analytical,1e-9),'-b',linewidth=2.,label='theory')
plt.plot(np.multiply(x_mesh,1e6),np.multiply(Ex_SMILEI,(1.e-9*me*c**2/conversion_factor/1.e-6/q)),'--r',linewidth=2.,label='simulation')
plt.ylabel('Ex (GV/m)')
plt.xlabel('x (um)')
plt.xlim(1.,50)
plt.ylim(-0.007,0.007)
plt.legend()
plt.show()