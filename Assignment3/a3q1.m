im = imread('data/door.jpg');

imshow(im);
disp('click on the four corners of the luggage. Double click the last point');
[x,y] = getpts();
close all;
imshow(im);

x2 = [1, 175, 175, 1]';
y2 = [1, 1, 280, 280]';

% compute homography
tform = maketform('projective',[x,y],[x2,y2]);
[imrec] = imtransform(im, tform, 'bicubic','XYScale',1);

% get height and width
imshow(imrec);
disp('Click on the length of the door. Double click the second point');
[x_height, y_height] = getpts();
disp('Click on the width of the door. Double click the second point');
[x_width, y_width] = getpts();

height = sqrt((x_height(1) - x_height(2))^2 + (y_height(1) - y_height(2))^2)/100;
width = sqrt((x_width(1) - x_width(2))^2 + (y_width(1) - y_width(2))^2)/100;

disp (height);
disp (width);