import numpy as np

from random import random
from math import log, ceil
from time import time, ctime
import pickle

class Hyperband:
	
	def __init__( self, get_params_function, try_params_function ):
		self.get_params = get_params_function
		self.try_params = try_params_function
		
		self.max_resource = 5	# maximum tree size for each config
		self.eta = 5			# defines configuration downsampling rate (default = 3)

		self.logeta = lambda x: log( x ) / log( self.eta )
		self.s_max = int( self.logeta( self.max_resource ))
		self.B = ( self.s_max + 1 ) * self.max_resource

		self.results = []	# list of dicts
		self.counter = 0
		self.best_loss = np.inf
		self.best_counter = -1
		#keeps track of the best counter index for a given time
		self.best_by_time = []

	# can be called multiple times
	def run( self, skip_last = 0, dry_run = False ):
		hb_start_time  = time() 
		
		for s in reversed( range( self.s_max + 1 )):
			
			# initial number of configurations
			n = int( ceil( self.B / self.max_resource / ( s + 1 ) * self.eta ** s ))	
			
			# initial number of iterations per config
			#r is the minimum resource given to each inner loop of successivehalving
			r = self.max_resource * self.eta ** ( -s )		

			# n random configurations
			T = [ self.get_params() for i in range( n )] 
			
			for i in range(( s + 1 ) - skip_last):
				
				# Run each of the n configs for <resource> 
				# and keep best (n_configs / eta) configurations
				
				n_configs = n * self.eta ** ( -i )
				n_resource = int(round(r * self.eta ** ( i )))
				print("\n*** {} configurations x {} resource each".format( 
					n_configs, n_resource))
				
				val_losses = []
				early_stops = []
				
				for t in T:
					self.counter += 1
					print("\n{} | {} | lowest loss so far: {:.4f} (run {})\n".format( 
						self.counter, ctime(), self.best_loss, self.best_counter ))
					
					start_time = time()
					
					if dry_run:
						result = { 'loss': random(), 'log_loss': random(), 'auc': random()}
					else:
						result = self.try_params( n_resource, t )		# <---
					time_since_start =  time() - hb_start_time 
					result['time'] = ctime()
						
					assert( type( result ) == dict )
					assert( 'loss' in result )
					
					seconds = int( round( time() - start_time ))
					print("\n{} seconds runtime.".format( seconds ))
					
					loss = result['loss']	
					val_losses.append( loss )
					
					early_stop = result.get( 'early_stop', False )
					early_stops.append( early_stop )
					
					# keeping track of the best result so far (for display only)
					# could do it be checking results each time, but hey
					if loss < self.best_loss:
						self.best_loss = loss
						self.best_counter = self.counter
					
					#params = t.copy()
					#del params['limits/time']
					#del params['limits/nodes']
					result['counter'] = self.counter
					result['time_since_start'] = time_since_start
					result['runtime'] = seconds
					result['resource'] = n_resource
					result['params'] = t
					self.results.append( result )
					
					with open('int_results.pkl', 'wb') as f:
						pickle.dump(self.results, f)
					
					self.best_by_time.append({time_since_start: self.best_counter})
					with open('best_index.pkl', 'wb') as f:
						pickle.dump(self.best_by_time, f)
    
				
				# select a number of best configurations for the next loop
				# filter out early stops, if any
				indices = np.argsort( val_losses )
				T = [ T[i] for i in indices if not early_stops[i]]
				T = T[ 0:int( n_configs / self.eta )]
					
		return self.results
	
