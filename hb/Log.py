'''
Parse a SCIP log file and returns statistics
@author A. Mélissa, B. Liang, E. Vercesi, A. Zhang
'''

import re

# TODO add more comments, documentation is missing
class Log:
    def __init__(self, path):
        self.path = path

    def vectorise(self):
        with open(self.path) as F:
            return F.readlines()

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
        line = filter(lambda x: "First Solution" in x, lines)
        time = next(line).split("seconds")[0].split(",")[-1]
        return float(time)

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

    def parse(self):
        return {
            "Primal-Dual Integral Value": self.get_primal_dual_integral()[0],
            "Primal-Dual Integral Percentage": self.get_primal_dual_integral()[1],
            "Gap": self.get_gap(),
            "Time First Feasible": self.get_running_time_first_feasible(),
            "Primal Bound": self.get_primal_bound(),
            "Dual Bound": self.get_dual_bound(),
            "B&B Tree nodes": self.get_number_of_bb_nodes()
        }


if __name__ == "__main__":
    # Testing section
    path = "item_placement_1064.mps.gz.log"
    l = Log(path).parse()
