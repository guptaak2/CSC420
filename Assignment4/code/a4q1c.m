K =  [[721.5377,    0, 609.5593],
      [  0,  721.5377, 172.8540],
      [  0,    0,  1.0000]];
  

baseline = 0.5327;
img = imread('data/test/left/004945.jpg');
disp = imread('data/test/results/004945_left_disparity.png');
disparity = double(disp)/256;


Z = (721.5377*baseline)./(disparity);

i = 1;
for r = 1:size(Z, 1)
    for c = 1:size(Z, 2)
        xyz(i, :) = (K \ [c-1 ; r-1; 1])' * Z(r,c);
        i = i + 1;
    end
end

X = xyz(:,1);
Y = xyz(:,2);
Z = xyz(:,3);

a = load('004945_dets.mat')

surf(xyz, img, 'FaceColor', 'texturemap', 'EdgeColor', 'none')
view(0, 1000)