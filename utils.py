'''
Parse a SCIP log file and returns statistics
@author A. Mélissa, B. Liang, E. Vercesi, A. Zhang
'''
import gzip
import os
import re
import subprocess
import sys


class Log:
    def __init__(self, path):
        self.path = path

    def vectorise(self):
        '''
        Vectorize both a .log.gz or a .log file
        :return: list of lines of the log file
        '''
        if ".gz" in self.path[-3:]:
            F = gzip.open(self.path, 'rt')
        else:
            F = open(self.path, 'r')
        lines = F.readlines()
        F.close()
        return lines

    def get_primal_dual_integral(self):
        lines = self.vectorise()
        line = filter(lambda x: "primal-dual" in x, lines)
        total, avg = [float(s) for s in next(line).split(" ") if
                      (len(s) > 0 and re.match(r'^-?\d+(?:\.\d+)$', s) is not None)]
        return float(total), float(avg)

    def get_gap(self):
        lines = self.vectorise()
        line = filter(lambda x: "Gap " in x, lines)
        gap = next(line).split(":")[1].strip().rstrip("%")
        try:
            return float(gap)
        except:
            return float('inf')

    def get_running_time_first_feasible(self):
        lines = self.vectorise()
        try: 
            line = filter(lambda x: "First Solution" in x, lines)
            time = next(line).split("seconds")[0].split(",")[-1]
            return float(time)
        except:
            return sys.float_info.max

    def get_primal_bound(self):
        lines = self.vectorise()
        line = filter(lambda x: "Primal Bound       " in x, lines)
        primal_bound = next(line).split(":")[1].split("(")[0].strip()
        return float(primal_bound)

    def get_dual_bound(self):
        lines = self.vectorise()
        line = filter(lambda x: "Dual Bound         " in x, lines)
        dual_bound = next(line).split(":")[1].strip()
        return float(dual_bound)

    def get_number_of_bb_nodes(self):
        lines = self.vectorise()
        line = filter(lambda x: "nodes            " in x, lines)
        bb_nodes = next(line).split(":")[1].split("(")[0]
        return int(bb_nodes)

    def get_root_node_solving_time(self):
        lines = self.vectorise()
        try:
            line = filter(lambda x: "First LP Time" in x, lines)
            root_node_time = next(line).split(":")[-1].strip()
            return float(root_node_time)
        except:
            return sys.float_info.max

    def get_LP_iter_freq(self):
        lines = self.vectorise()
        line = filter(lambda x: "dual LP" in x, lines)
        freq = next(line).split(":")[1].split()[2]
        return int(freq)

    def get_time(self):
        lines = self.vectorise()
        line = filter(lambda  x : "Total Time" in x, lines)
        time = next(line).split(":")[1].strip()
        return float(time)

    def parse(self):
        return {
            "Primal-Dual Integral Value": self.get_primal_dual_integral()[0],
            "Primal-Dual Integral Percentage": self.get_primal_dual_integral()[1],
            "Gap": self.get_gap(),
            "Time First Feasible": self.get_running_time_first_feasible(),
            "Primal Bound": self.get_primal_bound(),
            "Dual Bound": self.get_dual_bound(),
            "B&B Tree nodes": self.get_number_of_bb_nodes(),
            "Time to Solve Root Node": self.get_root_node_solving_time(),
            "Number of LP Iterations": self.get_LP_iter_freq(),
            "Total Time" : self.get_time()
        }


class SCIP:
    def __init__(self):
        pass

    def write_parameter_file(self, D, filename="scip.set", timelimit=-1):
        '''
        Method from writing parameter file from a dictionary
        :param D: dict, keys: SCIP parameters, values : va
        :param filename: str, name of the parameter file
        :param timelimit: set a timelimit; default: no timelimit = -1
        :param seed : set gloab seed
        :param compress_log: set True if you want a compressed log; useful for big files
        :param q: set to true if you want the output to not appear on the sdout
        '''
        F = open(filename, "w")
        for param in D.keys():
            F.write(param + "=" + str(D[param]) + "\n")
        if timelimit > 0:
            F.write("limits/time={}".format(timelimit))
        F.close()

    def run(self, path, logfile="logfile.log", parameter_configuration="scip.set", seed=42, compress_log=True, q=True):
        subprocess.run(
            "scip -l {} {} -s {} {} -f {}".format(
                logfile, "-q" if q else "", parameter_configuration, "-r " + str(seed) if seed > 0 else "", path
            ),
            shell=True)
        if compress_log:
            subprocess.run("gzip --force {}".format(logfile), shell=True)


def run_SCIP_with_smac(config, budget, instance, seed=42):
    '''

    # Method to define SCIP as TAE (target algorithm evaluator) ie model for SMAC
    :param config: configuration type object,
    :param budget: timelimit
    :param instance:
    :param seed:
    :return: primal dual integral percentage to be minimized by SMAC

    '''
    from SMAC.scenario import SMACscenario
    output_folder = sys.argv[1]
    smacscenario = SMACscenario(output_folder)
    configspace = smacscenario.get_configSpace()
    scip = SCIP()
    # Trying to generate the config with a sample
    sample_cfgs = configspace.sample_configuration()  # this creates a configuration type object
    sample_cfgs_dict = {k: sample_cfgs[k] for k in sample_cfgs}  # you can turn this object into a dictionary

    #Creating a separated folder for each run

    path_to_run_folder= "./SMAC3_output/" + output_folder + "/"
    instance_file_name = instance.split("/")[-1]
    instance_new = path_to_run_folder  + instance_file_name
    scip.write_parameter_file(sample_cfgs_dict, filename=instance_new + "_SMAC.set", timelimit=180)
    scip.run(instance, logfile=instance_new + ".log", parameter_configuration="{}_SMAC.set".format(instance_new), seed=seed,
             q=False)

    l = Log(instance_new + ".log.gz").get_primal_dual_integral()[1]
    os.remove("{}_SMAC.set".format(instance_new))
    os.remove(instance_new + ".log.gz")
    return l


if __name__ == "__main__":
    # Testing section
    pass
    # path = "./logs_example/item_placement_0.mps.gz.log"
    # path = "./logs_example/item_placement_908.log.gz"
    # l = Log(path)
    # features = l.parse()
    # SCIP().run("hb/instances/item_placement_0.mps.gz", parameter_configuration="scip.set", q=False)
