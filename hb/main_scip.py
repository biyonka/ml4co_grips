#!/usr/bin/env python

import sys
import pickle as pickle
from pprint import pprint

from hyperband import Hyperband
from defs_scip.scip import get_params, try_params

try:
    output_file = sys.argv[1]
    if not output_file.endswith('.pkl'):
        output_file += '.pkl'
except IndexError:
    output_file = 'results.pkl'

print("Will save results to", output_file)


hb = Hyperband(get_params, try_params)
results = hb.run(skip_last=0)

print("{} total, best:\n".format(len(results)))

for r in sorted(results, key=lambda x: x['loss'])[:5]:
    print("PDIntPerc: {} | {} seconds | {:.1f} resource | run {} ".format(
        r['loss'], r['seconds'], r['resource'], r['counter']))
    pprint(r['params'])
    print()

print("saving...")

with open(output_file, 'wb') as f:
    pickle.dump(results, f)
