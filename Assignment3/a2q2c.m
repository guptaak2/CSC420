% affine transformation
function out = a2q2c()
% get top 3 correspondences from a2q2b;
top_3 = a2q2b();

f_ref = top_3('f_ref');
f_test = top_3('f_test');

% keypoints
ref_indices = top_3('ref_indices');
test_indices = top_3('test_indices');

% point matrices
ref_points = [f_ref(1:2, ref_indices(1):ref_indices(1)), f_ref(1:2, ref_indices(2):ref_indices(2)), f_ref(1:2, ref_indices(3):ref_indices(3))];
test_points = [f_test(1:2, test_indices(1):test_indices(1)), f_test(1:2, test_indices(2):test_indices(2)), f_test(1:2, test_indices(3):test_indices(3))];

% since we have 3 keypoints, we use a = inv(P) * P'
P = [];
for i = 1:3
    r1 = [ref_points(1, i), ref_points(2, i), 0, 0, 1, 0];
    r2 = [0, 0, ref_points(1, i), ref_points(2, i), 0, 1];
    P = [P; r1; r2];
end

P_prime = [test_points(1,1); test_points(2,1); test_points(1,2); test_points(2,2); test_points(1,3); test_points(2,3)];

out = inv(P + eye(6)*1e-8)*P_prime;
end