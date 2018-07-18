% read image
im = imread('image.jpg');
% convert to grayscale
img = rgb2gray(im);

% instead of applying two filters, we can apply one 
% by sqrt(sigma_x^2 + sigma_y^2)
sigma = sqrt(1.^2 + 10.^2);
h = fspecial('gaussian', [10,10], sigma);
out = imfilter(img, h, 'conv');
imshow(out);