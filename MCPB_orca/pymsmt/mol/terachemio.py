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
#-----------------------Read info from terachem output file--------------------
#------------------------------------------------------------------------------

def split_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def get_matrix_from_terachem(filename,nrows):
    sort_values = [0]
    conversionf = 2240.036 ## # from hartree Bohr-2 to Kcal mol Angstr-2 ### not sure about this
    conversionf = 1
    with open(filename, 'r') as f:
        data = f.readlines()
    start = 0
    end = 0
    for sort, line in enumerate(data):
        if '*** Hessian Matrix ' in line:
            start = sort 
        elif 'Dipole moment derivatives:' in line:
            end = sort - 1
    hessian_session = data[start:end]
    for sort, line in enumerate(hessian_session):
        if line == '\n':
            sort_values.append(sort)
    
    hessian_matrix_all = []
    
    for i in range(len(sort_values)-1):
        start = sort_values[i] + 3
        end = sort_values[i+1]
        session = hessian_session[start:end]
        new_session = []
        for j in session:
            newline = [ float(value) * conversionf for value in j.split()[1:] ]
            new_session.append(newline)
        hessian_matrix_all.append(new_session)
    
   # print(len(hessian_matrix_all))
    if len(hessian_matrix_all) > 1:
        new_matrix = hessian_matrix_all[0]
        for m in hessian_matrix_all[1:]:
            new_matrix = np.hstack((new_matrix,m))
      #  print(new_matrix)
        assert new_matrix.shape == (nrows,nrows)
        return new_matrix 
    else:
        new_matrix = hessian_matrix_all[0]
        assert new_matrix.shape == (nrows,nrows)
        return new_matrix 
    #print(new_matrix * conversionf)

def get_crds_from_terachem(trjxyz,atomnumber):
    crds = []
    with open(trjxyz, 'r') as f:
        crds_raw = f.readlines()
    crdsall = split_list(crds_raw, atomnumber + 2)
    opt_structure = crdsall[-1][2:]
    for line in opt_structure:
        crd_floats = [float(x) / B_TO_A for x in line.split()[1:]]
        crds.extend(crd_floats)
    return crds