#!/short/k96/apps/bin/python3.6
#xxx
# -----------------------
# INTERFACE WITH TSK FILE
# -----------------------
import sys
from main import md 
from read_gms import xyz

#try:
#    tsk = sys.argv[1]
#except:
#    sys.exit('Task file not supplied.')
tsk = "task"

ptf = False # must be true to continue
sn  = False # must be true to continue
mt  = False # must be true to continue
tmp = False # must be true to continue

mtd = False # default metadyn:false
rst = False # default restart:false

with open(tsk, 'r+') as f:
  for line in f:
    if 'path_to_file' in line:
        path_to_file = line.split()[1]
        ptf          = True

    elif 'step_no' in line:
        s_no = int(line.split()[1])
        sn   = True

    elif 'dt' in line:
        dt = float(line.split()[1])
        mt = True

    elif 'temp' in line:
        temp = float(line.split()[1])
        tmp  = True

    elif 'restart' in line:
        # RESTART DEFAULT FALSE
        rst = line.split()[1]
        if rst == 'True' or rst == 'TRUE':
            rst = True
        elif rst == 'False' or rst == 'FALSE':
            rst = False
        else:
            sys.exit("Error input: restart value not boolean")

    elif 'mtd' in line:
        # METADYNAMICS DEFAULT FALSE
        mtd = line.split()[1]
        if mtd == 'True' or mtd == 'TRUE':
            mtd = True
        elif mtd == 'False' or mtd == 'FALSE':
            mtd = False
        else:
            sys.exit("Error input: mtd value not boolean")


if not ptf:
    sys.exit("Error input: 'path_to_file' not found in tsk")
if not sn:
    sys.exit("Error input: 'step_no' not found in tsk")
if not mt:
    sys.exit("Error input: 'dt' not found in tsk")
if not tmp:
    sys.exit("Error input: 'temp' not found in tsk")

# THE MD SIMULATION
md(path_to_file, s_no, dt, temp, rst, mtd)
    
