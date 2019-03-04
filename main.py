# USING PYTHON/3.4.3
# SOURCE: https://people.sc.fsu.edu/~jburkardt/py_src/md/md.py
# SOURCE: Frenkel, Smit, Understanding Molecular Simulation: 
#                                           From Algorithms to Applications

# --------------------------
# COLLECTS ENERGIES AND WRITES
# --------------------------
def md (path_to_file, s_no, dt, temp, restart, mtd):
    import numpy as np
    import math
    import os
    import subprocess
    from   initialise   import initiate, finish, restarting
    from   forces       import compute          # FORCES COMPUTES WITH SUBPROCESS
    from   positions    import update_pos
    from   velocities   import update_vel
    from   temp         import find_active_temp

    d_no = 3                            # FOR X, Y AND Z, ROWS IN MATRIX
    
    # DETERMINE WHEN TO PRINT STEP
    step_print = 1

    ### RESTARTING CALC
    if restart == 'True':
        name, original_f, step, coords, force, vel, FMO = restarting (path_to_file, d_no, temp, s_no, dt)
        
        p_no = len(coords)
    
        # CALCULATE FORCE FOR TIME = t
        force, potential = compute (p_no, d_no, coords, vel, dt, step, original_f, FMO, mtd)

        ### MTD

        # WRITE INITIAL VALUES TO name.trj
        with open(name + '.trj', 'a') as f:

            f.write("RESTART - VALUES SHOULD OVERLAP FOR THIS STEP\n")

            # COORDINATES
            f.write("Step " + str(step) + '\t' + "Coordinates in ANGSTROM\n")
            for line in coords:
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'. \
                        format(float(line[0]), float(line[1]), float(line[2])))

            # FORCES
            f.write('Step ' + str(step) + '\t' + 'Force in AMU-BOHR/S^2\n')
            for line in force:
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'.format(line[0], line[1], line[2]))

            # VELOCITIES
            f.write('Step ' + str(step) + '\t' + 'Velocities in BOHR/S\n')
            for line in vel:
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'.format(line[0], line[1], line[2]))



    ### STEP ZERO
    else:        

        step = 0

        # FOLDER FOR JOBS SUBMISSIONS
        if not os.path.exists("md_sub"):
            os.mkdir("md_sub")
        
        # SET UP FILES AND IF VELOCITIES NEEDED
        name, original_f, coords, vel, FMO = initiate (path_to_file, d_no, temp, s_no, dt)
        
        p_no = len(coords)

        # CALCULATE FORCE FOR TIME = t
        force, potential = compute (p_no, d_no, coords, vel, dt, step, original_f, FMO)

        ### MTD
        

        # WRITE INITIAL VALUES TO name.trj
        with open(name + '.trj','w+') as f:
            
            # COORDINATES
            f.write("Step " + str(step) + '\t' + "Coordinates in ANGSTROM\n")
            for line in coords:
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'.\
                        format(float(line[0]), float(line[1]), float(line[2])))
            
            # FORCES
            f.write('Step ' + str(step) + '\t' + 'Force in AMU-BOHR/S^2\n')
            for line in force: 
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'.format(line[0], line[1], line[2]))
            
            # VELOCITIES
            f.write('Step ' + str(step) + '\t' + 'Velocities in BOHR/S\n')
            for line in vel:
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'.format(line[0], line[1], line[2]))

            f.write('-----------------------------------------------------------------------\n')

        # HERE SO WILL RUN - NEED TO FIX BELOW - CAN"T REMEMBER WHAT THIS IS
        e0 = 0
        subprocess.call('rm *.dat', shell=True)
        #continue
        # END OF STEP 0 ---------------------------------------------------------------------
        
        step = 1

    # FOR ALL REMAINING STEPS ---------------------------------------------------------------
    
    for step in range(step, s_no + 1):
        
        # UPDATE POSITION USING update_pos()
        coords = update_pos (p_no, d_no, coords, vel, force, dt, step)

        # WRITE TO name.trj
        with open(name + ".trj", "a") as f:
            f.write("Step " + str(step) + '\t' + "Coordinates in ANGSTROM\n")
            for line in coords:
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'.format(float(line[0]), float(line[1]), float(line[2])))

        # CALCULATE FORCE, POTENTIAL AND KINETIC ENERGIES USING compute()
        force_prev = force
        force, potential = compute (p_no, d_no, coords, vel, dt, step, original_f, FMO)

        ### MTD

        # WRITE TO name.trj
        with open(name + '.trj','a') as f:
            f.write('Step ' + str(step) + '\t' + 'Force in AMU-BOHR/S^2\n')
            for line in force:
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'.format(line[0], line[1], line[2]))

        # UPDATE VELOCITY USING update_vel()
        vel, force_prev, kinetic = update_vel (p_no, d_no, coords, vel, force, \
        force_prev, dt, step)
        
        # WRITE TO name.trj
        with open(name + ".trj", "a") as f:
            f.write('Step ' + str(step) + '\t' + 'Velocities in BOHR/S\n')
            for line in vel:
                f.write('{:26.16e} {:26.16e} {:26.16e}\n'.format(line[0], line[1], line[2]))
            f.write('-----------------------------------------------------------------------\n')
        
        # PRINT ACTIVE TEMPERATURE
        find_active_temp(d_no, p_no, vel, coords)
        
        # INITIAL ENERGY e0 CALCULATED FOR ERROR CALC
        if (step == 1):
            e0 = potential + kinetic

        # IF TRUE WILL PRINT STEP
        if step % step_print == 0:
            # CALCULATE RELATIVE ERROR WRT E0 AND PRINT STEP
            rel = (potential + kinetic - e0)/e0
            with open(name + ".md", "a") as f:
                f.write('{:4}  {:26.16e}  {:26.16e}  {:26.16e} \n'.format\
                                    ( step, potential, kinetic, rel ))

    finish()
    
    return
