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


def doTrain(M, eta, r, T, X, Y):
	print "training, M:", M, ", eta:", eta, ", r:", r
	N = Y.shape[0]
	wLayer1 = init_w(3, M, r)
	wLayer2 = init_w(M+1, 1, r)
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
		# compute all delta
		delta2 = -2 * (yn - xlayer2) * (1 - np.tanh(slayer2) ** 2)
		delta1 = delta2.dot(wLayer2[1:,:].transpose()) * (1 - np.tanh(slayer1) ** 2)
		# gradient descent
		wLayer2 -= eta * xlayer1.transpose().dot(delta2)
		wLayer1 -= eta * xlayer0.transpose().dot(delta1)
	return wLayer1, wLayer2


def predict(wl1, wl2, X, Y):
	X = np.column_stack((np.ones(X.shape[0]).transpose(), X))
	Xl1 = np.tanh(X.dot(wl1))
	Xl1 = np.column_stack((np.ones(Xl1.shape[0]).transpose(), Xl1))
	Xl2 = np.tanh(Xl1.dot(wl2))
	# return np.sum((Xl2 - Y) ** 2)
	return np.sum((Xl2 - Y.reshape(Xl2.shape)) ** 2) / Y.shape[0]