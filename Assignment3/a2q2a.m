% SIFT features for reference.png, test.png and test2.png
function out = a2q2a()
% read images and grayscale
im = imread('reference.png');
img = single(rgb2gray(im));

% get frames and descriptors for images
[f, d] = vl_sift(img);

% Plot images
imshow(im);
hold on;
sfRef = plotsiftframe(f(:,1:100));
set(sfRef,'color','r','linewidth',1);
hold off;

end