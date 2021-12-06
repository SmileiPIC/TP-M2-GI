############################# Input namelist for Laser Wakefield Acceleration 
############################# with external injection of a relativistic electron bunch

import math 
import numpy as np
import scipy.constants

##### Physical constants
lambda0             = 0.8e-6                    # laser wavelength, m
c                   = scipy.constants.c         # lightspeed, m/s
omega0              = 2*math.pi*c/lambda0       # laser angular frequency, rad/s
eps0                = scipy.constants.epsilon_0 # Vacuum permittivity, F/m
e                   = scipy.constants.e         # Elementary charge, C
me                  = scipy.constants.m_e       # Electron mass, kg
ncrit               = eps0*omega0**2*me/e**2    # Plasma critical number density, m-3
c_over_omega0       = lambda0/2./math.pi        # converts from c/omega0 units to m
reference_frequency = omega0                    # reference frequency, s-1
E0                  = me*omega0*c/e             # reference electric field, V/m

##### Variables used for unit conversions
c_normalized        = 1.                        # speed of light in vacuum in normalized units
um                  = 1.e-6/c_over_omega0       # 1 micron in normalized units
fs                  = 1.e-15*omega0             # 1 femtosecond in normalized units
mm_mrad             = um                        # 1 millimeter-milliradians in normalized units
pC                  = 1.e-12/e                  # 1 picoCoulomb in normalized units

#########################  Simulation parameters

##### mesh resolution
dx                  = 0.10*um                   # longitudinal mesh resolution
dr                  = 0.165*um                  # transverse mesh resolution
dt                  = 0.8*dx/c_normalized       # integration timestep

##### simulation window size
nx                  = 576                       # number of mesh points in the longitudinal direction
nr                  = 256                       # number of mesh points in the transverse direction
Lx                  = nx * dx                   # longitudinal size of the simulation window
Lr                  = nr * dr                   # transverse size of the simulation window

##### Total simulation time
T_sim               = 5000.*dt

##### patches parameters (parallelization)
npatch_x            = 64
npatch_r            = 8


######################### Main simulation definition block

Main(
    geometry = "AMcylindrical",

    interpolation_order = 2,

    timestep = dt,
    simulation_time = T_sim,

    cell_length  = [dx, dr],
    grid_length = [ Lx,  Lr],

    number_of_AM = 1,

    number_of_patches = [npatch_x,npatch_r],

    EM_boundary_conditions = [
        ["silver-muller","silver-muller"],
        ["buneman","buneman"],
    ],

    solve_poisson = False,
    solve_relativistic_poisson = True,
    print_every = 100,

    random_seed = smilei_mpi_rank
)

######################### Define the laser pulse

##### laser parameters
#laser_fwhm        = 25.5*math.sqrt(2)*fs                              # laser FWHM duration in field, i.e. FWHM duration in intensity*sqrt(2)
#laser_waist       = 11.5*um                                           # laser waist, conversion from um
#center_laser      = Lx-1.7*laser_fwhm                                 # laser position at the start of the simulation
#a0                = 1.8                                               # laser peak field, normalized by E0 defined above

##### Define a Gaussian Beam with Gaussian temporal envelope
#LaserEnvelopeGaussianAM(
#  a0              = a0, 
#  omega           = (2.*math.pi/lambda0*c)/reference_frequency,       # laser frequency, normalized
#  focus           = [(center_laser+0.1*laser_fwhm),0.],               # laser focus, [x,r] position
#  waist           = laser_waist,                                      # laser waist
#  time_envelope   = tgaussian(center=center_laser, fwhm=laser_fwhm),  # time profile of the laser pulse
#  envelope_solver = 'explicit',
#  Envelope_boundary_conditions = [ ["reflective", "reflective"],
#      ["reflective", "reflective"], ],
#)


######################### Define a moving window

MovingWindow(
    time_start = 0.,     # window starts  moving at the start of the simulation
    velocity_x = c_normalized,
)

######################### Define the plasma

##### plasma parameters
#n0 = 0.0008              # plasma plateau density in units of critical density defined above
#Radius_plasma = 22.*um   # Radius of plasma
#Lramp         = 6.5*um   # Plasma density upramp length
#Lplateau      = 100.*Lx
#Ldownramp     = 0.1*Lx
#begin_upramp  = Lx
#begin_plateau = begin_upramp+Lramp
#end_plateau   = begin_plateau+Lplateau
#end_downramp  = end_plateau+Ldownramp

##### plasma density profile
#longitudinal_profile = polygonal(xpoints=[begin_upramp,begin_plateau,end_plateau,end_downramp],xvalues=[0.,n0,n0,0.])
#def plasma_density(x,r):
#	profile_r = 0.
#	if ((r)**2<Radius_plasma**2):
#		profile_r = 1.
#	return profile_r*longitudinal_profile(x,r)

####### define the plasma electrons
#Species(
#  name = "plasmaelectrons",
#  position_initialization = "regular",
#  momentum_initialization = "cold",
#  particles_per_cell = 4,
#  regular_number = [2,2,1],
#  c_part_max = 1.0,
#  mass = 1.0,
#  charge = -1.0,
#  number_density = plasma_density,
#  mean_velocity = [0.0, 0.0, 0.0],
#  temperature = [0.,0.,0.],
#  pusher = "ponderomotive_boris",
#  time_frozen = 0.0,
#  boundary_conditions = [
#     ["remove", "remove"],
#     ["remove", "remove"],
#  ],
#)


######################### Define the electron bunch

##### electron bunch parameters
#Q_bunch                    = -20*pC                          # Total charge of the electron bunch
#sigma_x                    = 1.9*um                          # initial longitudinal rms size
#sigma_r                    = 2*um                            # initial transverse/radial rms size (cylindrical symmetry)
#bunch_energy_spread        = 0.01                            # initial rms energy spread / average energy (not in percent)
#bunch_normalized_emittance = 3.*mm_mrad                      # initial rms emittance, same emittance for both transverse planes
#delay_behind_laser         = 18.5*um                         # distance between center_laser and center_bunch
#center_bunch               = center_laser-delay_behind_laser # initial position of the electron bunch in the window   
#gamma_bunch                = 200.                            # initial relativistic Lorentz factor of the bunch

#npart                      = 50000                           # number of computational macro-particles to model the electron bunch 
#normalized_species_charge  = -1                              # For electrons
#Q_part                     = Q_bunch/npart                   # charge for every macroparticle in the electron bunch
#weight                     = Q_part/((c/omega0)**3*ncrit*normalized_species_charge)

##### initialize the bunch using numpy arrays
##### the bunch will have npart particles, so an array of npart elements is used to define the x coordinate of each particle and so on ...
#array_position = np.zeros((4,npart))                         # positions x,y,z, weight
#array_momentum = np.zeros((3,npart))                         # momenta x,y,z

##### The electron bunch is supposed at waist. To make it convergent/divergent, transport matrices can be used
#array_position[0,:] = np.random.normal(loc=center_bunch, scale=sigma_x, size=npart)                        # generate random number from gaussian distribution for x position
#array_position[1,:] = np.random.normal(loc=0., scale=sigma_r, size=npart)                                  # generate random number from gaussian distribution for y position
#array_position[2,:] = np.random.normal(loc=0., scale=sigma_r, size=npart)                                  # generate random number from gaussian distribution for z position
#array_momentum[0,:] = np.random.normal(loc=gamma_bunch, scale=bunch_energy_spread*gamma_bunch, size=npart) # generate random number from gaussian distribution for px position
#array_momentum[1,:] = np.random.normal(loc=0., scale=bunch_normalized_emittance/sigma_r, size=npart)       # generate random number from gaussian distribution for py position
#array_momentum[2,:] = np.random.normal(loc=0., scale=bunch_normalized_emittance/sigma_r, size=npart)       # generate random number from gaussian distribution for pz position

#array_position[3,:] = np.multiply(np.ones(npart),weight)

##### define the electron bunch
#Species( 
#  name = "electronbunch",
#  position_initialization = array_position,
#  momentum_initialization = array_momentum,
#  c_part_max = 1.0,
#  mass = 1.0,
#  charge = -1.0,
#  relativistic_field_initialization = True,
#  pusher = "ponderomotive_boris", 
#  boundary_conditions = [
#  	["remove", "remove"],
#  	["remove", "remove"], 
#  ],
#)
 
######################### Diagnostics

##### 1D Probe diagnostic on the x axis
DiagProbe(
        every = 100,
        origin = [0., 1.*dr, 1.*dr],
        corners = [
            [Main.grid_length[0], 2.*dr, 2.*dr]
        ],
        number = [nx],
        fields = ['Ex','Ey','Rho','Jx','Env_A_abs','Env_Chi','Env_E_abs']
)

##### 2D Probe diagnostics on the xy plane
DiagProbe(
    every = 100,
    origin   = [0., -nr*dr,0.],
    corners  = [ [nx*dx,-nr*dr,0.], [0,nr*dr,0.] ],
    number   = [nx, int(2*nr)],
    fields = ['Ex','Ey','Rho','Jx','Env_A_abs','Env_Chi','Env_E_abs']
)

##### Diagnostic for the electron bunch macro-particles
#DiagTrackParticles(
#  species = "electronbunch",
#  every = 100,
#  attributes = ["x", "y", "z", "px", "py", "pz", "w"]
#)


######################### Load balancing (for parallelization)                                                                                                                                                     
LoadBalancing(
    initial_balance = False,
        every = 40,
    cell_load = 1.,
    frozen_particle_load = 0.1
)

##### Field diagnostics, used for 3D export
#DiagFields(
#    every = 1000,
#    fields = ["Env_A_abs","Env_E_abs"],
#)

#DiagFields(
#    every = 1000,
#    fields = ["Rho","Rho_plasmaelectrons"],
#)

#DiagFields(
#    every = 1000,
#    fields = ["Rho_electronbunch"],
#)

