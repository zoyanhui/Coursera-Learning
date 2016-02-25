import numpy as np
from base import read_file, get_slice_compare_matrix, nearest_neighbor_network

if __name__ == '__main__':
	training_x, training_y = read_file('./hw4_knn_train.dat')
	testing_x, testing_y = read_file('./hw4_knn_test.dat')
	ein = nearest_neighbor_network(training_x, training_y, training_x, training_y)
	print "Q15, ein:",  ein
	eout = nearest_neighbor_network(testing_x, testing_y, training_x, training_y)
	print "Q16, eout:", eout
