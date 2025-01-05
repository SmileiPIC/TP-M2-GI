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
c_normalized        = 1.                        # speed of light in vacuum  in normalized units
um                  = 1.e-6/c_over_omega0       # 1 micron                  in normalized units
mm                  = 1.e-3/c_over_omega0       # 1 mm                      in normalized units
fs                  = 1.e-15*omega0             # 1 femtosecond             in normalized units
mm_mrad             = um                        # 1 millimeter-milliradians in normalized units
pC                  = 1.e-12/e                  # 1 picoCoulomb             in normalized units

#########################  Simulation parameters

##### mesh resolution
dx                  = 0.05*um                   # longitudinal mesh resolution
dr                  = 0.3*um                    # transverse mesh resolution


dt                  = 0.97*dx/c_normalized      # integration timestep

##### Simulation window size
nx                  = 1152                      # number of mesh points in the longitudinal direction
nr                  = 104                       # number of mesh points in the transverse direction
Lx                  = nx * dx                   # longitudinal size of the simulation window
Lr                  = nr * dr                   # transverse size of the simulation window

##### Total simulated time
T_sim               = 10001*dt

##### Patches parameters (parallelization)
npatch_x            = 64
npatch_r            = 8


######################### Main simulation definition block

Main(
    geometry                           = "AMcylindrical",

    interpolation_order                = 2,

    timestep                           = dt,
    simulation_time                    = T_sim,

    cell_length                        = [ dx, dr],
    grid_length                        = [ Lx,  Lr],

    number_of_AM                       = 1,

    number_of_patches                  = [npatch_x,npatch_r],
 
    EM_boundary_conditions             = [["silver-muller"],["PML"],],
    number_of_pml_cells                = [[0,0],[20,20]],
 
    solve_poisson                      = False,
    solve_relativistic_poisson         = True,
    relativistic_poisson_max_iteration = 100000,

    print_every                        = 100,
    
    use_BTIS3_interpolation            = True,

    reference_angular_frequency_SI     = omega0,

    random_seed                        = smilei_mpi_rank
)

######################### Define the laser pulse

### laser parameters
#laser_fwhm_field    = 25.5*math.sqrt(2)*fs                                      # laser FWHM duration in field, i.e. FWHM duration in intensity*sqrt(2)
#laser_waist         = 12*um                                                     # laser waist, conversion from um
#x_center_laser      = Lx-1.7*laser_fwhm_field                                   # laser position at the start of the simulation
#x_focus_laser       = (x_center_laser+0.1*laser_fwhm_field)                     # laser focal plane position
#a0                  = 2.3                                                       # laser peak field, normalized by E0 defined above

### Define a Gaussian bunch with Gaussian temporal envelope
#LaserEnvelopeGaussianAM(
#    a0              = a0, 
#    omega           = (2.*math.pi/lambda0*c)/reference_frequency,               # laser frequency, normalized
#    focus           = [x_focus_laser,0.],                                       # laser focus, [x,r] position
#    waist           = laser_waist,                                              # laser waist
#    time_envelope   = tgaussian(center=x_center_laser, fwhm=laser_fwhm_field),  # we choose a Gaussian time envelope for the laser pulse field
#    envelope_solver              = 'explicit_reduced_dispersion',
#    Envelope_boundary_conditions = [ ["reflective"],["PML"] ],
#    Env_pml_sigma_parameters     = [[0.9 ,2     ],[80.0,2]     ,[80.0,2     ]],
#    Env_pml_kappa_parameters     = [[1.00,1.00,2],[1.00,1.00,2],[1.00,1.00,2]],
#    Env_pml_alpha_parameters     = [[0.90,0.90,1],[0.65,0.65,1],[0.65,0.65,1]]
#)


######################### Define a moving window

MovingWindow(
    time_start = 0.,                                            # the simulation window starts  moving at the start of the simulation
    velocity_x = c_normalized,                                  # speed of the moving window, normalized by c
)

########################### Define the plasma

###### Plasma plateau density
#plasma_density_1_ov_cm3    = 1.e18                              # plasma plateau density in electrons/cm^3
#n0                         = plasma_density_1_ov_cm3*1e6/ncrit  # plasma plateau density in units of critical density defined above

###### Initial plasma density distribution
#Radius_plasma              = 30.*um                             # Radius of plasma
#Lramp                      = 15.*um                             # Plasma density upramp length
#Lplateau                   = 1. *mm                             # Length of density plateau
#Ldownramp                  = 15.*um                             # Length of density downramp
#x_begin_upramp             = Lx                                 # x coordinate of the start of the density upramp
#x_begin_plateau            = x_begin_upramp+Lramp               # x coordinate of the end of the density upramp / start of density plateau
#x_end_plateau              = x_begin_plateau+Lplateau           # x coordinate of the end of the density plateau start of the density downramp
#x_end_downramp             = x_end_plateau+Ldownramp            # x coordinate of the end of the density downramp

##### Define the density longitudinal profile: a polygonal where at the x coordinates in xpoints.
##### The corresponding unperturbed plasma density is given by the values in xvalues,
##### radially uniform until r=Radius_plasma, out of which the density is zero.
#longitudinal_profile = polygonal(xpoints=[x_begin_upramp,x_begin_plateau,x_end_plateau,x_end_downramp],xvalues=[0.,n0,n0,0.])
#def plasma_density(x,r):
#	profile_r     = 0.
#	if (r<Radius_plasma):
#		profile_r = 1.
#	return profile_r*longitudinal_profile(x,r)

####### Define the plasma electrons
#Species(
#  name                     = "plasmaelectrons",
#  position_initialization  = "regular",
#  momentum_initialization  = "cold",
#  particles_per_cell       = 4,       # macro-particles per cell: this number must be equal to the product of the elements of regular_number
#  regular_number           = [1,4,1], # distribution of macro-particles per cell in each direction [x,r,theta]
#  mass                     =  1.0,    # units of electron mass
#  charge                   = -1.0,    # units of electron charge
#  number_density           = plasma_density,
#  mean_velocity            = [0.0, 0.0, 0.0],
#  temperature              = [0.,0.,0.],
#  pusher                   = "ponderomotive_borisBTIS3",
#  time_frozen              = 0.0,
#  boundary_conditions      = [ ["remove", "remove"],["remove", "remove"], ],
#)

######################## Define the electron bunch

###### electron bunch parameters
#Q_bunch                    = -60 * pC                          # Total charge of the electron bunch
#sigma_x                    = 1.5 * um                          # initial longitudinal rms size
#sigma_r                    = 2   * um                          # initial transverse/radial rms size (cylindrical symmetry)
#bunch_energy_spread        = 0.01                              # initial rms energy spread / average energy (not in percent)
#bunch_normalized_emittance = 3.  * mm_mrad                     # initial rms emittance, same emittance for both transverse planes
#delay_behind_laser         = 22. * um                          # distance between x_center_laser and center_bunch
#center_bunch               = x_center_laser-delay_behind_laser # initial position of the electron bunch in the window   
#gamma_bunch                = 200.                              # initial relativistic Lorentz factor of the bunch

#n_bunch_particles          = 50000                             # number of macro-particles to model the electron bunch 
#normalized_species_charge  = -1                                # For electrons
#Q_part                     = Q_bunch/n_bunch_particles         # charge for every macro-particle in the electron bunch
#weight                     = Q_part/((c/omega0)**3*ncrit*normalized_species_charge)

##### initialize the bunch using numpy arrays
##### the bunch will have n_bunch_particles particles, so an array of n_bunch_particles elements is used to define the x coordinate of each particle and so on ...
#array_position             = np.zeros((4,n_bunch_particles))   # positions x,y,z, and weight
#array_momentum             = np.zeros((3,n_bunch_particles))   # momenta x,y,z

##### The electron bunch is supposed at waist. To make it convergent/divergent, transport matrices can be used.
##### For the coordinates x,y,z, and momenta px,py,pz of each macro-particle, 
##### a random number is drawn from a Gaussian distribution with appropriate average and rms spread. 
#array_position[0,:]        = np.random.normal(loc=center_bunch, scale=sigma_x                           , size=n_bunch_particles)
#array_position[1,:]        = np.random.normal(loc=0.          , scale=sigma_r                           , size=n_bunch_particles)
#array_position[2,:]        = np.random.normal(loc=0.          , scale=sigma_r                           , size=n_bunch_particles)
#array_momentum[0,:]        = np.random.normal(loc=gamma_bunch , scale=bunch_energy_spread*gamma_bunch   , size=n_bunch_particles)
#array_momentum[1,:]        = np.random.normal(loc=0.          , scale=bunch_normalized_emittance/sigma_r, size=n_bunch_particles)
#array_momentum[2,:]        = np.random.normal(loc=0.          , scale=bunch_normalized_emittance/sigma_r, size=n_bunch_particles)

##### This last array element contains the statistical weight of each macro-particle, 
##### proportional to the total charge of all the electrons it contains
#array_position[3,:]        = np.multiply(np.ones(n_bunch_particles),weight)

##### define the electron bunch
#Species( 
#  name                              = "electronbunch",
#  position_initialization           = array_position,
#  momentum_initialization           = array_momentum,
#  mass                              =  1.0, # units of electron mass
#  charge                            = -1.0, # units of electron charge
#  relativistic_field_initialization = True,
#  pusher                            = "ponderomotive_borisBTIS3", 
#  boundary_conditions               = [ ["remove", "remove"],["remove", "remove"],],
#)

######################### Diagnostics

##### 1D Probe diagnostic on the x axis
DiagProbe(
    every                = 400,
    origin               = [0., 1.*dr, 1.*dr],
    corners              = [ [Main.grid_length[0], 2.*dr, 2.*dr]],
    number               = [nx],
    fields               = ['Ex','Ey','Rho','Env_A_abs','Env_E_abs','Bz','BzBTIS3']
)

##### 2D Probe diagnostics on the xy plane
DiagProbe(
    every                = 400,
    origin               = [0., -nr*dr,0.],
    corners              = [ [nx*dx,-nr*dr,0.], [0,nr*dr,0.] ],
    number               = [nx, int(2*nr)],
    fields               = ['Ex','Ey','Rho','Env_A_abs','Env_E_abs','Bz','BzBTIS3']
)

##### Diagnostic for the electron bunch macro-particles
#DiagTrackParticles(
#    species              = "electronbunch",
#    every                = 400,
#    attributes           = ["x", "y", "z", "px", "py", "pz", "w"]
#)


###### Load balancing (for parallelization when running with more than one MPI process)                                                                                                                                                     
LoadBalancing(
    initial_balance      = False,
    every                = 40,
    cell_load            = 1.,
    frozen_particle_load = 0.1
)

##### Field diagnostics, used for 3D export (see this tutorial https://smileipic.github.io/tutorials/advanced_vtk.html)

#DiagFields(
#    every                 = 100,
#    fields                = ["Env_E_abs"],
#)

#DiagFields(
#    every                 = 100,
#    fields                = ["Rho","Rho_plasmaelectrons"],
#)

#DiagFields(
#    every                 = 100,
#    fields                = ["Rho_electronbunch"],
#)

