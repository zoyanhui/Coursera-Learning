from random import randint
from math import sqrt, log

MINUS_INFINIT = -10000

def read_file(filename):
	Y = []
	X = []
	with open(filename) as f:
		for line in f.readlines():
			line_nums = [float(x) for x in line.split()]
			Y.append(int(line_nums[2]))			
			X.append((line_nums[0], line_nums[1]))
	return Y, X


def sort_sample(X, Y, d):
	data = []
	for i in range(d):
		data_d = []
		for idx, xx in enumerate(X):
			data_d.append((xx[i], Y[idx]))
		data_d.sort()
		data.append(data_d)
	return data


def train(data_set, T, d):
	G_set = []
	N = len(data_set[0])
	u = [1.0 / N] * N
	it = 1
	while it <= T:
		# select a feature from d, indexed from 0 to d-1
		i = randint(0, d -1)
		s, theta, alpha, u = do_train(data_set[i], it, u, N)		
		# print it, (s, theta, alpha)
		G_set.append((s, i, theta, alpha))
		it += 1
	return G_set

def do_train(data, t, u, N):
	# s = 1
	err_positive_right = [0] * N
	err_negative_left = [0] * N
	# s = -1
	err_positive_left = [0] * N
	err_negative_right = [0] * N
	for m in range(N - 1):
		if data[m][1] == 1:
			err_negative_left[m + 1] = err_negative_left[m] + u[m]
			err_positive_left[m + 1] = err_positive_left[m]
		else:
			err_positive_left[m + 1] = err_positive_left[m] + u[m]
			err_negative_left[m + 1] = err_negative_left[m]

	for m in range(N-1, -1, -1):
		if data[m][1] == 1:
			if m == N - 1:
				err_negative_right[m] = u[m]
				err_positive_right[m] = 0
			else:
				err_negative_right[m] = err_negative_right[m+1] + u[m]
				err_positive_right[m] = err_positive_right[m+1]
		else:
			if m == N - 1:
				err_positive_right[m] = u[m]
				err_negative_right[m] = 0
			else:
				err_positive_right[m] = err_positive_right[m+1] + u[m]
				err_negative_right[m] = err_negative_right[m+1]	
	# when s == 1
	s = 1
	err_min = None
	err_min_idx = None
	for m in range(N):
		err = err_positive_right[m] + err_negative_left[m]
		if err_min == None or err < err_min:
			err_min = err
			err_min_idx = m

	for m in range(N):
		err = err_positive_left[m] + err_negative_right[m]
		if err_min == None or err < err_min:
			err_min = err
			err_min_idx = m	
			s = -1

	if err_min_idx == 0:
		theta = MINUS_INFINIT
	else:
		theta = (data[err_min_idx-1][0] + data[err_min_idx][0]) / 2.0

	if t == 2:
		print "Q14, U2:", sum(u)
	if t == T:
		# Q15 rerun use T >= 1000
		print "Q15, UT:", sum(u)
	# calc_next_u()
	epsilon = (err_min + 0.0) / sum(u)
	g_epsilons.append(epsilon)	
	pt = sqrt((1.0- epsilon) / epsilon)
	for m in range(N):
		if m < err_min_idx:
			if s == 1:
				if data[m][1] == 1:
					u[m] *= pt
				else:
					u[m] /= pt
			else:
				if data[m][1] == -1:
					u[m] *= pt
				else:
					u[m] /= pt
		else:
			if s == 1:
				if data[m][1] == -1:
					u[m] *= pt
				else:
					u[m] /= pt
			else:
				if data[m][1] == 1:
					u[m] *= pt
				else:
					u[m] /= pt	
	alpha = log(pt)
	return s, theta, alpha, u


def sign(x):
	if x >= 0:
		return 1
	else:
		return -1

def predict(G, XX, YY):
	N = len(XX)
	err = 0
	for m in range(N):
		y = YY[m]
		x = XX[m]
		Sg = 0.0
		for g in G:
			Sg += g[3] * g[0] * sign(x[g[1]] - g[2])
		y_p = sign(Sg)
		if y_p != y:
			err += 1
	print "E(G):", (err + 0.0) / N

def predict_g(g, XX, YY):
	N = len(XX)
	err = 0
	for m in range(N):
		y = YY[m]
		x = XX[m]
		Sg = g[3] * g[0] * sign(x[g[1]] - g[2])
		y_p = sign(Sg)
		if y_p != y:
			err += 1
	print "E(g):", (err + 0.0) / N
	# return (err + 0.0) / N

T = 300 #10000
d = 2

g_epsilons = [] 

if __name__ == '__main__':
	training_y, training_x = read_file('./hw2_adaboost_train.dat')
	testing_y, testing_x = read_file('./hw2_adaboost_test.dat')
	
	training = sort_sample(training_x, training_y, d)
	G = train(training, T, d)

	print "Q13, Ein(G):",
	predict(G, training_x, training_y)

	print "Q18, Eout(G):",
	predict(G, testing_x, testing_y)

	# Q16 find the minimum epsilon
	print "Q16 minimum epsilon:", min(g_epsilons)
	# print g_epsilons

	g1 = G[0]	

	print "Q12, Ein(g1)",
	predict_g(g1, training_x, training_y)

	print "Q17, Eout(g1)",
	predict_g(g1, testing_x, testing_y)





	
