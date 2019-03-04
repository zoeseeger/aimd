# METADYNAMICS ROUTINE

def metadynamics(d_no, p_no, dt, step, coords, force):

    import sys, math

    # TO PUT IN TSK FILE
    w   = 0.1   # height of gaussian
    sig = 0.1   # width of gaussian
    tau = 100   # frequency of gaussian deposition
    max_gauss = 1000

    n_gauss = 0 # NUMBER OF ADDED GAUSSIANS
    S = [] # LIST OF CV VALUES AT EACH TAU
    dist = []
    ds_dr = [] # LIST OF LISTS DERIVATIVES FOR ATOM 1 & 2


    # CALCULATE THE VALUE OF CV AND ITS DERIVATIVES
    #-----------------
    # CODE SPECIFIC TO CVs OF CHOICE
    # ALTHOUGH MAY NEED TO CHANGE LOOPS AND CONTAINERS FOR MORE CVs

    # CV OF DISTANCE BETWEEN ONLY TWO ATOMS

    # GET CV VALUE, S,  AND THREE ITEM LIST OF DISTANCES
    s = 0
    for i in d_no:
        distn = (float(coords[0][i]) - float(coords[1][i]))**2
        s     = s + distn
        dist.append(distn)

    # CV VALUE
    s = math.sqrt(s)

    # DERIVATIVES FOR ATOM 1 AND ATOM 2

    ds_dr.append([ dist[0]/s,  dist[1]/s,   dist[2]/s])
    ds_dr.append([-dist[0]/s, -dist[1]/ s, -dist[2]/s])

    #-----------------

    # IF A MULTIPLE OF TAU - TIME BETWEEN ADDED GAUSSIANS

    # STEP * TIME_STEP (dt) = TIME & TIME % tau == 0
    if step % ( tau / dt) == 0:
        n_gauss += 1

        if n_gauss < max_gauss:
            S.append(s)
        else:
            sys.exit("Successful run: max_gauss exceeded")

    ### WRITE SOMETHING TO FILE

    # FIND DERIVATIVE OF POTENTIAL WRT CVS
    # SHOULD ALLOW MULTIPLE CVS

    dV_ds = 0

    for stau in S:
        V     = w * math.exp(-(s-stau)**2 /2 /sig**2)
        dV_ds = dV_ds + V * (s-stau)**2 /2 /sig**2


    # ADD TO FORCES
    for i in range(0, p_no):
        for j in range(0, d_no):
            force[i,j] = force[i,j] - dV_ds * ds_dr[i][j]

    return force

