import cv2
import numpy as np

def compute_sift(img1, img2):
	# Initialize SIFT 
	sift = cv2.xfeatures2d.SIFT_create()

	# Extract keypoints and descriptors
	k1, d1 = sift.detectAndCompute(img1, None)
	k2, d2 = sift.detectAndCompute(img2, None)

	# Bruteforce matcher to be run on descriptors
	bf = cv2.BFMatcher()
	matches = bf.knnMatch(d1,d2, k=2)

	threshold = 0.8
	final_matches = []
	for m1, m2 in matches:
		if m1.distance < threshold * m2.distance:
			final_matches.append(m1)

	min_matches = 8
	if len(final_matches) > min_matches:
		img1_pts = []
		img2_pts = []

		for match in final_matches:
			img1_pts.append(k1[match.queryIdx].pt)
			img2_pts.append(k2[match.trainIdx].pt)

		img1_pts = np.float32(img1_pts).reshape(-1,1,2)
		img2_pts = np.float32(img2_pts).reshape(-1,1,2)
		
		# Compute homography
		M, mask = cv2.findHomography(img1_pts, img2_pts, cv2.RANSAC, 5.0)
		return M

def stitch_images(img1, img2, M):
	# get size of input images
	w1, h1 = img1.shape[:2]
	w2, h2 = img2.shape[:2]

	img1_dims = np.float32([ [0,0], [0,w1], [h1, w1], [h1,0] ]).reshape(-1,1,2)
	img2_dims_temp = np.float32([ [0,0], [0,w2], [h2, w2], [h2,0] ]).reshape(-1,1,2)

	# Get perspective of second image
	img2_dims = cv2.perspectiveTransform(img2_dims_temp, M)

	result_dims = np.concatenate((img1_dims, img2_dims), axis = 0)

	# Calculate dimensions of match points
	[x_min, y_min] = np.int32(result_dims.min(axis=0).ravel() - 0.5)
	[x_max, y_max] = np.int32(result_dims.max(axis=0).ravel() + 0.5)
	
	# Create output array after affine transformation 
	transform_dist = [-x_min,-y_min]
	transform_array = np.array([[1, 0, transform_dist[0]], 
								[0, 1, transform_dist[1]], 
								[0,0,1]]) 

	# Warp images
	result_img = cv2.warpPerspective(img2, transform_array.dot(M), (x_max-x_min, y_max-y_min))
	result_img[transform_dist[1]:w1+transform_dist[1], transform_dist[0]:h1+transform_dist[0]] = img1

	return result_img

# Read input images
img1 = cv2.imread('data/landscape_1.jpg')
img2 = cv2.imread('data/landscape_2.jpg')
img3 = cv2.imread('data/landscape_3.jpg')
img4 = cv2.imread('data/landscape_4.jpg')
img5 = cv2.imread('data/landscape_5.jpg')
img6 = cv2.imread('data/landscape_6.jpg')
img7 = cv2.imread('data/landscape_7.jpg')
img8 = cv2.imread('data/landscape_8.jpg')
img9 = cv2.imread('data/landscape_9.jpg')

# Use SIFT to find keypoints and compute homography matrix
# and Stitch the images together using homography matrix
M_1 =  compute_sift(img1, img2)
result_image_1 = stitch_images(img2, img1, M_1)

M_2 =  compute_sift(img3, img4)
result_image_2 = stitch_images(img4, img3, M_2)

M_3 =  compute_sift(img5, img6)
result_image_3 = stitch_images(img6, img5, M_3)

M_4 =  compute_sift(img7, img8)
result_image_4 = stitch_images(img8, img7, M_4)

M_5 = compute_sift(result_image_1, result_image_2)
result_image_5 = stitch_images(result_image_2, result_image_1, M_5)

M_6 = compute_sift(result_image_3, result_image_4)
result_image_6 = stitch_images(result_image_4, result_image_3, M_6)

M_7 = compute_sift(result_image_6, img9)
result_image_7 = stitch_images(img9, result_image_6, M_7)

# M_8 = compute_sift(result_image_5, result_image_7)
# result_image_8 = stitch_images(result_image_7, result_image_5, M_8)

# Show stitched image
cv2.imwrite('panorama_7.jpg',result_image_7)
cv2.imwrite('panorama_5.jpg',result_image_5)
# cv2.imshow ('Stitched Image', result_image_8)
# cv2.waitKey()
