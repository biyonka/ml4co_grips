'''
Parse a SCIP log file and returns statistics
@author A. Mélissa, B. Liang, E. Vercesi, A. Zhang
'''
import gzip
import re

class Log:
    def __init__(self, path):
        self.path = path

    def vectorise(self):
        '''
        Vectorize both a .log.gz or a .log file
        :return: list of lines of the log file
        '''
        if ".gz" in self.path[-3:]:
            F =  gzip.open(self.path, 'rt')
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
    #path = "./logs_example/item_placement_0.mps.gz.log"
    path = "./logs_example/item_placement_908.log.gz"
    l = Log(path)
    features = l.parse()
