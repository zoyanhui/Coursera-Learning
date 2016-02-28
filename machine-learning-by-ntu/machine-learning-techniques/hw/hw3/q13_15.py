# -*- coding: utf-8 -*-
from random import randint
import json

# Implement the simple C&RT algorithm without pruning using the Gini index 
# as the impurity measure as introduced in the class. 
# For the decision stump used in branching, 
# if you are branching with feature i and direction s, 
# please sort all the xn,i values to form (at most) N+1 segments of equivalent θ, 
# and then pick θ within the median of the segment. 
# Run the algorithm on the following set for training:
# hw3_train.dat
# and the following set for testing:
# hw3_test.dat
# How many internal nodes (branching functions) are there in the resulting tree G?

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
	dt_left = None
	numleft = 0
	if impurity_left != 0:
		dt_left = CART_DT(mxy_left, d)
		numleft = dt_left.get_internum()
	elif len(mxy_left) > 0:	
		dt_left = mxy_left[0][1]		
	dt_right = None
	numRight = 0
	if impurity_right != 0:
		dt_right = CART_DT(mxy_right, d)
		numRight = dt_right.get_internum()
	elif len(mxy_right) > 0:
		dt_right = mxy_right[0][1]

	dt_g = DT_NODE()
	dt_g.setSubGc((dt_left, dt_right))
	dt_g.setBc(bc)
	dt_g.set_internum(numRight + numleft + 1)
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


C = 2
K = [-1, 1]
d = 2


if __name__ == '__main__':
	training_y, training_x = read_file('./hw3_train.dat')
	testing_y, testing_x = read_file('./hw3_test.dat')
	mxy = merge_data(training_x, training_y)
	DT_G = CART_DT(mxy, d)
	# Q13
	print "Q13, internal nodes:", DT_G.get_internum()
	print "Q14, Ein:", predict_err(DT_G, training_x, training_y)
	print "Q15, Eout:", predict_err(DT_G, testing_x, testing_y)

	

