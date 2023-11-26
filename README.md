# TP-M2-GI
Numerical practical (Travaux Pratiques, or TP) for the Master M2 - Grands Instruments.

The case study, simulated with the Particle in Cell (PIC) code Smilei, is a set-up of laser-plasma acceleration with external injection of a relativistic electron bunch. At first, only the propagation of an intense laser pulse in vacuum is simulated. Afterwards, the plasma is added, to study the generation of plasma waves. Finally, a relativistic electron bunch is added and injected in the plasma wave, to be accelerated.

The exercises introduce the physics of the considered set-up, teach how to compare the code results with analytical theory when possible and introduce the basic postprocessing of interest for PIC simulations of plasma acceleration. 


Following is an animation of the first laser wakefield acceleration case study of the practical.
The laser pulse (envelope of the electric field depicted in red) excites a relativistic plasma wave, whose electronic density is shown with a blue-white volume rendering.
The white particles represent the relativistic electron bunch that is injected and accelerated in the plasma wave.

![LWFA_TP_M2-GI](https://user-images.githubusercontent.com/9608804/191453308-a7670636-b676-4b1f-a1b4-dbf6b81d895a.gif)


# List of contents of the TP folders and files
- folder `Answers_Form`: the form to submit the answers to the practical exercises.
- folder `doc`: the course handouts including the exercises and useful postprocessing commands.
- folder `Postprocessing_Scripts`: some Python scripts to analyze the laser pulse propagation, the plasma wave generation and the electron bunch properties.
- file `InputNamelist.py`: the input file in Python, to run the simulations of the practical.
- file `submission_script.sh`: the slurm job submission script to run the practical's simulations on the cluster.


### Acknowledgements

For this TP, the participants have launched their simulations using HPC resources 
from the “Mésocentre” computing center of CentraleSupélec and 
École Normale Supérieure Paris-Saclay supported by CNRS and Région Île-de-France 
(http://mesocentre.centralesupelec.fr/).
We would like to thank the Mésocentre engineers for their assistance in the organization
of this TP, in particular K. Hasnaoui.

We would like to acknowledge the help of S. Kazamias and O. Guilbaud in the conception and realization of this TP.

Last but not least, we are grateful to the students who attend this TP each year,
contributing to the improvement of its material through their 
invaluable feedback.
