import numpy as np
from base import read_file, nearest_neighbor_network




if __name__ == '__main__':
	training_x, training_y = read_file('./hw4_knn_train.dat')
	testing_x, testing_y = read_file('./hw4_knn_test.dat')
	print "Q17, ein:", nearest_neighbor_network(training_x, training_y, training_x, training_y,5)
	print "Q18, eout:", nearest_neighbor_network(testing_x, testing_y, training_x, training_y, 5)

