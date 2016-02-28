from base import read_file, doTrain, predict
from time import clock
import numpy as np

_g_exp_times = 500
_g_T=50000
_g_w_value_range = [0, 0.1, 10, 100, 1000] # [-r, r]
_g_eta = 0.1
_g_M = 3

training_x = None
training_y = None
testing_x = None
testing_y = None

def do_single(r):
	global training_x, training_y, testing_x, testing_y
	wl1, wl2 = doTrain(_g_M, _g_eta, r, _g_T, training_x.copy(), training_y.copy())
	eout = predict(wl1, wl2, testing_x.copy(), testing_y.copy())
	print "r:", r, ", eout:", eout
	return r, eout

def do_by_multiprocessing():
	from multiprocessing import Pool, cpu_count
	start = clock()
	pool = Pool(cpu_count())
	repeat_r_array = np.repeat(_g_w_value_range, _g_exp_times)
	res = pool.map(do_single, repeat_r_array)
	print res
	pool.close()
	pool.join()
	eout_map = {}
	for r,eout in res:
		if eout_map.get(r) == None:
			eout_map[r] = 0
		eout_map[r] += eout
	min_eout = None
	min_eout_r = None
	for r, eout in eout_map.items():
		if min_eout == None or min_eout > eout:
			min_eout = eout
			min_eout_r = r
	print "min eout,", min_eout , ", min_eout_r:", min_eout_r
	end = clock()
	print "run by multiprocessing:", str(end - start)

if __name__ == '__main__':
	training_x, training_y = read_file('./hw4_nnet_train.dat')
	testing_x, testing_y = read_file('./hw4_nnet_test.dat')
	do_by_multiprocessing()

