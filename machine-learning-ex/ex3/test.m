theta = [-2; -1; 1; 2];
X = [ones(3,1) magic(3)];
y = [1; 0; 1];
lambda = 3;
[j grad] = lrCostFunction(theta, X, y, lambda)

