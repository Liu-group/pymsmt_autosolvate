"""
module for writting a orca  file and read the coordinates and force
constants from Gaussian output file.
"""

import numpy as np
import linecache
from pymsmt.exp import *
from pymsmt.mol.constants import B_TO_A
from parmed.periodic_table import AtomicNum
import sys
import collections
import math

#------------------------------------------------------------------------------
#-----------------------Read info from orca output file--------------------
#------------------------------------------------------------------------------

def get_matrix_from_orca(orcahess,nrows):
    fc = np.zeros((nrows,nrows),float)
    nrows = nrows
    conversionf = 2240.48 # from hartree Bohr-2 to Kcal mol Angstr-2
    conversionf = 1
    try:
        with open(orcahess, 'r') as f:
            hessian_found = False
            for line in f:
                if '$hessian' in line:
                    hessian_found = True
                # print(line)
                    break

            if hessian_found:
                line = f.readline()
                fc = np.zeros((nrows, nrows), float)
                for i in range((nrows + 4) // 5):
                    line = f.readline()
                    for j in range(nrows):
                        data = f.readline().split()[1:]
                        for k in range(len(data)):
                            fc[j, i * 5 + k] = float(data[k])
        fc = fc * conversionf
        return fc
    except FileNotFoundError:
        print("Erorr:",orcahess, "file not found")



def get_crds_from_orca(trjxyz, orcaout):
    check = False
    atomnumber = None
    crds = []
    #### check opt finish #####
    try:
        with open(orcaout) as f:
            for line in f:
                if " ****ORCA TERMINATED NORMALLY****" in line:
                    check = True
                    print("ORCA opt terminated normally")

    except FileNotFoundError:
        print("Erorr:",orcaout, "file not found")

    if check:
        try:
            with open(trjxyz, 'r') as f:
                firstline = f.readline()
                atomnumber = list(firstline.strip())
                if len(atomnumber[0].split()) == 1:
                    atomnumber = int(firstline)
                    queue = collections.deque(f,maxlen=atomnumber)
                    queue = list(queue)
                    if len(queue) != atomnumber:
                        print('Erorr: Reading orca trj file has an error, please check the space and newline character.')
                        sys.exit()
                    else:
                        for crd in queue:
                            crd = crd.strip()
                            if len(crd.split()) != 4:
                                print('Erorr: wrong format of orca trj xyzfile')
                                sys.exit()
                            else:
                                crd_floats = [float(x)/B_TO_A for x in crd.split()[1:4]]
                                crds.extend(crd_floats)
    
        except FileNotFoundError:
            print("Erorr:",trjxyz, "file not found")
        
        except ValueError:
            print("Erorr: ","wrong format of orca trj xyzfile")
        
    else:
        print("Erorr: ORCA opt is not terminated normally")
    
    return crds

def get_esp_from_orca(gwf,xyzfile,espout,espfile):
    pass



