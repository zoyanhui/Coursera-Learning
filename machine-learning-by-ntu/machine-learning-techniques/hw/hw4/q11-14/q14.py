from time import clock
import numpy as np

def read_file(filename):
	Y = []
	X = []	
	with open(filename) as f:
		for line in f.readlines():
			line_nums = [float(x) for x in line.split()]
			Y.append(int(line_nums[2]))
			X.append(line_nums[0])
			X.append(line_nums[1])
	Y = np.array(Y)
	X = np.array(X).reshape(-1, 2)
	return X, Y


def init_w(n, m, r):
	s = np.random.uniform(-r, r, n * m)
	return s.reshape(n, m)


def doTrain(eta, r, T, X, Y):
	print "training, eta:", eta, ", r:", r
	N = Y.shape[0]
	wLayer1 = init_w(3, 8, r)
	wLayer2 = init_w(8+1, 3, r)
	wLayer3 = init_w(3+1, 1, r)
	t = 0
	while t < T:
		t += 1
		# randomly pick n
		n = np.random.randint(0, N)
		yn = Y[n]
		xlayer0 = np.hstack((1, X[n]))
		xlayer0.shape = 1, xlayer0.shape[0]		
		# compute all xlayer
		slayer1 = xlayer0.dot(wLayer1)
		xlayer1 = np.tanh(slayer1)		
		xlayer1 = np.column_stack((np.ones(xlayer1.shape[0]).transpose(), xlayer1))
		slayer2 = xlayer1.dot(wLayer2)
		xlayer2 = np.tanh(slayer2)
		xlayer2 = np.column_stack((np.ones(xlayer2.shape[0]).transpose(), xlayer2))
		slayer3 = xlayer2.dot(wLayer3)
		xlayer3 = np.tanh(slayer3)
		# compute all delta

		delta3 = -2 * (yn - xlayer3) * (1 - np.tanh(slayer3) ** 2)
		delta2 = delta3.dot(wLayer3[1:,:].transpose()) * (1 - np.tanh(slayer2) ** 2)
		delta1 = delta2.dot(wLayer2[1:,:].transpose()) * (1 - np.tanh(slayer1) ** 2)
		# gradient descent
		lamb = 0
		wLayer3 -= eta * (xlayer2.transpose().dot(delta3) + lamb * wLayer3)
		wLayer2 -= eta * (xlayer1.transpose().dot(delta2) + lamb * wLayer2)
		wLayer1 -= eta * (xlayer0.transpose().dot(delta1) + lamb * wLayer1)
	return wLayer1, wLayer2, wLayer3


def sign(x):
	if x >= 0:
		return 1
	else:
		return -1

sign = np.vectorize(sign)



def predict(wl1, wl2, wl3, X, Y):
	X = np.column_stack((np.ones(X.shape[0]).transpose(), X))
	Xl1 = np.tanh(X.dot(wl1))
	Xl1 = np.column_stack((np.ones(Xl1.shape[0]).transpose(), Xl1))
	Xl2 = np.tanh(Xl1.dot(wl2))
	Xl2 = np.column_stack((np.ones(Xl2.shape[0]).transpose(), Xl2))
	Xl3 = np.tanh(Xl2.dot(wl3))	
	# using square error can not get a selectable option
	square_err = np.sum((Xl3 - Y.reshape(Xl3.shape)) ** 2) / Y.shape[0]
	# using 0/1 error, which according to the options of Q14
	Xl3 = sign(Xl3)
	zero_one_err = (np.sum(Xl3 != Y.reshape(Xl3.shape)) + 0.0) / Y.shape[0]
	return square_err, zero_one_err


_g_exp_times = 500
_g_T=50000
_g_w_value_range = 0.1 # [-r, r]
_g_eta = 0.01

training_x = None
training_y = None
testing_x = None
testing_y = None

def do_single(fake):
	global training_x, training_y, testing_x, testing_y
	wl1, wl2, wl3 = doTrain(_g_eta, _g_w_value_range, _g_T, training_x.copy(), training_y.copy())
	seout, zeout = predict(wl1, wl2, wl3, testing_x.copy(), testing_y.copy())
	sein, zein = predict(wl1, wl2, wl3, training_x.copy(), training_y.copy())
	# print "ein:", sein, zein
	# print "eout:", seout, zeout
	return seout, zeout

def do_by_multiprocessing():
	from multiprocessing import Pool, cpu_count
	start = clock()
	pool = Pool(cpu_count())	
	res = pool.map(do_single, range(_g_exp_times))
	pool.close()
	pool.join()
	square_eouts = []
	zero_one_eouts = []
	for sout, zeout in res:	
		square_eouts.append(sout)
		zero_one_eouts.append(zeout)	
	end = clock()
	print "run by multiprocessing:", str(end - start)
	return square_eouts, zero_one_eouts

if __name__ == '__main__':
	training_x, training_y = read_file('./hw4_nnet_train.dat')
	testing_x, testing_y = read_file('./hw4_nnet_test.dat')
	seouts, zeouts = do_by_multiprocessing()
	# not get any answer of the options
	print "Q14, square eout:[", min(seouts),",", max(seouts),"]", ", mean error:", np.mean(seouts)
	print "Q14, zero one eout:[", min(zeouts),",", max(zeouts),"]", ", mean error:", np.mean(zeouts)


