# TP-M2-GI
Numerical practical for the Master M2 - Grands Instruments.

The case study, simulated with the Particle in Cell (PIC) code Smilei, is a set-up of laser-plasma acceleration with external injection of a relativistic electron bunch. At first, only the propagation of an intense laser pulse in vacuum is simulated. Afterwards, the plasma is added, to study the generation of plasma waves. Finally, a relativistic electron bunch is added and injected in the plasma wave, to be accelerated.

The exercises introduce the physics of the considered set-up, teach some sanity checks to compare the code results with theory and introduce the basic postprocessing of interest for PIC simulations of plasma acceleration. 


An animation of the first laser wakefield acceleration simulation in the practical:

https://user-images.githubusercontent.com/9608804/190160422-dbfdf027-2160-4f0d-a34c-7b96af4e563c.mp4


# List of contents
- folder `Answers_Form`, which contains the form to submit the answers to the practical exercises.
- folder `Handouts`, which contains the course handouts, to be built with LaTeX. To complete the practical, solve the exercises in this file and fill the answer form.
- folder `Instructions_Cluster`, which contains the instructions to compile the code, run and postprocess simulations. The file is built with LaTeX
- folder `Postprocessing_Scripts`, which contains some Python scripts to analyze the laser pulse propagation, the plasma wave generation and the electron bunch properties.
- folder `ScriptSetEnvironment`, with a bash script to load the libraries and variable definitions to build Smilei on the cluster.
- file `InputNamelist.py`, in Python, to run the simulations of the practical.
- file `submission_script.sh`, a slurm job submission script to run the practical's simulations on the cluster.



