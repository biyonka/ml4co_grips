import ConfigSpace.hyperparameters as CSH
import ConfigSpace as CS
from smac.scenario.scenario import Scenario

class SMACscenario :
    def __init__(self,arg_name_folder):
        # Define configuration space
        self.hyperparams = [
            CSH.CategoricalHyperparameter('branching/scorefunc', ['s', 'p', 'q'], default_value='q'),
            CSH.UniformFloatHyperparameter('branching/scorefac', 0, 1, default_value=0.167),
            CSH.CategoricalHyperparameter('branching/preferbinary', [True, False], default_value=False),
            CSH.UniformFloatHyperparameter('branching/clamp', 0, 0.5, default_value=0.2),
            CSH.UniformFloatHyperparameter('branching/midpull', 0, 1, default_value=0.75),
            CSH.UniformFloatHyperparameter('branching/midpullreldomtrig', 0, 1, default_value=0.5),
            CSH.CategoricalHyperparameter('branching/lpgainnormalize', ['d', 'l', 's'], default_value='s'),
            CSH.CategoricalHyperparameter('lp/pricing', ['l', 'a', 'f', 'p', 's', 'q', 'd'], default_value='l'),
            CSH.UniformIntegerHyperparameter('lp/colagelimit', -1, 2147483647, default_value=10),
            CSH.UniformIntegerHyperparameter('lp/rowagelimit', -1, 2147483647, default_value=10),
            CSH.CategoricalHyperparameter('nodeselection/childsel', ['d', 'u', 'p', 'i', 'l', 'r', 'h'],
                                          default_value='h'),
            CSH.UniformFloatHyperparameter('separating/minortho', 0, 1, default_value=0.9),
            CSH.UniformFloatHyperparameter('separating/minorthoroot', 0, 1, default_value=0.9),
            CSH.UniformIntegerHyperparameter('separating/maxcuts', 0, 2147483647, default_value=100),
            CSH.UniformIntegerHyperparameter('separating/maxcutsroot', 0, 2147483647, default_value=2000),
            CSH.UniformIntegerHyperparameter('separating/maxroundsroot', -1, 2147483647, default_value=-1),
            CSH.UniformFloatHyperparameter('separating/minefficacyroot', 0, 1e+98, default_value=0.0001),
            CSH.UniformIntegerHyperparameter('separating/cutagelimit', -1, 2147483647, default_value=80),
            CSH.UniformIntegerHyperparameter('separating/poolfreq', -1, 65534, default_value=10),
            CSH.UniformIntegerHyperparameter('presolving/maxrounds', -1, 2147483647, default_value=-1),
            CSH.UniformFloatHyperparameter('presolving/abortfac', 0, 1, default_value=0.0008),
            CSH.UniformIntegerHyperparameter('presolving/maxrestarts', -1, 2147483647, default_value=-1)
        ]
        self.configspace = CS.ConfigurationSpace()
        self.set_configSpace()
        self.arg_name_folder=arg_name_folder

    def set_configSpace(self) :
        for hp in self.hyperparams:
            self.configspace.add_hyperparameter(hp)

    def get_configSpace(self):
        return self.configspace



    def get_scenario(self):
        return Scenario({
            "run_obj": "quality",  # Optimize quality (alternatively runtime)
            "cs": self.get_configSpace(),
            "output_dir" : "SMAC3_output/" + self.arg_name_folder,
            "train_inst_fn" : "1_instances_path_train.txt",
            "test_inst_fn": "1_instances_path_test.txt",
            "algo_runs_timelimit" : 60
        })

