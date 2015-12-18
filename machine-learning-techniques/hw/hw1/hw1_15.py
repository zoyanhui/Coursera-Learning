import sys
sys.path.append('../libsvm-3.20/python')
from lib.svmutil import *
from math import sqrt

def read_file(filename):
	Y = []
	X = []
	with open(filename) as f:
		for line in f.readlines():
			line_nums = [float(x) for x in line.split()]
			Y.append(1 if int(line_nums[0]) == 0 else -1)
			idx = 1
			each_x = {}
			for num in line_nums[1:]:
				each_x[idx] = num
				idx += 1
			X.append(each_x)
	return Y, X


if __name__ == '__main__':
	training_y, training_x = read_file('features.train')
	testing_y, testing_x = read_file('features.test')
	# 	options:
		# -s svm_type : set type of SVM (default 0)
		# 	0 -- C-SVC
		# 	1 -- nu-SVC
		# 	2 -- one-class SVM
		# 	3 -- epsilon-SVR
		# 	4 -- nu-SVR
		# -t kernel_type : set type of kernel function (default 2)
		# 	0 -- linear: u'*v
		# 	1 -- polynomial: (gamma*u'*v + coef0)^degree
		# 	2 -- radial basis function: exp(-gamma*|u-v|^2)
		# 	3 -- sigmoid: tanh(gamma*u'*v + coef0)
		# -d degree : set degree in kernel function (default 3)
		# -g gamma : set gamma in kernel function (default 1/num_features)
		# -r coef0 : set coef0 in kernel function (default 0)
		# -c cost : set the parameter C of C-SVC, epsilon-SVR, and nu-SVR (default 1)
		# -n nu : set the parameter nu of nu-SVC, one-class SVM, and nu-SVR (default 0.5)
		# -p epsilon : set the epsilon in loss function of epsilon-SVR (default 0.1)
		# -m cachesize : set cache memory size in MB (default 100)
		# -e epsilon : set tolerance of termination criterion (default 0.001)
		# -h shrinking: whether to use the shrinking heuristics, 0 or 1 (default 1)
		# -b probability_estimates: whether to train a SVC or SVR model for probability estimates, 0 or 1 (default 0)
		# -wi weight: set the parameter C of class i to weight*C, for C-SVC (default 1)
	prob  = svm_problem(training_y, training_x)
	param = svm_parameter('-t 0 -c 0.01')
	model = svm_train(prob, param)
	svs = model.get_SV()
	coef = model.get_sv_coef()

	w1 = 0
	w2 = 0
	for i in range(0, len(svs)):
		w1 += svs[i][1] * coef[i][0]
		w2 += svs[i][2] * coef[i][0]

	w_2f = sqrt(pow(w1,2) + pow(w2,2))
	print w_2f
	p_label, p_acc, p_val = svm_predict(training_y, training_x, model)
	print p_acc
	


