from base import read_file, doTrain, predict
from time import clock
import numpy as np

_g_exp_times = 500
_g_T=50000
_g_w_value_range = 0.1 # [-r, r]
_g_eta = [0.001, 0.01, 0.1, 1, 10]
_g_M = 3

training_x = None
training_y = None
testing_x = None
testing_y = None

def do_single(eta):
	global training_x, training_y, testing_x, testing_y
	wl1, wl2 = doTrain(_g_M, eta, _g_w_value_range, _g_T, training_x.copy(), training_y.copy())
	eout = predict(wl1, wl2, testing_x.copy(), testing_y.copy())
	return eta, eout

def do_by_multiprocessing():
	from multiprocessing import Pool, cpu_count
	start = clock()
	pool = Pool(cpu_count())
	repeat_eta_array = np.repeat(_g_eta, _g_exp_times)
	res = pool.map(do_single, repeat_eta_array)
	pool.close()
	pool.join()
	eout_map = {}
	for eta,eout in res:
		if eout_map.get(eta) == None:
			eout_map[eta] = 0
		eout_map[eta] += eout
	min_eout = None
	min_eout_eta = None
	for eta, eout in eout_map.items():
		if min_eout == None or min_eout > eout:
			min_eout = eout
			min_eout_eta = eta
	print min_eout_eta
	print "min eout,", min_eout / _g_exp_times, ", min_eout_eta:", min_eout_eta
	end = clock()
	print "run by multiprocessing:", str(end - start)

if __name__ == '__main__':
	training_x, training_y = read_file('./hw4_nnet_train.dat')
	testing_x, testing_y = read_file('./hw4_nnet_test.dat')
	do_by_multiprocessing()


