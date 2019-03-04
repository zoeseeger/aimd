# -------------------------------------
# FUNCTION COMPUTES FORCES AND ENERGIES
# -------------------------------------
def compute (p_no, d_no, coords, vel, dt, step, original_f, FMO, mtd):
    from   convert import F2F
    from   metad   import metadynamics 
    import numpy   as     np
    import os
    import re
    import subprocess
    
    # ZERO MATRICES
    force  = np.zeros([p_no, d_no])

    # TO RUN SPEC 
    cwd = os.getcwd()
    
    # PUT ZEROS IN FRONT OF NAME TO ORDER IN FOLDER 
    if len(str(step)) == 1:
        step_name = '000' + str(step)
    elif len(str(step)) == 2:
        step_name = '00' + str(step)
    elif len(str(step)) == 3:
        step_name = '0' + str(step)
    else:
        step_name = str(step)
    
    # CREATING FOLDERS TO WRITE
    if not os.path.exists("md_sub/step_" + step_name):
        os.mkdir("md_sub/step_" + step_name)
    os.chdir("md_sub/step_" + step_name)

    # SAVE ALL TEXT EXCEPT COORDS IN xyz
    save_coords = True
    # inp: HEADERS OF INPUT FILES 
    inp         = []
    # ut: HOLDS SYMBOL AND ATOM NUMBER
    ut          = []
    for line in original_f:
        if save_coords:
            inp.append(line)
        if re.search('END', line):
            save_coords = True
        elif not save_coords:
            line_mod = line.split()
            ut.append([line_mod[0], line_mod[1]])   
        if re.search('FMOXYZ', line):
            save_coords = False
        elif not FMO:
            if re.search('C1', line):
                save_coords = False
    
    # ADD NEW COORDS TO xyz
    for i in range(0, p_no):
        for j in range(0, d_no):
            
            #print(coords[i][j])
            ut[i].append(float(coords[i][j]))
    '''lines_job = [
                 "#!/bin/bash"                   ,
                 "#PBS -P k96 "                  ,
                 "#PBS -q express"               ,
                 "#PBS -l walltime=00:20:00"      ,
                 "#PBS -l ncpus=1"              ,
                 "#PBS -l mem=3GB"              ,
                 "#PBS -l jobfs=60GB"            , 
                 "#PBS -l wd"                    ,
                 ""                              ,
                 "module unload openmpi/1.6.3"   ,
                 "module load openmpi/1.8.4"     ,
                 "/short/k96/apps/gamess/rungms.rika water.inp $PBS_NCPUS 01 > water.log"
                                                  ]'''
    with open("job.inp", 'w+') as f:
        for line in inp:
            f.write(line)
        # WRITE FIRST COORDS AS STRING SO KEEPS ZEROS    
        if step == 0:
            for line in coords:
                f.write(' ' + line[3] + '  ' + line[4] + '  ' + line[0]\
                + '  ' + line[1] + '  ' + line[2] + '\n')
        else:
            for line in ut:
                f.write(' ' + line[0] + '  ' + line[1] + '{:21.13E}{:21.13E}{:21.13E}\n'\
                                                .format(line[2],line[3],line[4]))

        f.write(" $END")
    
    '''with open("job.job", 'w+') as f:
        f.writelines(lines_job)'''
    
    with open('step_' + step_name + '.xyz', 'w+') as f:
        # NUMBER OF LINES IN XYZ
        f.write(str(len(ut)) + '\n\n')
        # MAKE COORDS INTO FLOAT
        if step == 0:
            for line in coords:
                f.write(' ' + line[3] + '  ' + line[0] + '  ' + line[1] + '  ' + line[2] + '\n')
        else:
            for line in ut:
                f.write(line[0] + '{:21.13E}{:21.13E}{:21.13E}\n'.format(line[2],line[3],line[4]))
    
    # START GAMESS CALCULATION; JOB NOW OBSOLETE
    if step == 0:
        subprocess.call('rm /short/k96/zls565/tmp/job.F07', shell=True)
    #subprocess.call('rm *.dat', shell=True)
    #subprocess.call('module unload openmpi/1.6.2')
    #subprocess.call('module load openmpi/1.8.2')

    subprocess.call('/short/k96/zls565/gamess-scs/md-force-gms/rungms.rika job.inp > job.log', shell=True)
    #/short/k96/zls565/gamess-scs/md-force-gms/rungms.rika water.inp > water.log

    
    # READ IN FORCE DATA TO USE AS POTENTIAL
    potential = 0
   
    # PULL FORCE/POTENTIAL ENERGY FOR ENERGY OF STEP
    # fx(r) = -dU(r)/dx        (partial derivative)
    # fx(r) = -(x/r)(dU(r)/dr) (partial derivative)
    hold = [] # HOLD FORCE IN HARTREE/BOHR
    save = False
    plc1 = True
    plc2 = False
    look = False
    with open('job.log', 'r+') as f:
      if FMO:
        for line in f:
            if plc1:
                if 'NBODY' in line:
                    #print(line)
                    spl_line = line.split(' ')
                    for part in spl_line:
                        if 'NBODY' in part:
                            bdy = part.replace('NBODY=','')
                    plc2 = True
                    plc1 = False
            if plc2:
                if bdy == '2':
                    if re.search('Two-body FMO properties.', line):
                        look = True
                        plc2 = False
                if bdy == '3':
                    if re.search('Three-body FMO properties.', line):
                        look = True
                        plc2 = False
            if look:
                if '\n' == line:
                    save = False
                if save:
                    line   = line.split()
                    hold.append([line[0], line[1], line[2]])
                    #print(line)
                if "X------------------------------X" in line:
                    save = True
      
      elif not FMO:
        for line in f:
            if look:
                if not line.strip():
                    break
                h_line = line.split()
                hold.append([h_line[0], h_line[1], h_line[2]])
            # YOU NEED TP CHANGE THIS!!!
            if re.search("X------------------------------X", line):
                look = True
    
    # TRANSFER FORCE TO NUMPY ARRAY AND CONVERT TO GRAM*ANGSTROM/SECOND^2
    #print("force: %20.16e" % float(hold[0][2]))
    for i in range(0, p_no):
        for j in range(0, d_no):
            # force = -(energy gradient)
            # FORCE GIVEN IN HARTREE/BOHR CONVERSION FACTOR
            force[i,j] = '{:.15E}'.format(float(hold[i][j]))
            force[i,j] = float(hold[i][j]) * F2F
            force[i,j] = '{:.15E}'.format(force[i,j])
    #print("force: ", force[0,2])
    #print('f2f %24.19e' %F2F)

    # CONVERT TO POTENTIAL !
    if mtd:
        force = metadynamics(d_no, p_no, dt, step, coords, force)

    # MOVE TO STARTING DIRECTORY
    os.chdir(cwd)

    return force, potential
    
