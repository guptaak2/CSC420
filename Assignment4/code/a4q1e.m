% % plot the detection's bounding box
% figure('position', [300,100,size(im,2),size(im,1)]);
% subplot('position',[0,0,1,1]);
% imshow(G_im, []);
% imshow(im_input);
% axis off;
% axis equal;
% rectangle('position', [x,y,size(template,2),size(template,1)], 'edgecolor', [0.1,0.2,1], 'linewidth', 3.5);

BW = imread('004945.jpg');
imshow(BW);
rectangle('position', [mat.dets{1}(1), mat.dets{1}(2), mat.dets{1}(3), mat.dets{1}(4)], 'Edgecolor', 'r', 'linewidth', 3.5);