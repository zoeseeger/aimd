# --------------------------------------
# UPDATES VELOCITIES/ACC USING VELOCITY VERLET
# -------------------------------------
def update_vel (p_no, d_no, coords, vel, force, force_prev, dt, step):
    # UPDATE VELOCITIES - VELOCITY VERLET TAYLOR SERIES EXPANSION FOR VELOCITIES
    # v(t+dt) = v(t) + (force(t) + force(t+dt)) * 1/2 * 1/mass * dt
    #print([[vel[0,0], force[0,0], force_prev[0,0], float(coords[0][5])]])
    for i in range(0, p_no):
        for j in range(0, d_no):
            vel[i,j] = vel[i,j] + 0.5 * dt * (force[i,j]  + force_prev[i,j]) / float(coords[i][5])
            vel[i,j] = '{:.8e}'.format(vel[i,j])
            vel[i,j] = float(vel[i,j])
    #print(vel)    
    # COMPUTE KINETIC ENERGY
    # USED TO FIND TOTAL ENERGY (+ POTENTIAL) AND FIND % ERROR IN CALC !
    kinetic = 0.0
    for k in range(0, p_no):
        for j in range(0, d_no):
            # COORDS[5] = ATOMIC MASSES
            # 1/2 * m * v^2 ; CONVERSION FACTOR 1e-23 
            kinetic = kinetic + 0.5 * float(coords[k][5]) * vel[k,j] ** 2 
    return vel, force_prev, kinetic

