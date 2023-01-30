.. _UsefulTools:
Useful Tools
----------------

Instructions for using the cluster
^^^^^^^^^^^^^^^^^^^^^^^^

Before starting, it may be importannt to check the documentation for the Smilei PIC code, for that, go to `Smilei website <https://smileipic.github.io/Smilei/index.html>`_.

A.1- Login to the cluster
^^^^^^^^^^^^^^^^^^^^^^^^

- Open a shell/Terminal window to work on command line

- Login to the the Ruche cluster and then enter your password, which will not appear on your screen (see the access credentials you have received):

.. code-block:: bash

    ssh -XY username@...

Once you are connected you will be in your home space,  whose path is also referenced with the shortcut ``$HOME``.
It is highly recommended to use this space only to compile the code. As explained in the following, run your simulations in the space called ``$WORKDIR``.


A.2- Compile the code Smilei
^^^^^^^^^^^^^^^^^^^^^^^^

Before performing this step, make sure that smile is not installed on your workspace. If so, skip this step and go to step 1.3.

To compile the code `Smilei`:

- Download `Smilei`:
.. code-block:: bash

    git clone https://github.com/SmileiPIC/Smilei.git

- Enter the newly created folder `Smilei`:
.. code-block:: bash

    cd Smilei
- Clean potentially incomplete build files:
.. code-block:: bash

    make clean

- Compile the code from the code folder:
.. code-block:: bash

    make -j 10 machine=ruche

This should create the files called ``smilei`` and ``smilei_test``. If you see the line 
``Linking smilei_test for test mode`` and no errors are displayed,
it means everything worked well. It is normal to see messages like ``In file included from ...``

- Compile the postprocessing library `happi`:
.. code-block:: bash

    make happi

- To know the location of your executable file, just use:
.. code-block:: bash

    pwd

This command will display the path to your current working
directory, for example ``path/to/executable``. This path will
be used later. Now your executables ``smilei`` and
``smilei_test`` should be found in your folder ``path/to/executable``.

.. _sec13:
A.3- Prepare your simulation
^^^^^^^^^^^^^^^^^^^^^^^^

- Enter your working space:
.. code-block:: bash

    cd $WORKDIR

- Create a new simulation folder, for example called ``sim``, where you will run your simulation:

.. code-block:: bash

    mkdir sim
    cd sim

Each time you do it, choose a convenient name of the folder to
remember which simulation it contains. In order to avoid overwriting data, it is recommended to create 
a new simulation folder for each simulation.

- Inside the simulation folder, create a link to the executables:
.. code-block:: bash

    ln -s path/to/executable/smilei
    ln -s path/to/executable/smilei_test

The expression ``path/to/executable`` is just an example. You need to insert the actual path where your files ``smilei``
and ``smilei_test`` are. In the case of the cluster Ruche, the files ``smilei``
and ``smilei_test`` code should be in ``$HOME/Smilei``, so the command is:

.. code-block:: bash

    ln -s $HOME/Smilei/smilei
    ln -s $HOME/Smilei/smilei_test

- Inside the simulation folder, you will need a file to submit a simulation job to the job scheduler, e.g. ``submission_script.sh``. 
You can transfer the file you already have through  the comand ``scp`` or just copy and paste it in a new file inside your simulation folder. 
A copy of the ``submission_script.sh`` should be in the folder ``cd $WORKDIR/TP-M2-GI`` of Ruche, so if you are already inside your simulation folder, you can copy the 
``submission_script.sh`` with this command:

.. code-block:: bash
   
    cp $WORKDIR/TP-M2-GI/submission_script.sh

- Inside the simulation folder, you will need also the input file of your simulation ``InputNamelist.py``. A copy of the ``InputNamelist.py`` should be in ``cd $WORKDIR/TP-M2-GI`` of Ruche, so if you are already inside your simulation folder, you can copy the ``InputNamelist.py`` with this command: ``cp $WORKDIR/TP-M2-GI/InputNamelist.py``. Once you have all these files in your simulation folder (executables, submission script, input namelist) you are ready to run your simulation. If you change the name of your namelist, remember that it must be a ``.py`` file and it must appear a the end of the ``submission_script.sh``.

A.4- Run your simulation
^^^^^^^^^^^^^^^^^^^^^^^^

IMPORTANT WARNING: do NOT launch a simulation directly in your workspace. Indead, use the simulation job submission script as described below. You are now
connected in the login nodes of the cluster, made to transfer files and compile codes, and shared among the connected users. If you 
launch a simulation directly it will be run on this shared space  where all the machine users can connect, slowing down or blocking  their operations. Imagine to have a very slow home wifi connection,
sufficient only to send some e-mails to work, shared among you and many house-mates. In this analogy running a simulation directly on  the login node is equivalent to start a long video-call, blocking
everyone elses’ attempt to send e-mails and work properly. Instead, launching a simulation with a job submission script as described in the following will make the simulation run on the compute nodes, 
where the necessary resources are safely distributed among the machine users. Science is also learning to work together and to respect each other’s space.

- Check if you have all the required files (executables, submission script, input namelist) through the command:

.. code-block:: bash
   
    ls

- To check that your namelist does not contain syntax errors, use the ``smilei_test`` executable on the namelist (you will need to load the same libraries used for the code compilation): ``./smilei_test InputNamelist.py``. If you see the line ``END TEST MODE``, the namelist does not contain syntax errors and can be run.

- Launch your simulation job:

.. code-block:: bash
   
    sbatch submission_script.sh

- To check the status (running/queueing etc) of yout job:

.. code-block:: bash
   
    squeue -u $USER

This should also return the number ``JobId`` of your job, necessary for the next command.

- To delete your job from the queue:

.. code-block:: bash
   
    scancel JobId

- To read the end of the log file and let it refresh (if you want to watch your simulation execute for example):

.. code-block:: bash
   
    tail -f smilei.log
   
The the comand ``ctrl+C`` will allow you to stop watching the file `smilei.log`.

- If you want to change the time you want for your simulation, change the corresponding line in the file ``submission_script.sh`` (here 20 minutes) ``#SBATCH –time=00:20:00``. The longest simulation of the session runs approximately for 3 minutes with 10 MPI processes and 2 OpenMP threads. These parameters are already set in the submission script.

- If you want to change the number of OpenMP threads in your simulation, change the corresponding line in the file ``submission_script.sh``(here 2 threads) as written in this line ``export OMP_NUM_THREADS=2``

- If you want to change the number of MPI process in your simulation, change the corresponding line  ``#SBATCH –ntasks=10`` in the file ``submission_script.sh`` (here 10 processes).

A.5- Postprocess your simulation results
^^^^^^^^^^^^^^^^^^^^^^^^

- Open ``IPython`` (before, you will need to load the Python modules and define variables like how you did to compile the code, and be sure you have compiled ``happi``):

.. code-block:: bash
   
    ipython

- Import the libraries you need:

.. code-block:: bash
   
    import happi
    import numpy as np
    import matplotlib.pyplot as plt 

The output files have the extension ``.h5`` and can be opened  with the postprocessing library ``happi``. You will need also the 
file ``smilei.py``, generated at the start of your simulation.

- Open your simulation:

.. code-block:: bash
   
    S = happi.Open("path/to/my/results")

again, ``"path/to/my/results"`` is an example, you need to put the path of your simulation. 
If you use simply ``S = happi.Open()``, the library ``happi`` open the results inside the current working directory.

-  Now you can use the commands in the section postprocessing.

A.6- Command line cheatsheet
^^^^^^^^^^^^^^^^^^^^^^^^

- ``pwd``: shows the path of the current working directory.

- ``cd path``: go to ``path``

- ``ls``: shows the content of the current directory.

- ``ls path``: shows the content in ``path``.

- ``rm file``: removes ``file``. To remove a folder, you will need an additional flag: ``rm -r folder`` (be careful).

- ``cp source_file destination_path``: copies ``source_file`` to the ``destination_path``.

- ``scp source_file destination_path`` : same as ``cp``, but you can also transfer folders and files to a different machine, e.g. from the cluster to your computer and vice versa. You have to provide your username, the server address and your password, e.g. ``scp source_file username@server:/destination_path/``. This command can be used to transfer output files from the cluster to your computer for later postprocessing if so you prefer (of course larger data files will need more time to transfer).

- ``mv source destination``: move ``source`` (can be a file or directory) to a ``destination``. If the ``destination`` does not specify a path, the command renames ``source`` with the name
``destination``.

- ``ipython``: opens ``Ipython``, where also the previous commands can be used. To run a Python script inside this interface, use ``%run script_name.py``.

.. _Postprocessing:
Postprocessing
^^^^^^^^^^^^^^^^^^^^^^^^

A fundamental part of working with simulation codes is the 
postprocessing of the results. Smilei includes an entire ``Python`` library 
for postprocessing. 
However, to plot your first results and make quantitative evaluations 
you do not need to be an expert of ``Python``.

For your convenience and quick reference, here we include only the commands 
you will need for this practical. Do not hesitate to copy and paste 
the following commands in ``IPython`` and adapt them to the problem you are solving.

Remember that the results are in normalized units. 
The library ``happi`` also allows to convert to SI units, but this will not be taught in this practical 
(details in the `documentation <https://smileipic.github.io/Smilei/Use/post-processing.html>`_).


B.1- Compilation of happi
^^^^^^^^^^^^^^^^^^^^^^^^

It is sufficient to use the command ``make happi`` in the code folder 
(after you have loaded the Python modules, see the file ``ClusterEnvironment.pdf``). 
Then, to analyze the results of your simulation, open the ``IPython`` interface 
(just use the command ``ipython`` in the command line terminal).

B.2- Open a simulation
^^^^^^^^^^^^^^^^^^^^^^^^
To import the library ``happi`` in ``IPython`` and open a simulation in the folder, use::

   import happi; S = happi.Open("path/to/simulation")

In this specific example the folder’s path is called for example ``"path/to/simulation"`` 
(use the path of your simulation instead!). 

The last command will create an object called ``S``, our simulation, 
which contains all the necessary data, taken from the input namelist and from the 
output files. 

You can easily access parameters from the input namelist, for example::

   S.namelist.dx
   S.namelist.Main.geometry

In general, if you tap ``S.`` or add the name of the blocks and then use the tab key, 
you will see the available blocks and variables.

B.3- Plot diagnostics
^^^^^^^^^^^^^^^^^^^
To open a specific diagnostic, like the ``Probe1`` defined in the namelist, 
and plot the longitudinal electric field ``Ex`` contained in that diagnostic, use::

   S.Probe.Probe1("Ex").plot()

Other physical fields defined on the grid that you can plot are for example ``Ey``
(the electric field component in the `y` direction), 
``Rho`` (the charge density). Remember that you can also specify operations 
on the fields, like ``2.*Ey-Ex``, when you declare your variable.

By default, the last command will only plot the requested field obtained 
in the last simulation output available for that diagnostic. 
You may instead be interested in a specific iteration of the simulation (in code units), 
like iteration 1200. To plot only that timestep, just specify it inside the diagnostic block::

   S.Probe.Probe1("Ex", timesteps=1200).plot()

Remember that this timestep corresponds to physical time ``1200*dt``, where ``dt`` 
is the simulation timestep, which can be found with ``dt=S.namelist.Main.timestep``.

To know which iterations are available in your diagnostic, you can use::

   S.Probe.Probe1("Ex").getAvailableTimesteps()

B.4- Visualize multiple timesteps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Normally you have a sequence of outputs, so you may want to see an animation 
of the outputs or to be able to slide between the saved timesteps. 
It is possible to do it with these commands respectively::

    S.Probe.Probe1("Ex").animate()
    S.Probe.Probe1("Ex").slide()

In the last case, just slide with the horizontal bar to see the evolution of the plotted quantity at
different iterations.

B.5- Modify elements of the plot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Like in Python, you may be interested into specifying the figure number, 
or change the colormap, or specifying a maximum or minimum value plotted. 
You can include the same corresponding keywords inside the plot/animate/slide command. 
As an example where all these elements are specified::

   S.Probe.Probe1("Ex").plot(figure=2, vmin = -0.1, vmax = 0.1 , cmap = "seismic")

B.6- Plot multiple lines
^^^^^^^^^^^^^^^^^^^^^^^^^
You may be interested in visualizing multiple curves in the same plot window. 
Then the command ``happi.multiPlot`` is what you need.

For example, if you want to plot two quantities from the same simulation, 
scaling them through multiplying factors::

   import happi
   S = happi.Open("path/to/simulation")
   E = S.Probe.Probe1("0.1*Ex", timesteps=1000, label = "E")
   rho = S.Probe.Probe1("-10.*Rho", timesteps=1000, label="charge density")
   happi.multiPlot(E, rho, figure = 1)

The previous example draws two curves, but you can use multiPlot to plot more curves.

Note that you can plot also different timesteps from the same simulation with the same procedure. 
Similarly, you can plot two quantities from two or more simulations::

   import happi
   S1 = happi.Open("path/to/simulation1")
   Ex1 = S1.Probe.Probe0("Ex",timesteps=1000)
   S2 = happi.Open("path/to/simulation2")
   Ex2 = S2.Probe.Probe0("Ex",timesteps=1000)
   happi.multiPlot(Ex1,Ex2)

B.7- Export the data
^^^^^^^^^^^^^^^^^^^^
Those shown above are all the ``happi`` commands you may need for this practical. 
If you prefer instead to analyze your results with ``numpy`` arrays in Python, 
you can easily export your diagnostic to a ``numpy`` array, for example::

   import happi
   import numpy as np
   S = happi.Open("path/to/simulation")
   myArrayVariable = S.Probe.Probe1("Ex").getData()
   myArrayVariable = S.Probe.Probe1("Ex", timesteps=1200).getData()
   myArrayVariable = np.asarray(myArrayVariable)

In case you want to export the data to a text file ``.txt`` and read it with 
another language, you can write this array on a text file using::

   np.savetxt("file_name.txt", myArrayVariable)
