import sys
sys.path.append('../libsvm-3.20/python')
from lib.svmutil import *
from math import sqrt
import random

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

def traing_with_gamma():	
	training_y, training_x = read_file('features.train', 0)
	# testing_y, testing_x = read_file('features.test', 0)
	all_idx = range(0, len(training_x))
	val_idx = random.sample(all_idx, 1000)
	dict_val_idx = set(val_idx)
	train_idx = [i for i in all_idx if i not in dict_val_idx]
	validation_y = [training_y[i] for i in val_idx]
	validation_x = [training_x[i] for i in val_idx]

	new_training_y = [training_y[i] for i in train_idx]
	new_training_x = [training_x[i] for i in train_idx]


	prob  = svm_problem(new_training_y, new_training_x)
	best_gamma = None
	best_eval = None
	gamma = [1,10,100,1000,10000]
	for g in gamma:
		eval_each = do_modeling(prob, g, new_training_y, new_training_x, validation_y, validation_x)
		if best_eval == None:		
			best_eval = eval_each
			best_gamma = g
		elif eval_each < best_eval:
			best_eval = eval_each
			best_gamma = g
		# elif eval_each == best_eval and g < best_gamma: 
		# 	best_eval = eval_each
		# 	best_gamma = g
	return best_gamma

def do_modeling(prob, g, training_y, training_x, testing_y, testing_x):
	print "#################-----------#######"
	param_str = '-t 2 -c 0.1 -g ' + str(g)
	param = svm_parameter(param_str)
	print "param:", param_str
	model = svm_train(prob, param)
	# svs = model.get_SV()
	# coef = model.get_sv_coef()
	# print "number of support vectors:", str(len(svs))
	# w1 = 0.0
	# w2 = 0.0
	# sum_alpha = 0.0
	# for i in range(0, len(svs)):
	# 	w1 += svs[i][1] * coef[i][0]
	# 	w2 += svs[i][2] * coef[i][0]
	# 	sum_alpha += abs(coef[i][0])

	# w_2f = sqrt(pow(w1,2) + pow(w2,2))
	# print "w_2f:", w_2f
	# print "sum_alpha:", sum_alpha
	# # print w_2f
	# p_label, p_acc, p_val = svm_predict(training_y, training_x, model)
	# sum_e_in = 0
	# for i in range(0, len(p_label)):
	# 	if p_label[i] != training_y[i]:
	# 		sum_e_in += 1

	# print "ein:", str(float(sum_e_in) / len(training_y))
	p_label, p_acc, p_val = svm_predict(testing_y, testing_x, model)
	sum_e_out = 0
	for i in range(0, len(p_label)):
		if p_label[i] != testing_y[i]:
			sum_e_out += 1
	# eout = str(float(sum_e_out) / len(testing_y))
	print "eout:", sum_e_out
	return sum_e_out




if __name__ == '__main__':
	try_times = 100
	best_gamma_times = {}
	for i in range(0, try_times):
		gamma = traing_with_gamma()
		if best_gamma_times.get(gamma) == None:
			best_gamma_times[gamma] = 1
		else:
			best_gamma_times[gamma] += 1
	print best_gamma_times
	