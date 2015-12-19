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

def traing_ein(label):	
	training_y, training_x = read_file('features.train', label)
	prob  = svm_problem(training_y, training_x)
	param = svm_parameter('-t 1 -g 1 -r 1 -d 2 -c 0.01')
	model = svm_train(prob, param)
	svs = model.get_SV()
	coef = model.get_sv_coef()

	w1 = 0.0
	w2 = 0.0
	sum_alpha = 0.0
	for i in range(0, len(svs)):
		w1 += svs[i][1] * coef[i][0]
		w2 += svs[i][2] * coef[i][0]
		sum_alpha += abs(coef[i][0])

	w_2f = sqrt(pow(w1,2) + pow(w2,2))
	print "sum_alpha:", sum_alpha
	# print w_2f
	p_label, p_acc, p_val = svm_predict(training_y, training_x, model)
	sum_e_in = 0
	for i in range(0, len(p_label)):
		if p_label[i] != training_y[i]:
			sum_e_in += 1

	print float(sum_e_in) / len(training_y)	
	



if __name__ == '__main__':
	labels = [0, 2, 4, 6, 8]
	for label in labels:
		traing_ein(label)	