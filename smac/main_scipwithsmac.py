import ConfigSpace.hyperparameters as CSH
from smac.facade.smac_bb_facade import SMAC4BB
from smac.facade.hyperband_facade import HB4AC
from smac.scenario.scenario import Scenario
import ConfigSpace as CS
from smac.utils import *


#Define configuration space
hyperparams=[
CSH.CategoricalHyperparameter('branching/scorefunc', ['s', 'p', 'q'],default_value='q'),
CSH.UniformFloatHyperparameter('branching/scorefac', 0, 1,default_value=0.167),
CSH.CategoricalHyperparameter('branching/preferbinary', [True, False],default_value=False),
CSH.UniformFloatHyperparameter('branching/clamps', 0, 0.5,default_value=0.2),
CSH.UniformFloatHyperparameter('branching/midpull', 0, 1,default_value=0.75),
CSH.UniformFloatHyperparameter('branching/midpullreldomtrig', 0, 1,default_value=0.5),
CSH.CategoricalHyperparameter('branching/lpgainnormalize', ['d','l','s'],default_value='s'),
CSH.CategoricalHyperparameter('lp/pricing', ['l','a','f','p','s','q','d'],default_value='l'),
CSH.UniformIntegerHyperparameter('lp/colagelimit', -1, 2147483647,default_value=10),
CSH.UniformIntegerHyperparameter('lp/rowagelimit', -1, 2147483647,default_value=10),
CSH.CategoricalHyperparameter('nodeselection/childsel',['d','u','p','i','l','r','h'],default_value='h'),
CSH.UniformFloatHyperparameter('separating/minortho', 0, 1,default_value=0.9),
CSH.UniformFloatHyperparameter('separating/minorthoroot', 0, 1,default_value=0.9),
CSH.UniformIntegerHyperparameter('separating/maxcuts', 0, 2147483647,default_value=100),
CSH.UniformIntegerHyperparameter('separating/maxcutsroot', 0, 2147483647,default_value=2000),
CSH.UniformIntegerHyperparameter('separating/maxroundsroot', -1, 2147483647,default_value=-1),
CSH.UniformFloatHyperparameter('separating/minefficacyroot', 0, 1e+98,default_value=0.0001),
CSH.UniformIntegerHyperparameter('separating/cutagelimit', -1, 2147483647,default_value=80),
CSH.UniformIntegerHyperparameter('separating/poolfreq', -1, 65534,default_value=10),
CSH.UniformIntegerHyperparameter('presolving/axrounds', -1, 2147483647,default_value=-1),
CSH.UniformFloatHyperparameter('presolving/abortfac', 0, 1,default_value=0.0008),
CSH.UniformIntegerHyperparameter('presolving/maxrestarts', -1, 2147483647,default_value=-1)
]

configspace = CS.ConfigurationSpace()
for hp in hyperparams :
    configspace.add_hyperparameter(hp)


# Provide meta data for the optimization
scenario = Scenario({
    "run_obj": "quality",  # Optimize quality (alternatively runtime)
    "runcount-limit": 10,  # Max number of function evaluations (the more the better)
    "cs": configspace,
    "train_inst_fn" : "instance_path",
    "algo_runs_timelimit" : 60
})

#smac = SMAC4BB(scenario=scenario, tae_runner=run_SCIP_with_smac)
smac = HB4AC(scenario=scenario, tae_runner=run_SCIP_with_smac)
best_found_config = smac.optimize()