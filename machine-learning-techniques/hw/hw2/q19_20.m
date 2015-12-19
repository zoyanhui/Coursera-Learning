data = load('hw2_lssvm_all.dat');
training_size = 400;
training_x = data(1:training_size, 1:10);
training_y = data(1:training_size, 11);
testing_x = data(training_size + 1:end, 1:10);
testing_y = data(training_size + 1:end, 11);

function  ret = kernel_exp(x1, x2, mgamma)
	ret = exp(-mgamma * sum((x1 - x2).^2));
endfunction

function ret = kernel_matrix(X, Xba, mgamma)
	n = size(X, 1);
	m = size(Xba, 1);
	for i = 1:n
		for j = 1:m
			ret(i,j) = kernel_exp(X(i,:), Xba(j,:), mgamma);
		end
	end
endfunction

function retval = cal_beta(K, y, lambda)
	retval = inv(lambda * eye(size(K))  +  K) * y;
endfunction

gammas = [32,2,0.125];
lambdas = [0.001,1,1000];

testing_size = size(testing_y, 1);
ein = [];
eout = [];
for mgamma = gammas
	for	lambda = lambdas
		K = kernel_matrix(training_x, training_x, mgamma);
		mbeta = cal_beta(K, training_y, lambda);
		predict_y = sign(K' * mbeta );
		ein = [ein(:); sum(predict_y != training_y) / training_size];
		

		K_test = kernel_matrix(training_x, testing_x, mgamma);
		predict_test_y = sign(K_test' * mbeta);
		eout = [eout(:); sum(predict_test_y != testing_y) / testing_size];
		
	end
end	

disp("Ein:"), disp (ein);

disp("Eout:"), disp (eout);