Introduction 
-------------------


In this practical work, you will familiarize with a Particle in Cell (PIC) code ([BirdsallLangdon]_, [Lapenta]_), 
learn how to set up and run a basic PIC simulation to study laser wakefield acceleration of electrons, and how to analyze the results.
The PIC code used for this tutorial, `Smilei <https://smileipic.github.io/Smilei/index.html>`_ ([Derouillat2018]_), is not a simplified version 
but a full PIC code that you can use for your future studies.




Summary of this practical
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the case study of this practical work, an intense laser pulse is injected into the plasma, 
exciting a relativistic plasma wave used to accelerate an externally injected relativistic electron bunch. 
This plasma acceleration scheme is known as laser wakefield acceleration, or LWFA ([Esarey2009]_, [Malka2012]_). 

The practical will consist in four parts:

- :ref:`Exploring the Input Namelist  <exploringthenamelist>` (**Exercises 1-2**): we will explore the Python ``InputNamelist.py`` file to understand the basic set-up of the problem (simulation window size, resolution, ...). In this part the simulation window is empty.
- :ref:`Laser pulse in vacuum  <laserpulseinvacuum>` (**Exercises 4-6**): we will add a laser laser pulse propagating in vacuum and check that its diffraction follows the one predicted for a Gaussian beam.
- :ref:`Laser wakefield excitation <plasmawave>` (**Exercises 7-11**): we will add a pre-ionized plasma and visualize how the laser pulse excites plasma waves in its wake, also checking the results against the analytical theory in the linear regime.
- :ref:`Laser wakefield acceleration of an electron bunch <laserplasmainjection>` (**Exercises 12-20**): we will add a relativistic electron bunch, injecting it into the plasma waves and studying its acceleration. 

We will arrive progressively to the full laser wakefield acceleration simulation set-up,
familiarizing with the postprocessing using the Python postprocessing library
`happi <https://smileipic.github.io/Smilei/Use/post-processing.html>`_ and adding step by step all 
the necessary blocks to the input namelist file called `InputNamelist.py <https://github.com/SmileiPIC/TP-M2-GI/blob/main/InputNamelist.py>`_ . 

To add the physical elements or required additional outputs, you just need to
decomment (i.e. remove the symbol ``#`` in front of the) lines with the relative variables and blocks,
as will be described in the exercises. 
For example, to activate a block that introduces a laser in the simulation, 
you only need to remove the symbol ``#`` in front the ``LaserEnvelopeGaussianAM`` block
and the lines defining the variables used by that block.

Prerequisites
^^^^^^^^^^^^^^^^^

Although the `InputNamelist.py <https://github.com/SmileiPIC/TP-M2-GI/blob/main/InputNamelist.py>`_ is written in Python,
no extensive knowledge of that language is required to understand its contents. 
The first exercises will use pre-made Python scripts and commands for the analysis of simulations, while the last exercises 
will ask to modify these scripts to extend their scope. These exercises include basic numpy array manipulation
and plotting of 1D and 2D arrays.
 
This practical work assumes that the reader knows how to navigate in a directory tree, create folders, 
and copy files from the command line (for a quick recap, see Sections 4-9, 13-14, and 17 
in [ShawCommandLineCrashCourse]_).

Some clarifications
^^^^^^^^^^^^^^^^^^^^^^^^
**Warning** Although external injection of an electron bunch in a plasma wave
is not the most common nor easy laser plasma acceleration scheme to realize experimentally, 
it was chosen due its conceptual simplicity, which allows to easily study some basic concepts underlying 
laser wakefield acceleration. The interested reader can find 
`here <https://smileipic.github.io/tutorials/advanced_wakefield_envelope.html>`_ a tutorial which 
includes laser wakefield acceleration with ionization injection, a more common laser wakefield acceleration scheme.

**Warning:** Many parameters of the simulation were chosen as a compromise between having a quick simulation
and being able to describe the physical phenomena of laser plasma acceleration of electron.
More physically accurate simulations of this phenomenon would require larger mesh sizes, a different resolution,
etc., that would require longer simulations less suited for a basic tutorial. 

A quick word on Smilei
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As previously stated, the numerical tool you will use for this 
practical is the PIC code Smilei [Derouillat2018]_. A prior knowledge of Smilei 
is not mandatory for the purposes of the practical exercises. Yet, 
feel free to check `Smilei’s website on GitHub <https://smileipic.github.io/Smilei/>`_ . 
The interested reader can also find additional 
`tutorials <https://smileipic.github.io/tutorials/>`_ focusing on physical 
processes not covered by this practical.

Smilei is an open-source and collaborative 
code freely distributed under a CeCILL-B license 
(equivalent to the GPL license for free-softwares). 
It can be run in 1D,2D,3D and cylindrical geometry with azimuthal modes decomposition,
with a diverse suite of physical models and numerical techniques,
from a laptop to supercomputers.



----

References
^^^^^^^^^^

.. [BirdsallLangdon] `C. K. Birdsall and A. B. Langdon, Plasma Physics via Computer Simulation, Taylor and Francis Group, 2004`
.. [Lapenta] `G. Lapenta, Kinetic plasma simulation: Particle in cell method <https://juser.fz-juelich.de/record/283633/files/Lapenta_KT-2.pdf>`_
.. [Derouillat2018] `J. Derouillat et al., Smilei : A collaborative, open-source, multi-purpose particle-in-cell code for plasma simulation, Computer Physics Communications, 222:351 – 373, 2018 <https://doi.org/10.1016/j.cpc.2017.09.024>`_
.. [Esarey2009] `E. Esarey et al., Physics of laser-driven plasma-based electron accelerators, Rev. Mod. Phys., 81:1229–1285, 2009 <http://dx.doi.org/10.1103/RevModPhys.81.1229>`_
.. [Malka2012] `V. Malka, Laser plasma accelerators, Physics of Plasmas, 19(5):055501, 2012 <https://doi.org/10.1063/1.3695389>`_
.. [ShawCommandLineCrashCourse] `Z. A. Shaw, Command line crash course <https://www.computervillage.org/articles/CommandLine.pdf>`_



