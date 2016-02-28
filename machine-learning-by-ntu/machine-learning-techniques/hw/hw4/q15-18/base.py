import numpy as np

def read_file(filename):
	Y = []
	X = []
	with open(filename) as f:
		for line in f.readlines():
			line_nums = [float(x) for x in line.split()]
			Y.append(int(line_nums[-1]))
			X+=line_nums[:-1]
	Y = np.array(Y)
	Y.shape = Y.shape[0],1
	X = np.array(X).reshape(Y.shape[0], -1)
	return X, Y

def get_slice_compare_matrix(n ,N):
	if n == 0:
		return np.arange(1, N)
	elif n == N -1:
		return np.arange(0, N-1)
	elif n <0 or n >= N:
		return np.arange(0, N)
	else:
		sliced = np.arange(0, n)
		return np.r_[sliced, np.arange(n+1, N)]

def fix_idx(idx_array, n):
	def fix_idx_inner(idx):
		if idx >= n:
			idx += 1
		return idx

	fix_idx_inner = np.vectorize(fix_idx_inner)
	return fix_idx_inner(idx_array)


def calc_distance(X, CX, knn = 1):
	N = X.shape[0]
	nearest_neighbors = []
	for n in range(N):
		x = X[n]
		# sliced = get_slice_compare_matrix(n, N)
		# X_noN = x - X[sliced]	
		X_noN = x - CX
		distance_matrix = np.sum(X_noN ** 2, 1)	
		idx_order = np.argsort(distance_matrix)
		idx_order = idx_order[0:knn]
		# print n, idx_order
		# idx_order = fix_idx(idx_order, n)
		nearest_neighbors.append(idx_order)		
	return np.array(nearest_neighbors)#.reshape((N, -1))


def nearest_neighbor_network(X, Y, CX, CY, knn =1):
	nearest_neighbors = calc_distance(X, CX, knn)	
	CY = np.ndarray.flatten(CY)
	nn_array = CY[nearest_neighbors]
	nn_array = np.sum(nn_array, 1)
	nn_array = np.sign(nn_array)
	err = np.sum(nn_array != Y.reshape(nn_array.shape))
	# print err
	return (np.sum(err) + 0.0) / Y.shape[0]


