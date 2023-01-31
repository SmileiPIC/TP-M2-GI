Introduction
--------------------


In this practical work, you will familiarize yourself with a Particle in Cell (PIC) code ([BirdsallLangdon]_, [Lapenta]_), 
learn how to set up and run a PIC simulation to study plasma acceleration, and then analyze the results.
The PIC code you will use, Smilei ([Derouillat2018]_), is not a simplified version 
but a full PIC code that you can use for your future studies. You can find more information 
on `this website <https://smileipic.github.io/Smilei/index.html>`_, 
and on the `tutorials <https://smileipic.github.io/tutorials/>`_.


At the end of this practical work, you will be able to run and analyze a full PIC simulation 
of a plasma acceleration set-up, where an intense laser pulse is injected into the plasma, 
exciting a relativistic plasma wave. The excited plasma wave can accelerate an injected electron beam placed just behind the laser pulse. 
This plasma acceleration scheme is known as laser wakefield acceleration (LWFA)
([TajimaDawson]_, [Malka2002]_, [Esarey2009]_, [Malka2012]_) and is commonly compared 
to a surfer (the injected electrons) being accelerated by waves in the sea (the plasma waves). 
As antecipated, in the particular LWFA set-up of this practical work, the relativistic electron beam 
is externally injected into the plasma wave. Although this is not the simplest LWFA experimental set-up, 
it was chosen due its conceptual simplicity.
Additional information on more widely used LWFA set-ups can be found in References [Esarey2009]_ and [Malka2012]_.


You will not immediately simulate this described full case.
Instead you will arrive progressively at the full simulation arrangement,
familiarizing yourself with the code and adding step by step all 
the necessary blocks to the input namelist file, called 
`InputNamelist.py <https://github.com/SmileiPIC/TP-M2-GI/blob/main/InputNamelist.py>`_ . 
In referenced file, the lines that start with the symbol
``#`` are comments and are ignored by the code.  
The comments in the input namelist for this practical work serve one of two purposes: 
i) to help understand a particular section of the namelist 
or ii) to deactivate a particular block or variable definition in the namelist. 
For example, to activate a block that introduces a laser in the simulation, 
you only need to remove the symbol ``#`` in front the LaserEnvelopeGaussianAM block
and do not forget to uncomment the laser parameters.


The `InputNamelist.py <https://github.com/SmileiPIC/TP-M2-GI/blob/main/InputNamelist.py>`_ is written in Python,
but you do not need extensive knowledge of that language to understand its contents. 
Knowing how to define variables (and, optionally, how to define numpy arrays) should be sufficient. 
This practical work assumes that you know how to navigate in a directory tree, create folders, 
and copy files from the command line (for a quick recap, see Sections 4, 5, 7, 8, 9, 13, 14, and 17 
of Reference [ShawCommandLineCrashCourse]_).


From the very first exercises of this practical work, you will have the full input namelist at your disposal. 
However, only the module that describes the propagation of the laser in vacuum will be uncommented. 
After understanding the code's functioning with only the laser, you will then be invited to activate the plasma.
This will allow for the electrostatic plasma wave excitation. Finally, after comprehending the temporal evolution 
of the laser and the plasma wave excitation, the injection and acceleration of an electron bunch will be considered. 
Each of these three elements is introduced into the simulation as a block of text (note that two blocks are initially commented out).


You will be assisted in analyzing your results using the postprocessing library of Smilei called `happi <https://smileipic.github.io/Smilei/Use/post-processing.html>`_ . 
Alternatively, you can use happi library to export the data to arrays and text files that 
can be processed with other programming languages. More information can be found in the post-processing tab.



A quick word on Smilei
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


As previously stated, the numerical tool you will use for this 
practical is the PIC code Smilei [Derouillat2018]_. A prior knowledge of Smilei 
is not mandatory for the purposes of the practical exercises. Yet, 
checking `Smilei’s website <https://smileipic.github.io/Smilei/>`_  for information 
on how to write a namelist can be useful. Furthermore, the interested reader can find additional 
`tutorials <https://smileipic.github.io/tutorials/>`_ also focusing on physical 
processes not covered by this practical.

Smilei is an open-source and collaborative 
code freely distributed under a CeCILL-B license 
(equivalent to the GPL license for free-softwares). 
The code, its documentation and post-processing tools are freely available 
on `Smilei's website <https://smileipic.github.io/Smilei/index.html>`_ hosted on GitHub.

----

References
^^^^^^^^^^

.. [BirdsallLangdon] `C. K. Birdsall and A. B. Langdon, Plasma Physics via Computer Simulation, Taylor and Francis Group, 2004`
.. [Lapenta] `G. Lapenta, Kinetic plasma simulation: Particle in cell method <https://juser.fz-juelich.de/record/283633/files/Lapenta_KT-2.pdf>`_
.. [Derouillat2018] `J. Derouillat et al., Smilei : A collaborative, open-source, multi-purpose particle-in-cell code for plasma simulation, Computer Physics Communications, 222:351 – 373, 2018 <https://doi.org/10.1016/j.cpc.2017.09.024>`_
.. [TajimaDawson] `T. Tajima and J. M. Dawson, Laser electron accelerator, Phys. Rev. Lett., 43:267–270, 1979 <https://doi.org/10.1103/PhysRevLett.43.267>`_
.. [Malka2002] `V. Malka et al., Electron acceleration by a wake field forced by an intense ultrashort laser pulse, Science, 298(5598):1596–1600, 2002 <https://doi.org/10.1126/science.1076782>`_
.. [Esarey2009] `E. Esarey et al., Physics of laser-driven plasma-based electron accelerators, Rev. Mod. Phys., 81:1229–1285, 2009 <http://dx.doi.org/10.1103/RevModPhys.81.1229>`_
.. [Malka2012] `V. Malka, Laser plasma accelerators, Physics of Plasmas, 19(5):055501, 2012 <https://doi.org/10.1063/1.3695389>`_
.. [ShawCommandLineCrashCourse] `Z. A. Shaw, Command line crash course <https://www.computervillage.org/articles/CommandLine.pdf>`_