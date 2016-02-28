import sys
sys.path.append('../libsvm-3.20/python')
from lib.svmutil import *
from math import sqrt

def read_file(filename, label = 0):
	Y = []
	X = []
	with open(filename) as f:
		for line in f.readlines():
			line_nums = [float(x) for x in line.split()]
			Y.append(1 if int(line_nums[0]) == label else -1)
			idx = 1
			each_x = {}
			for num in line_nums[1:]:
				each_x[idx] = num
				idx += 1
			X.append(each_x)
	return Y, X

def traing_with_c():	
	training_y, training_x = read_file('features.train', 0)
	testing_y, testing_x = read_file('features.test', 0)
	prob  = svm_problem(training_y, training_x)
	C = [0.001,0.01,0.1,1,10]
	for c in C:
		do_modeling(prob, c, training_y, training_x, testing_y, testing_x)

def do_modeling(prob, c, training_y, training_x, testing_y, testing_x):
	param_str = '-t 2 -g 100 -c ' + str(c)
	param = svm_parameter(param_str)
	print "param:", param_str
	model = svm_train(prob, param)
	svs = model.get_SV()
	coef = model.get_sv_coef()
	print "number of support vectors:", str(len(svs))
	w1 = 0.0
	w2 = 0.0
	sum_alpha = 0.0
	for i in range(0, len(svs)):
		w1 += svs[i][1] * coef[i][0]
		w2 += svs[i][2] * coef[i][0]
		sum_alpha += abs(coef[i][0])

	w_2f = sqrt(pow(w1,2) + pow(w2,2))
	print "w_2f:", w_2f
	print "sum_alpha:", sum_alpha
	# print w_2f
	p_label, p_acc, p_val = svm_predict(training_y, training_x, model)
	sum_e_in = 0
	for i in range(0, len(p_label)):
		if p_label[i] != training_y[i]:
			sum_e_in += 1

	print "ein:", str(float(sum_e_in) / len(training_y))
	p_label, p_acc, p_val = svm_predict(testing_y, testing_x, model)
	sum_e_out = 0
	for i in range(0, len(p_label)):
		if p_label[i] != testing_y[i]:
			sum_e_out += 1
	print "eout:", str(float(sum_e_out) / len(testing_y))




if __name__ == '__main__':
	traing_with_c()