% read images and grayscale
im_1 = imread('data/landscape_1.jpg');
img_landscape_1 = single(rgb2gray(im_1));
im_2 = imread('data/landscape_2.jpg');
img_landscape_2 = single(rgb2gray(im_2));

Affine_Transformation = RANSAC(img_landscape_1, img_landscape_2);
stitch_imgs(im_1, im_2, Affine_Transformation);

% get frames and descriptors for images
function [f, d] = getSIFTFeatures(image)
[f, d] = vl_sift(image);
end

% get matches using vl_ubcmatch instead of A2 code
function [matches, scores] = getMatches(d_1, d_2)
[matches, scores] = vl_ubcmatch(d_2, d_1);
end

% function to get affine transformation between two points p1, p2
function affine = getAffine(p1, p2)
G = [  p2(1,1) p2(2,1) 0 0 1 0; 
       0    0   p2(1,1) p2(2,1) 0 1;
       p2(1,2) p2(2,2) 0 0 1 0; 
       0    0   p2(1,2) p2(2,2) 0 1;
       p2(1,3) p2(2,3) 0 0  1 0 ; 
       0    0   p2(1,3) p2(2,3) 0 1;
       ];

F = [ p1(1,1);p1(2,1);p1(1,2);p1(2,2);p1(1,3);p1(2,3)] ;
E = G\F;
affine = [E(1) E(2) E(5);
     E(3) E(4) E(6)];
end

% RANSAC
function Transformation = RANSAC(img1, img2)
[f1, d1] = getSIFTFeatures(img1);
[f2, d2] = getSIFTFeatures(img2);
[matches, scores] = getMatches(d1, d2);
[B, I] = sort(scores);
[m, n] = size(I);
best_points = 0;

for i = 1 : 1000
    random_num = randperm(n, 3);
    int1 = random_num(1);
    int2 = random_num(2);
    int3 = random_num(3);
    p2 = [ f2(1,matches(1,int1)) f2(1,matches(1,int2)) f2(1,matches(1,int3)) ; f2(2, matches(1,int1)) f2(2, matches(1,int2)) f2(2, matches(1,int3)) ] ;
    p1 = [ f1(1, matches(2,int1)) f1(1, matches(2,int2)) f1(1, matches(2,int3)) ; f1(2, matches (2,int1)) f1(2, matches (2,int2)) f1(2, matches (2,int3)) ] ;
    
    affine = getAffine(p1, p2);
    matched_so_far = 0;
    
    for index = 1 : n
        Point2 = [f2(1,matches(1,index)); f2(2,matches(1,index)) ; 1];
        Point1 = [f1(1,matches(2,index)); f1(2,matches(2,index)) ; 1];
        T2Point = affine*Point2;
        Euclidean_dist = sqrt( (Point1(1)-T2Point(1))^2 + (Point1(2)-T2Point(2))^2 );
        if Euclidean_dist <= 2
            matched_so_far = matched_so_far + 1;
        end
    end
    
    if matched_so_far > best_points
        best_points = matched_so_far;
        best_affine = affine;
        best_int1 = int1;
        best_int2 = int2;
        best_int3 = int3;
    end
end
Transformation = best_affine
end

function stitch_imgs(J, K, A)
[m1,n1] = size(single(rgb2gray(J)));
[m2,n2] = size(single(rgb2gray(K)));

T1 = [1 0 0; 0 1 0; 100 0 1];
rotation = [ cos(-pi/16) -sin(-pi/16) 0; sin(-pi/16) cos(-pi/16) 0 ; 0 0 1];
scaling = [ 0.8 0 0 ; 0 0.8 0; 0 0 1];
translation = [1 0 0; 0 1 0; 100 50 1];
T2 = translation*scaling*rotation;

AffineTransformation1Image = zeros(m2,n2+T1(3,1),3);
AffineTransformation2Image = zeros(m2+round(A(1,3)), n2,3);
MosaicImage = zeros(m1+round(A(2,3)),n1+round(A(1,3)),3);

tform2 = affine2d(T2);
tform1 = affine2d(T1);

for i = 1: m2
    for j = 1: n2
        for k = 1:3
         u = [A(1,1) A(1,2) ; A(2,1) A(2,2) ]*[i;j];
         in1 = round(u(1));
         if in1 <= 0
            in1 = 1;
         end
         in2 = round(u(2)); 
         if in2 <= 0
            in2 = 1;
         end
        
         if round(A(1,1)*i)+round(A(1,2)*j)-round(A(2,3)) <= 0
            Offset = -round(A(1,1)*i)-round(A(1,2)*j) + 1; 
         else
            Offset =  round(A(2,3));
         end
        
         MosaicImage(Offset+round(A(1,1)*i)+round(A(1,2)*j),round(A(1,3))+round(A(2,1)*i)+round(A(2,2)*j),k) = K(i,j,k);
         AffineTransformation1Image(in1,in2,k) = K(i,j,k);
         AffineTransformation2Image(in1,in2,k) = K(i,j,k);

        end 
    end
end

Rcb1 = imref2d(size(AffineTransformation1Image));
[AffineTransformation1Image] = imwarp(AffineTransformation1Image, tform1,'OutputView',Rcb1);

Rcb2 = imref2d(size(AffineTransformation2Image));
[AffineTransformation2Image] = imwarp(AffineTransformation2Image, tform2,'OutputView',Rcb2);

for i = 1: m1
    for j = 1: n1
        for k = 1: 3
        
        MosaicImage(i,j,k) = J(i,j,k);
        AffineTransformation1Image(i,j,k) = J(i,j,k);
        AffineTransformation2Image(i,j,k) = J(i,j,k);
        
        end         
    end
end

figure;
image(uint8(MosaicImage));
title('Stitched 2 images');
end
