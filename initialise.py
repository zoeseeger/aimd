def initiate(path_to_file, d_no, temp, s_no, dt):
    
    import  sys
    import  numpy       as     np
    from    time        import clock, time
    from    times       import t_stamp
    from    read_gms    import xyz
    
    ### WRITING .md FILE
    
    wtime1 = clock()
    
    sys  = sys.version.split()

    ### GET STARTING DATA
    # COORDS: LIST OF LISTS; X, Y, Z, SYMBOL, CHARGE, MASS
    name, original_f, coords, FMO = xyz(path_to_file) 
    
    p_no = len(coords)

    # FOR NOW PRINT OUT
    with open(name + ".md", 'w+') as f:
    # STARTING PARAMS
        f.write(t_stamp() + '\n'                                                            )
        f.write('     Molecular Dynamics Simulator \n'                                      )
        f.write('     Written by Zoe Seeger, 2016\n'                                        )
        f.write('     This programme is using Python version ' + sys[0] + '\n'              )
        f.write('     With: \n'                                                             )
        f.write('         Spatial dimensions  : ' + str(d_no) + '\n'                        )
        f.write('         Number of particles : ' + str(p_no) + '\n'                        )
        f.write('         Temperature         : ' + str(temp) + '\n'                        )
        f.write('         Number of steps     : ' + str(s_no) + '\n'                        )
        f.write('         Time step (seconds) : ' + str(dt)   + '\n'                        )
        f.write('\n'                                                                        )
        f.write('   Step  Potential \t\t\t\t Kinetic \t\t\t\t Relative Error \n'            )
        f.write('   -------------------------------------------------------------------- \n')
    
    # --------------
    # INITIATION
    # --------------            
    # RANDOM DISTR. VELOCITES ABOUT 0
    '''mu, sigma = 0, 0.01          # CONSIDER SIGMA MORE CAREFULLY ! ***
    vel = np.random.normal(mu, sigma, size=(p_no, d_no)) ! 
    for row in vel:
        sum_velocity = 0
        for val in row:
            sum_velocity = sum_velocity + val
        #print("SUM OF VELOCITIES: ", sum_velocity)
        if sum_velocity > 0.2:  # CONSIDER CUTOFF MORE CAREFULLY, \
                                            WHAT IS TOO LARGE? !
            #print("SUM OF VELOCITIES ", sum_velocity, " TOO LARGE")

    active_temp = find_active_temp(d_no, p_no, vel, coords)

    # SCALING FACTOR OF OLD TEMP -> NEW TEMP FOR VELOCITIES 
    scale_temp  = math.sqrt(temp/active_temp)
    for i in range(0, p_no):
        for j in range(0, d_no):'''

    ### READ IN VELS FROM FILE
    vel  = np.zeros([p_no, d_no])

    with open('vels', 'r+') as f:
        for i, line in enumerate(f):
            line = line.split()
            for j, val in enumerate(line):
                vel[i, j] = float(val)

    return name, original_f, coords, vel, FMO


def restarting (path_to_file, d_no, temp, s_no, dt):
    
    import  os, sys
    import  numpy       as     np
    from    time        import clock, time
    from    times       import t_stamp
    from    read_gms    import xyz
    
    ### WRITING .md FILE
    wtime1 = clock()
    sys    = sys.version.split()
    
    # COORDS: LIST OF LISTS; X, Y, Z, SYMBOL, CHARGE, MASS
    # DISCARD COORDS
    name, original_f, coords, FMO = xyz(path_to_file) 
   
    p_no = len(coords)

    # FOR NOW PRINT OUT
    with open(name + ".md", 'a') as f:
    # STARTING PARAMS
        f.write('!!! RESTART !!!\n'                                                         )
        f.write(t_stamp() + '\n'                                                            )
        f.write('     Molecular Dynamics Simulator \n'                                      )
        f.write('     Written by Zoe Seeger, 2016\n'                                        )
        f.write('     This programme is using Python version ' + sys[0] + '\n'              )
        f.write('     With: \n'                                                             )
        f.write('         Spatial dimensions  : ' + str(d_no) + '\n'                        )
        f.write('         Number of particles : ' + str(p_no) + '\n'                        )
        f.write('         Temperature         : ' + str(temp) + '\n'                        )
        f.write('         Number of steps     : ' + str(s_no) + '\n'                        )
        f.write('         Time step (seconds) : ' + str(dt)   + '\n'                        )
        f.write('\n'                                                                        )
        f.write('   Step  Potential \t\t\t\t Kinetic \t\t\t\t Relative Error \n'            )
        f.write('   -------------------------------------------------------------------- \n')
    
    ### GET RESTART DATA VELS AND COORDS AND STEP NO
    
    # EXPECT .trj FILE
    coor  = False
    coord = []
    velo   = False
    veloc  = []
    forc   = False
    force  = []
    for File in os.listdir('.'):
        if File.endswith('.trj'):
            with open(File, 'r+') as f:
                for line in f:
                    if 'Coordinates in' in line or \
                       'COORDINATES IN' in line:
                        coor  = True
                        veloc = False
                        coord = []

                        # STEP NO // Step 80 COORDINATES IN ANGSTROM
                        line = line.split()
                        step = int (line[1])
                    
                    elif 'Velocities in' in line:
                        coor   = False
                        veloc  = True
                        velo   = []
                    elif 'Force in' in line:
                        coor  = False
                        veloc = False
                    elif coor:
                        line = line.split()
                        coord.append(line)
                    elif '-'*20 in line:
                        # DONT INCLUDE SPACER IN vel
                        pass
                    elif veloc:
                        line = line.split()
                        velo.append(line)

    ### CONVERT FORMAT
    vel = np.zeros([p_no, d_no])
    
    for i in range(0, p_no):         
        for j in range(0, d_no):
            coords[i][j] = float(coord[i][j])

    for i in range(0, p_no):         
        for j in range(0, d_no):
            vel[i, j] = float(velo[i][j])

    print(coords)
    print(' ')
    print(vel)

    return name, original_f, step, coords, force, vel, FMO


def finish():
    
    from time import clock, time
    from times import t_stamp

    with open(name + ".md", 'a') as f:
        t_stamp()
        wtime2 = clock()
        f.write(' Simulation human time = ')
        f.write(str(wtime2 - wtime1))
        f.write('\n Normal Execution.')




