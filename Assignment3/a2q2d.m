% Visualize affine
function out = a2q2d()
% read image
im_ref = imread('reference.png');
im_test = imread('test2.png');
[imrows, imcols, ~] = size(im_ref);

% Matrix P 
P = [1, 1, 0, 0, 1, 0; 0, 0, 1, 1, 0, 1;
1, imrows, 0, 0, 1, 0; 0, 0, 1, imrows, 0, 1;
imcols, 1, 0, 0, 1, 0; 0, 0, imcols, 1, 0, 1;
imcols, imrows, 0, 0, 1, 0; 0, 0, imcols, imrows, 0, 1;]

% affine transformation
transformed = a2q2c();
a = P*transformed;

% Plot corners of shrek 2
figure;
imshow(im_test);
hold on;
line([a(1), a(3)],[a(2),a(4)],'color','r', 'linewidth', 3);
line([a(1), a(5)],[a(2),a(6)],'color','r', 'linewidth', 3);
line([a(3), a(7)],[a(4),a(8)],'color','r', 'linewidth', 3);
line([a(5), a(7)],[a(6),a(8)],'color','r', 'linewidth', 3);
hold off;
end