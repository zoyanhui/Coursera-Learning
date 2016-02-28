import numpy as np

def read_file(filename):
	X = []
	with open(filename) as f:
		for line in f.readlines():
			line_nums = [float(x) for x in line.split()]
			X+=line_nums
	X = np.array(X).reshape(-1, 9)
	return X

def init_centers(X, k):
	N = X.shape[0]	
	idxs = np.random.choice(np.arange(N), k)
	return X[idxs]

# MU is centers matrix
def calc_distance(X, MU, N):	
	nearest_neighbors = []
	for n in range(N):
		x = X[n]
		mudistance = x - MU
		idx_order = np.argmin(np.sum(mudistance ** 2, 1))				
		nearest_neighbors.append(idx_order)		
	return np.array(nearest_neighbors).reshape((N, -1))

def calc_new_centers(clusters, MU, X, N):
	s_map = {}
	for n in range(N):
		c = clusters[n][0]
		if s_map.get(c) == None:
			s_map[c] = []
		s_map[c].append(X[n])
	dimension = X.shape[1]
	new_centers = []
	sum_err = 0.0
	for c, xs in s_map.items():
		# cluster c
		sc = np.array(xs)#.reshape((-1, dimension))
		sum_err += calc_err(sc, MU[c])
		new_centers.append(np.mean(sc, 0))
	return np.array(new_centers), sum_err

def calc_err(sc, mu):
	return np.sum((sc - mu) ** 2)	

def kmeans(X, N, K):
	MU = init_centers(trainX, K)	
	OLD_MU = None
	compare_mu = MU != OLD_MU
	# print compare_mu
	while (OLD_MU is None) or ((type(compare_mu) is np.ndarray) and compare_mu.any()) or ((type(compare_mu) is bool) and compare_mu):		
		OLD_MU = MU.copy()
		clusters = calc_distance(trainX, MU, N)
		MU, sum_err = calc_new_centers(clusters, MU, trainX, N)
		compare_mu = MU != OLD_MU
		# print compare_mu
	ein = sum_err / N 
	return ein

def repeat_kmeans(X, N, K):
	t = 0
	eins = []
	while t < _try_times:
		t += 1
		ein = kmeans(X, N, K)
		eins.append(ein)
	print "Ein:", np.mean(np.array(eins))

_try_times = 500

if __name__ == '__main__':	
	trainX = read_file('./hw4_kmeans_train.dat')
	N = trainX.shape[0]	
	print "Q19:"
	K = 2
	repeat_kmeans(trainX, N, K)
	print "Q20:"
	K = 10
	repeat_kmeans(trainX, N, K)



	
