import os
import sys
import inspect
import numpy as np
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import subprocess
import utils


params=sys.argv[2].split()
dict_params= {params[i][1:] : params[i+1] for i in range (0,(len(params)-1),2)}
utils.run_SCIP_with_optano(instance=str(sys.argv[1]),params=dict_params)
