function out = q3a(image)
% calculate magnitude of gradient
[Gx, Gy] = imgradientxy(image);
Gmag = sqrt(Gx.^2 + Gy.^2);
imshow(Gmag, []);
out = Gmag;
end