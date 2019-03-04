# -------------------------------------
# FIND ACTIVE TEMPERATURE
# -------------------------------------
def find_active_temp(d_no, p_no, vel, coords):
    from convert import AMU2KG, AU2METER, kB
    # TEMPERATURE FROM VELOCITY MEAN SQUARED
    active_temp = 0
    for i in range(0, p_no):
        # T = m*v ^2 / 3 * N * k_B
        # DO m*v ^2 
        active_temp = active_temp + \
            (vel[i,0]*vel[i,0] + vel[i,1]*vel[i,1] + vel[i,2]*vel[i,2]) * coords[i][5]
    # / Nf * k_B where Nf ~ 3N (degrees of freedom) WITH CONVERSION FACTOR 1e-23
    active_temp = active_temp * AMU2KG * AU2METER * AU2METER / (3 * p_no * kB)
    return active_temp

