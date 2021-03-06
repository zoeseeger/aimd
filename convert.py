# BOHR TO ANGSTROM
AU2ANG = 0.52917724924 

# FOR FORCE FROM GAMESS
AU2KCAL =  4.359816E-18 / 1.380658E-23 * 1.98721984E-03

EK2KCAL = 2.39005738055577E-27 * AU2ANG * AU2ANG

# FROM HARTREE/BOHR TO AMU-BOHR/s^2
F2F = -AU2KCAL / EK2KCAL

# FROM AMU MASS TO KG
AMU2KG = 1.66053904020E-27

# BOHR TO METER
AU2METER = AU2ANG * 1E-10

# BOLTZMANN CONSTANT
kB = 1.3806485279E-23
