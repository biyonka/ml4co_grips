import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import utils
from smac.facade.smac_ac_facade import SMAC4AC
from scenario import SMACscenario


smac = SMAC4AC(scenario=SMACscenario().get_scenario(), tae_runner=utils.run_SCIP_with_smac)
best_found_config = smac.optimize()
print("Best found config :", best_found_config)
file = open("best_found_config.txt", "w")
file.write(str(best_found_config))
file.close()
