# ab initio molecular dynamics with metadynamics

- Python module
- Spawns GAMESS gradient calculations and pulls the forces
- Uses verlocity verlet MD
- Requires numpy


### Input:

- expects gamess gradient input file
- task file (eg):

    path_to_file = water.inp # gamess gradient input file 
    step_no      = 60000     # number of steps
    dt           = 1e-15     # time step
    temp         = 300       # temperature
    restart      = True      # Boolean for restart calculation
    mtd          = True      # Boolean for metadynamics simulation
    

### Files

- aimd executes md() using task file provided to programme and looks for keywords 'path_to_file', 'step_no', 'dt', 'temp' to define md parameters
- convert holds values to convert between units
- forces handles collecting forces from gamess output
- main holds the md() function and calls the others in a loop
- masses holds the molar masses in a dictionary
- positions excecutes r(t+dt) = r(t) + v(t)*dt + 1/2 * force(t)/mass * dt\**2
- read_gms reads 'path_to_file' which is a gradient input file for gamess
- temp holds a function which determines the current md temperature
- times is a function that returns the time
- velocities excecutes v(t+dt) = v(t) + (force(t) + force(t+dt)) * dt/2mass 


### Restart:

- in dir with .trj file of previous calculation
- in dir with FMO .inp file with same system info


### Metadynamics:

- call function after gradient calculation
- determines the form of the CVs


### Output:

- gamess gradient calculation ouput goes into /md_sub/ 
- each step gets a folder within md_sub
- subfolders contain xyz, input, output files
- file.md prints step , potential, kinetic and error information
- file.trj prints the coordinates, force and velocity for each step


### Excecution:

- job file (eg.):

    #!/bin/bash
    #PBS -P k96
    #PBS -l walltime=40:00:00
    #PBS -l ncpus=16
    #PBS -l mem=63GB
    #PBS -l jobfs=100GB
    #PBS -l wd

    module unload openmpi/1.6.3
    module load openmpi/1.8.2
    module load python3
    python3 /short/k96/zls565/md/src/aimd.py


### Units:

- Position    Bohr                           (Bohr)
- Time        Second                         (s)
- Mass        AMU                            (AMU)
- Velocity    Bohr per Second                (Bohr/s)
- Force       AMU by Bohr per Second squared (AMU*Bohr/s^2)


