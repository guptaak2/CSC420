% SIFT features for reference.png and test.png
function out = a2q2b()

% read images and grayscale
im_test = imread('test2.png');
img_test = single(rgb2gray(im_test));
im_ref = imread('reference.png');
img_ref = single(rgb2gray(im_test));

% get frames and descriptors for images
[f_test, d_test] = vl_sift(img_test);
[f_ref, d_ref] = vl_sift(img_ref);

% find matches via euclidean distance
dist = dist2(double(d_ref.'), double(d_test.'));
[imrows, imcols] = size(dist);

% calculate ratios and first and second closest matches
[dist_sorted, dist_index] = sort(dist, 2);
for i = 1:imrows
    closest = dist_index(i, 1);
    second = dist_index(i, 2);
    ratio = dist_sorted(i, 1)./dist_sorted(i, 2);
    if ratio < 0.8
        matches(i) = closest;
        ratios(i) = ratio;
    else
        matches(i) = 0;
        ratios(i) = Inf;
    end
end


% get top 3 correspondences by choosing matches with lowest ratio
[ratio_sorted, ratio_index] = sort(ratios);
for index = 1:3
    ind = ratio_index(1, index);
    top(ind) = matches(ind);
end

indices = find(top > 0);

% Plot images
% figure;
% imshow(im_ref);
% hold on;
% mr1 = plotsiftframe(f_ref(:, indices(1):indices(1))); set(mr1,'color','r','linewidth',3) ;
% mr2 = plotsiftframe(f_ref(:, indices(2):indices(2))); set(mr2,'color','g','linewidth',3) ;
% mr3 = plotsiftframe(f_ref(:, indices(3):indices(3))); set(mr3,'color','b','linewidth',3) ;
% hold off;  
% 
% figure;
% imshow(im_ref)
% 
% imshow(im_test);
% hold on;
% mr1 = plotsiftframe(f_test(:, top(indices(1)):top(indices(1)))); set(mr1,'color','r','linewidth',3) ;
% mr2 = plotsiftframe(f_test(:, top(indices(2)):top(indices(2)))); set(mr2,'color','g','linewidth',3) ;
% mr3 = plotsiftframe(f_test(:, top(indices(3)):top(indices(3)))); set(mr3,'color','b','linewidth',3) ;
% hold off;

% Return map with frames and key feature indices
out = containers.Map({'f_ref', 'f_test', 'ref_indices', 'test_indices'}, {f_ref, f_test, [indices(1), indices(2), indices(3)],[top(indices(1)), top(indices(2)), top(indices(3))]});
end