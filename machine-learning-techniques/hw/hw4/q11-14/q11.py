from base import read_file, doTrain, predict
from time import clock
import numpy as np

_g_exp_times = 500
_g_T=50000
_g_hidden_node_nums = [1,6,11,16,21] # M
_g_w_value_range = 0.1 # [-r, r]
_g_eta = 0.1

def do_single(M):
	global training_x, training_y, testing_x, testing_y
	wl1, wl2 = doTrain(M, _g_eta, _g_w_value_range, _g_T, training_x.copy(), training_y.copy())
	eout = predict(wl1, wl2, testing_x.copy(), testing_y.copy())
	return M, eout

def do_by_multiprocessing():
	from multiprocessing import Pool, cpu_count
	start = clock()
	pool = Pool(cpu_count())
	repeat_M_array = np.repeat(_g_hidden_node_nums, _g_exp_times)
	res = pool.map(do_single, repeat_M_array)
	pool.close()
	pool.join()
	eout_map = {}
	for M,eout in res:
		if eout_map.get(M) == None:
			eout_map[M] = 0
		eout_map[M] += eout
	min_eout = None
	min_eout_M = None
	for M, eout in eout_map.items():
		if min_eout == None or min_eout > eout:
			min_eout = eout
			min_eout_M = M
	print "min eout,", min_eout / _g_exp_times, ", min_eout_M:", min_eout_M
	end = clock()
	print "run by multiprocessing:", str(end - start)

if __name__ == '__main__':
	training_x, training_y = read_file('./hw4_nnet_train.dat')
	testing_x, testing_y = read_file('./hw4_nnet_test.dat')
	do_by_multiprocessing()

	# eout_map = {}
	# exp_time = 0
	# while exp_time < _g_exp_times:
	# 	exp_time += 1
	# 	print "exp_time:", exp_time
	# 	for M in _g_hidden_node_nums:
	# 		wl1, wl2 = doTrain(M, _g_eta, _g_w_value_range, _g_T, training_x.copy(), training_y.copy())
	# 		eout = predict(wl1, wl2, testing_x.copy(), testing_y.copy())
	# 		if eout_map.get(M) == None:
	# 			eout_map[M] = 0
	# 		eout_map[M] += eout
	# min_eout = None
	# min_eout_m = None
	# for M, eout in eout_map.items():
	# 	if min_eout == None or min_eout > eout:
	# 		min_eout = eout
	# 		min_eout_m = M
	# print min_eout_m

