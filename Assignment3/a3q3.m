K =  [[725,    0, 620.5],
      [  0,  725, 187.0],
      [  0,    0,     1]];
  
baseline = 1.0;

img = imread('data/rgb.png');
disparity = double(imread('data/disparity.png'))/256;

Z = (725*baseline)./(disparity);

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

surf(xyz, img, 'FaceColor', 'texturemap', 'EdgeColor', 'none')
view(0,1000)
axis manual
