import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import utils

from smac.facade.smac_ac_facade import SMAC4AC
from scenario import scenario


smac = SMAC4AC(scenario=scenario, tae_runner=utils.run_SCIP_with_smac)
best_found_config = smac.optimize()