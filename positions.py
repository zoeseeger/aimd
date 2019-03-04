# -------------------------------------
# UPDATE POSITIONS
# -------------------------------------
def update_pos (p_no, d_no, coords, vel, force, dt, step):
    from convert import AU2ANG

    # UPDATE POSITIONS
    #print("coord: %20.16e" % float(coords[0][2]))
    # PRINT TO 16 SIG FIGS
    #print("vel: %20.16e" % vel[0,2])
    #print("force: %20.16e" % force[0,2])
    #print([float(coords[0][0]), vel[0,0], dt, force[0,0], (coords[0][5])])
    for i in range(0, p_no):
       for j in range(0, d_no):
            # VELOCITY VERLET; TAYLOR SERIES EXPANSION FOR COORDS
            # r(t+dt) = r(t) + v(t)*dt + 1/2 * force(t)/mass * dt**2 
            # f(t) = a(t)/mass & f(t+dt) = force
            acc = force[i,j] / (coords[i][5])
            
            # TO COMPLY WITH GAMESS
            coords[i][j] = '{:.14E}'.format(float(coords[i][j]) / AU2ANG)
            #print([coords[i][j], vel[i,j], dt, force[i,j]])
            #print(float(coords[i][j]) + vel[i,j] * dt + 0.5 * acc * dt * dt)
            coords[i][j] = (float(coords[i][j]) + \
                        vel[i,j] * dt + 0.5 * acc * dt * dt) * AU2ANG
            #coords[i][j] = float(coords[i][j]) + \
            #            (vel[i,j] * dt + 0.5 * acc * dt * dt) * AU2ANG
            coords[i][j] = '{:.10e}'.format(coords[i][j])
    #print(coords)
    #print("coord: %20.16e" % float(coords[0][2]))
            
    return coords

