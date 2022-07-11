'''
Stratified sample ancording to a certain feature
@author M. AIDLI, G. Iommazzo, B. Liang, E. Vercesi, A. Zhang
'''
import os
import numpy as np
from utils import *
import argparse
from sklearn.model_selection import train_test_split
import time
from collections import Counter

def write_file(family, set_of_instances, file_name):
    F = open(file_name, "w+")
    for i in set_of_instances:
        F.write(family + "_" + i + ".mps.gz\n")
    F.close()



##################
# Parser
##################
parser = argparse.ArgumentParser()
parser.add_argument("-d", metavar='d', help="Name of the directory with the log files under study")
parser.add_argument("-s", metavar='s', help="Sample size you want to extract (Train size + Test size)", type=int)
parser.add_argument("-r", metavar='r', help="Percentage of test set on total sample dimension", type=float)
parser.add_argument("-p", metavar='p', help="Problem name: one among item_placement, load_balancing, anonymous", type=str, default="item_placement")
parser.add_argument("-hm", metavar='hm', help="Measure of hardness to be collected and to cluster on", default="Primal-Dual Integral Percentage")
args = parser.parse_args()
directory = args.d
try:
    # Basic check of the passed directory name
    assert directory[-1] in ["/", "\\"]
except:
    raise ValueError("Directory path should end with / or \\")

# Store the name of the instance family in a variable
family = args.p

######################################
# Collect one score for each instance
######################################
# Note: some of the following passages can be avoided in case of complete exploration
names = [] # Name of the instance
scores = [] # Score to be collected
files = os.listdir(directory)

start = time.time()
while len(names) < args.s:
    # Pick one instance
    i = np.random.randint(0, len(files))
    file = files[i]
    # Verify wether the instance is in the folder
    if "{}_{}_3.log.gz".format(args.p, i) in files:
        # Split the name of the file, retrieve the number
        numb = file.split("_")[2]
        # If the number is not in the list name, collect the associated score
        if numb not in names:
            score = 0
            try: # Collect score only if you have three run on three different seeds
                for seed in [3, 4, 5]:
                    score += Log(directory + "item_placement_{}_{}.log.gz".format(i, seed)).parse()[args.hm]
                scores.append(score/3)
                names.append(numb)
            except:
                pass
print("Time for collecting a random sampling:", time.time() - start)

######################################
# Stratify
######################################
# Create three bins among min score and max score
bins = np.linspace(min(scores), max(scores), 3)
# Return the indices of the bins to which each value in input array belongs
y_binned = np.digitize(scores, bins)
# Print info on the created classes
counter_classes = Counter(y_binned)
for k in counter_classes.keys():
    print("Class", k, ":", counter_classes[k], "elements", flush=True)

######################################
# Divide between train and test
######################################
Xtr, Xte, ytr, yte = train_test_split(names, scores, stratify=y_binned, test_size=args.r)

print("Files for the training set:", len(Xtr), flush=True)
print("Files for the test set:", len(Xte), flush=True)

write_file(family, Xtr, "./SMAC/instance_path_train.txt")
write_file(family, Xte, "./SMAC/instance_path_test.txt")


