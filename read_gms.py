# -----------------------------
# READ IN GAMESS INPUT FILE
# -----------------------------

def xyz(file):
    import sys
    import re
    #from periodictable import C,H,Cl,B,F,N,O 
    from masses import masses_dict
    import numpy as np
    
    # USE "script.py filename.inp"
    '''if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        print("No file name given with script, will terminate.")
    file = sys.argv[1]'''
    
    name = file.replace('.inp', '')

    # COORDS SAVED 
    save_coords = False
    coords      = []
    FMO         = False
    # COORDS IS LIST OF LISTS; [ATM SYMBOL, ATOMIC NUMBER, X, Y, Z, APPEND MASS]
    with open(file, 'r+') as f:
        original_f = f.readlines()
        for line in original_f:
            if re.search('FMOXYZ', line):
                FMO = True
                break
        for line in original_f:
            if 'END' in line:
                save_coords = False
            if save_coords:
                line = line.split()
                # ORDER CHANGED: X, Y, Z, SYM, ATM#, APPEND MASS
                coords.append([line[2],line[3],line[4],line[0],line[1]])    
            elif re.search('FMOXYZ', line):
                save_coords = True
            elif not FMO:
                if re.search('C1', line):
                    save_coords = True

    # CONVERT COORDS TO BOHRS
    #for j in range(0,len(coords)): 
    #    for i in range(0,3):
    #        coords[j][i] = float(coords[j][i]) / 0.52917724924
    # CHARGE == ATOMIC NUMBER,
    # MAKE SECOND LETTER OR MORE LOWERCASE SO CAN BE READ BY periodictable
    for i in coords:
        if len(i[3]) > 1:
            for lett in i[3]:
                if lett == i[3][0]:
                    symbol = lett
                else:
                    symbol = symbol + lett.lower()
                    i[3] = symbol
    # APPEND MOLAR MASS
    for i in range(0,len(coords)):
        if coords[i][3] in masses_dict:
            coords[i].append(masses_dict[coords[i][3]])
        else:
            print('Could not find ' + i + ' in elemental masses.')
    return name, original_f, coords, FMO


