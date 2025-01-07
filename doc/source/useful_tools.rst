.. _UsefulTools:
Appendix: Cheatsheet
----------------------------


A: Command Line Terminal Cheatsheet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- When you feel lost, use the command ``pwd`` (mnemonic ``pwd``: present working directory) to display your present path. For example, a path may have the form ``/gpfs/users/user_01``. This specific example means that you are in the folder ``user_01``, which is inside the folder ``users``, which is inside the folder ``gpfs``.

- To go back to your home (the path where you connect with the ``ssh`` command), use ``cd ~`` (useful if you feel lost in your directory tree).

- To check the content of your present path, use the command ``ls`` (mnemonic ``ls``: list) 
  
- Similarly, you can check the content of another directory, e.g. with a path called ``folder/subfolder``, using the command ``ls folder/subfolder/``

- To move to a specific path, e.g. ``path/to/your/folder`` use ``cd path/to/your/folder`` (mnemonic ``cd``: change directory)
  
- To move up by one level from your present path, use the shortcut ``cd ..``

- To change the name of a file or directory, use ``mv old_name new_name`` (mnemonic ``mv``: move) 

- To move a file/folder into a folder ``move source destination_folder/``. The `source` can be a file or a folder.

- **Risky command** To remove a file, use ``rm filename`` (mnemonic ``rm``: remove). To remove an entire folder and its content, use ``rm -rf foldername`` or ``rmdir foldername``.

- **Warning** This operation is irreversible! 

----------

.. _sec13:
B: How to prepare a simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each time an exercise asks to run a new simulation, it is recommended to
create a new directory, where you will insert the required files and run this new simulation.
This will ensure that no previous data is lost or overwritten.

Following are the instructions to complete this process.

- Create a new simulation folder, for example called ``sim``, where you will run your simulation:

.. code-block:: bash

    mkdir simulation_folder_name
    cd simulation_folder_name

Each time you do it, choose a convenient name of the folder to
remember which simulation it contains. In order to avoid overwriting data, it is recommended to create 
a new simulation folder for each simulation.

- Go inside the simulation folder, e.g. with the command ``cd simulation_folder_name``.

- Inside the simulation folder, you will need a file to submit a simulation job to the job scheduler, e.g. ``JJ_submission_script.sh``. 
You can transfer the file you already have in your home through  the comand ``cp``:

.. code-block:: bash

  cp ~/TP-M2-GI/JJ_submission_script.sh simulation_folder_name/ 
  
The last command will copy the file ``~/TP-M2-GI/JJ_submission_script.sh`` inside the folder called ``simulation_folder_name`` in your present working directory.

- Inside the simulation folder, you will need also the input file of your simulation ``InputNamelist.py``. A copy of the ``InputNamelist.py`` should be in ``~/TP-M2-GI``, 
have a copy in another folder you can use the ``cp`` command (add the source and destination paths.)

----------

C: How to Run your simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Check if you have all the required files (submission script, input namelist) through the command ``ls``

- Remember to uncomment the necessary variables and blocks as explained in the exercise before launching a simulation.

- Launch your simulation job:

.. code-block:: bash
   
    jjsub JJ_submission_script.sh

- To check the status (running/queueing etc) of your job:

.. code-block:: bash
   
    jjstat -u $USER

This should also return the number ``JobId`` of your job, necessary for the next command.

- To stop/delete your job from the queue (this operation is irreversible!):

.. code-block:: bash
   
    jjdel JobId

- To read the end of the log file and let it refresh (if you want to watch your simulation execute for example):

.. code-block:: bash
   
    tail -f smilei.log
   
The the comand ``ctrl+C`` will allow you to stop watching the file `smilei.log`.

----------

D: How to postprocess your simulation results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Here, ``"path/to/my/results"`` is just an example of path, you need to put the path of your simulation. 
If you use simply ``S = happi.Open()``, the library ``happi`` open the results inside the current working directory.

For your convenience and quick reference, some of the most commonly used commands of ``happi`` are reported. 
Do not hesitate to copy and paste the following commands in ``IPython`` and adapt them to the problem you are solving.

Remember that the results are in normalized units, but you can specify also SI units for the plot. 



D.02: Open a simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To import the library ``happi`` in ``IPython`` and open a simulation in the folder, use::

   import happi; S = happi.Open("path/to/simulation")

In this specific example the folder’s path is called for example ``"path/to/simulation"`` 
(use the path of your simulation instead!).

Using instead::

   import happi; S = happi.Open()
   
will open the simulation in your current path. If you are not in a simulation folder, 
an error message will be displayed. 

The last command will create an object called ``S``, our simulation, 
which contains all the necessary data, taken from the input namelist and from the 
output files. 

You can easily access parameters from the input namelist, for example::

   S.namelist.dx
   S.namelist.Main.geometry

In general, if you tap ``S.`` or add the name of the blocks and then use the tab key, 
you will see the available blocks and variables.

D.03: Plot diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
   
   
D.04: Specifying the physical units 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The code, including its outputs, uses normalized units.
You can specify the units you want to use, e.g.::

    S.Probe.Probe1("Ex",units=["um","GV/m"]).plot()
        

D.05: Visualize multiple timesteps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Normally you have a sequence of outputs, so you may want to see an animation 
of the outputs or to be able to slide between the saved timesteps. 
It is possible to do it with these commands respectively::

    S.Probe.Probe1("Ex").animate()
    S.Probe.Probe1("Ex").slide()

In the last case, just slide with the horizontal bar to see the evolution of the plotted quantity at
different iterations.

D.06: Modify elements of the plot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Like in Python, you may be interested into specifying the figure number, 
or change the colormap, or specifying a maximum or minimum value plotted. 
You can include the same corresponding keywords inside the plot/animate/slide command. 
As an example where all these elements are specified::

   S.Probe.Probe1("Ex").plot(figure=2, vmin = -0.1, vmax = 0.1 , cmap = "seismic")

D.07: Plot multiple lines in the same window
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

D.08: Export the data
^^^^^^^^^^^^^^^^^^^^^^^^^
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
