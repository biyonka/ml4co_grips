"function (and parameter space) definitions for hyperband"
#Simple SCIP run

from common_defs import *
from scipy.stats import gmean


list_of_instances = [
    "./instances/item_placement_0.mps.gz",
   "./instances/item_placement_1.mps.gz",
    "./instances/item_placement_2.mps.gz",
    "./instances/item_placement_3.mps.gz"
    ]

#define configuration space
#http://hyperopt.github.io/hyperopt/getting-started/search_spaces/
#default values in comment next to each param
space = {
'branching/scorefunc': hp.choice('bsf', ('s', 'p', 'q')), #q
'branching/scorefac': hp.uniform('bsfac', 0, 1), #0.167
'branching/preferbinary': hp.choice('bpb', (True, False)), #false
'branching/clamps': hp.uniform('bc', 0, 0.5), #0.2
'branching/midpull': hp.uniform('bmp', 0, 1), #[0.75]
'branching/midpullreldomtrig': hp.uniform('bmpr', 0, 1),# [0.5]
'branching/lpgainnormalize': hp.choice('blpgn', ('d','l','s')),# [s]
'lp/pricing': hp.choice('lpp', ('l','a','f','p','s','q','d')), #[l]
"lp/colagelimit":hp.quniform('lpcl', -1, 2147483647, 1), # [10] 
'lp/rowagelimit': hp.quniform('lprl', -1, 2147483647, 1),# [10]
'nodeselection/childsel': hp.choice('nscs',('d','u','p','i','l','r','h')), #[h]
'separating/minortho': hp.uniform('smo', 0, 1),# [0.9]
'separating/minorthoroot': hp.uniform('smor', 0, 1),# [0.9]
'separating/maxcuts': hp.quniform('smc', 0, 2147483647,1), # [100]
'separating/maxcutsroot': hp.quniform('smcr',0,2147483647, 1), #[2000]
'separating/maxroundsroot': hp.quniform('smrr',-1, 2147483647, 1), #[-1]
'separating/minefficacyroot': hp.uniform('smef', 0, 1e+98), #[0.0001]
'separating/cutagelimit': hp.quniform('cl',-1, 2147483647, 1), #[80]
'separating/poolfreq': hp.quniform('spf',-1, 65534, 1), #[10]
'presolving/maxrounds': hp.quniform('pmr',-1, 2147483647, 1), #[-1]
'presolving/abortfac': hp.uniform('paf', 0,1), #[0.0008]
'presolving/maxrestarts': hp.quniform('pmre',-1, 2147483647, 1)#[-1]
}

def get_params():
    params = sample(space)
    return handle_integers(params)

#n_iterations is just the resource we are allocating (tree size for now, can change later)
def try_params(resource, params):
    print('tree size', resource)

    #Allocate resource to SCIP
    params['limits/nodes'] = resource
    
    #Add time limit to scip params, use 3 minutes for now
    params['limits/time'] = 180	
    pprint(params)
    
    #run SCIP on instances to get list of performance measures (one per instance)
    scip_gap = run_and_eval_scip(params, list_of_instances, feature="Gap")
    scip_pd_val = run_and_eval_scip(params, list_of_instances, feature="Primal-Dual Integral Value")
    optimizing_stat = gmean(scip_gap)
    pd_val = gmean(scip_pd_val)
    return {'loss': optimizing_stat, 'PDIntVal':  pd_val, 'Gap': optimizing_stat}
