# -*- coding: utf-8 -*-
from random import randint
import json

# Now, `prune' your decision tree algorithm by restricting it to have one branch only. 
# That is, the tree is simply a decision stump determined by Gini index. 
# Make a random `forest' GRS with those decision stumps with Bagging like Questions 16-18 with T=300. 
# Repeat the experiment for 100 times and compute average Ein and Eout using the 0/1 error.

def read_file(filename):
	Y = []
	X = []
	with open(filename) as f:
		for line in f.readlines():
			line_nums = [float(x) for x in line.split()]
			Y.append(int(line_nums[2]))			
			X.append([line_nums[0], line_nums[1]])
	return Y, X


def gini_index(merged_xy):
	N = len(merged_xy)
	s = 0.0
	if N ==0:
		return s
	uk = {}
	for i in range(len(K)):
		uk[K[i]] = 0
	for xn, yn in merged_xy:
		uk[yn] += 1
	for k, num in uk.items():
		s += pow((num + 0.0) / N, 2)
	return 1-s

def merge_data(x_list, y_list):
	mdata = []
	for i in range(len(x_list)):
		mdata.append((x_list[i], y_list[i]))
	return mdata

def calc_pick_theta(mxy, feature_i, ds_index):
	if ds_index == 0:
		return mxy[0][0][feature_i] - 1
	if ds_index == len(mxy):
		return mxy[ds_index - 1][0][feature_i] + 1
	return (mxy[ds_index - 1][0][feature_i] + mxy[ds_index][0][feature_i]) / 2.0

def branching(mxy, feature_i):		
	sort_sample(mxy, feature_i)
	# calculate weighted impurity for each decision stump
	min_branch_score = None
	branch_index = None
	impurity_left = None
	impurity_right = None
	theta = None
	for i in range(len(mxy) + 1):
		_theta = calc_pick_theta(mxy, feature_i, i)
		impurity_l = gini_index(mxy[0:i])
		impurity_r = gini_index(mxy[i:])
		branch_score = impurity_l * i + impurity_r * (len(mxy) - i)
		if min_branch_score == None or min_branch_score > branch_score:
			min_branch_score = branch_score
			branch_index = i
			impurity_left = impurity_l
			impurity_right = impurity_r
			theta = _theta
	return mxy[0:branch_index], mxy[branch_index:], theta, impurity_left, impurity_right, min_branch_score


def sort_sample(mxy, feature_i):
	if feature_i == 0:
		mxy.sort()
	else:		
		for x, y in mxy:			
			temp = x[0]
			x[0] = x[feature_i]
			x[feature_i] = temp
		mxy.sort()
		for x, y in mxy:
			temp = x[0]
			x[0] = x[feature_i]
			x[feature_i] = temp	

class DT_NODE(object):
	"""docstring for DT_NODE"""
	def __init__(self):
		# sub decision tree
		self.sub_gc = None
		# branching criteria
		self.bc = None
		self.inert_node_num = 0

	def setBc(self, bc):
		self.bc = bc

	def getBc(self):
		return self.bc

	def setSubGc(self, gcs):
		self.sub_gc = tuple(gcs)

	def getSubGc(self):
		return self.sub_gc

	def set_internum(self, num):
		self.inert_node_num = num

	def get_internum(self):
		return self.inert_node_num

	def __str__(self):
		return "{ 'bc': " + json.dumps(self.bc) + ", 'sub': ["+ str(self.sub_gc[0])+ ", "+ str(self.sub_gc[1]) + "]}"

	def __repr__(self):
		return "{ 'bc': " + json.dumps(self.bc) + ", 'sub': ["+ str(self.sub_gc[0])+ ", "+ str(self.sub_gc[1]) + "]}"

def CART_DT(mxy, d):
	# if termination return base g
	# else
	# split D to C parts with minimum impurity
	min_branch_score = None
	mxy_left = None
	mxy_right = None 
	theta = None 
	impurity_left = None 
	impurity_right = None
	feature = None
	for _feature_i in range(d):
		# learning branching criteria b(x)
		_mxy_left, _mxy_right, _theta, _impurity_left, _impurity_right, branch_score = branching(mxy, _feature_i)
		if min_branch_score == None or branch_score < min_branch_score:
			mxy_left = _mxy_left
			mxy_right = _mxy_right
			theta = _theta
			impurity_left = _impurity_left
			impurity_right = _impurity_right
			min_branch_score = branch_score	
			feature = _feature_i
	bc = {"theta": theta, "s": 1, "feature": feature}	
	
	# dt_g = DT_NODE()	
	# dt_g.setBc(bc)	
	# sum_left = 0
	# for x,y in mxy_left:
	# 	sum_left += y
	# sum_right = 0
	# for x,y in mxy_right:
	# 	sum_right += y

	# if sum_left >=0:
	# 	if sum_right<0:
	# 		dt_g.setSubGc((1, -1))
	# 	else:
	# 		if sum_left > sum_right:
	# 			dt_g.setSubGc((1, -1))
	# 		else:
	# 			dt_g.setSubGc((-1, 1))
	# else:
	# 	if sum_right>=0:
	# 		dt_g.setSubGc((-1, 1))
	# 	else:
	# 		if sum_left > sum_right:
	# 			dt_g.setSubGc((1, -1))
	# 		else:
	# 			dt_g.setSubGc((-1, 1))




	dt_left = None
	if impurity_left != 0:
		sum_y = 0
		for x,y in mxy_left:
			sum_y += y
		dt_left = 1 if sum_y >=0 else -1
		# dt_left = CART_DT(mxy_left, d)
	elif len(mxy_left) > 0:	
		dt_left = mxy_left[0][1]		
	dt_right = None
	if impurity_right != 0:		
		sum_y = 0
		for x,y in mxy_right:			
			sum_y += y
		dt_right = 1 if sum_y >=0 else -1
		# dt_right = CART_DT(mxy_right, d)
	elif len(mxy_right) > 0:
		dt_right = mxy_right[0][1]

	dt_g = DT_NODE()
	dt_g.setSubGc((dt_left, dt_right))
	dt_g.setBc(bc)
	return dt_g

def sign(x):
	if x >= 0:
		return 1
	else:
		return -1

def cal_dc_branch(bx, x):
	return bx["s"] * sign(x[bx["feature"]] - bx["theta"])	
	
def do_predict(DT_G, x):
	tree_node = DT_G
	while tree_node != None:		
		if type(tree_node) is not DT_NODE:
			return tree_node
		bx = tree_node.getBc()
		c = cal_dc_branch(bx, x)
		# print c
		if c < 0:
			tree_node = tree_node.getSubGc()[0]
		else:
			tree_node = tree_node.getSubGc()[1]
	raise Error("null predict")


def predict_err(DT_G, data_x, data_y):
	mxy = merge_data(data_x, data_y)
	err = 0
	for x, y in mxy:
		y_bar = do_predict(DT_G, x)
		if y_bar != y:
			err += 1
	return (err + 0.0) / len(data_y)

def predict_err_mxy(DT_G, mxy):
	err = 0
	for x, y in mxy:
		y_bar = do_predict(DT_G, x)
		if y_bar != y:
			err += 1
	return (err + 0.0) / len(mxy)

def do_predict_grf(GRF, x):
	y_bar_sum = 0
	for gt in GRF:
		y_bar = do_predict(gt, x)
		y_bar_sum += y_bar
	return 1 if y_bar_sum >=0 else -1

def predict_err_grf(GRF, mxy):	
	err = 0
	for x, y in mxy:
		y_bar = do_predict_grf(GRF, x)
		if y_bar != y:
			err += 1
	return (err + 0.0) / len(mxy)


def bagging_sample(mxy):
	N = len(mxy)
	sampled = []
	for i in range(N):
		idx = randint(0, N-1)
		sampled.append(mxy[idx])
	return sampled


C = 2
K = [-1, 1]
d = 2
T = 300
repeat_times = 100


if __name__ == '__main__':
	training_y, training_x = read_file('./hw3_train.dat')
	testing_y, testing_x = read_file('./hw3_test.dat')
	mxy = merge_data(training_x, training_y)
	mxy_test = merge_data(testing_x, testing_y)
	
	ein_grf_list = []
	eout_grf_list = []
	for r_time in range(repeat_times):
		print "repeat", r_time + 1
		GtRF = []
		t = 0
		while t < T:
			t += 1
			sample_mxy = bagging_sample(mxy)
			gt = CART_DT(sample_mxy, d)
			GtRF.append(gt)
		print GtRF
		ein_grf = predict_err_grf(GtRF, mxy)
		ein_grf_list.append(ein_grf)
		eout_grf_list.append(predict_err_grf(GtRF, mxy_test))

	# Q19 have problem, not right
	print "Q19, ave Grf ein", sum(ein_grf_list) / len(ein_grf_list)
	# Q20
	print "Q20, ave Grf eout", sum(eout_grf_list) / len(eout_grf_list)
	

