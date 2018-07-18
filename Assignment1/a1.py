import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.misc as sm
import math

#Read image
img_rgb = sm.imread('mountains.jpg')
#Allocate space for grayscale version of image
img_gray = np.zeros((img_rgb.shape[0], img_rgb.shape[1]))
#Convert image to grayscale
for row in range(len(img_rgb)):
	for col in range(len(img_rgb[row])):
		img_gray[row][col] = np.average(img_rgb[row][col])

#Setup variables to store filter h&w and image h&w
img_filter = np.array([[-1,-1,-1],[-1,4,-1],[-1,-1,-1]])[..., None]
img_filter_3d = np.repeat(img_filter, 3, axis=2)
img_height = img_gray.shape[0]
img_width = img_gray.shape[1]
img_depth = img_rgb.shape[2]
filter_height = img_filter.shape[0]
filter_width = img_filter.shape[1]

#Function to perform 2D correlation with image and filter
def correlate(padded_img, filter):
	img_output = np.zeros((img_height, img_width))
	for i in range(img_width):
		for j in range(img_height):
			img_output[j][i] = (filter*padded_img[j:j+filter_height, i:i+filter_width]).sum()

	return img_output

#Function to perform 2D correlation with rgb image and 3D filter
def correlate_3d(padded_img, filter):
	img_output = np.zeros((img_height, img_width))
	for i in range(img_width):
		for j in range(img_height):
			img_output[j][i] = (filter*padded_img[j:j+filter_height, i:i+filter_width, :]).sum()

	return img_output

#Add "zero-pad" to deal with border of the image
padded_img = np.zeros((img_height + 2, img_width + 2))   
padded_img[1:-1, 1:-1] = img_gray
output = correlate(padded_img, img_filter)

#Calculate number of padding zeros to add to top, bottom, left and right of image
padding_height = ((img_height - 1) + (filter_height - img_height)) 
padding_width = ((img_width - 1) + (filter_width - img_width))
padding_top = padding_height // 2
padding_bottom = padding_height - padding_top
padding_left = padding_width // 2
padding_right = padding_width - padding_left

#Add "zero-pad" to deal with top, bottom, left and right of image
padded_rgb_img = np.zeros((img_height + padding_height, img_width + padding_width, img_depth))
padded_rgb_img[padding_top:-padding_bottom, padding_left:-padding_right, :] = img_rgb
output_rgb = correlate_3d(padded_rgb_img, img_filter_3d)

#Plots
# fig1 = plt.figure()
# plt.imshow(img_gray, cmap=cm.Greys_r)
# fig1.suptitle("Original Grayscale Image")

# fig2 = plt.figure()
# plt.imshow(output, cmap=cm.Greys_r)
# fig2.suptitle("Correlated Grayscale Image")

# fig3 = plt.figure()
# plt.suptitle("Original RGB Image")
# plt.imshow(img_rgb)

# fig4 = plt.figure()
# plt.suptitle("Correlated RGB Image")
# plt.imshow(output_rgb)

# plt.show()

def create_gauss_filter(sigma_x, sigma_y):
	sigma = math.sqrt((sigma_x)**2 + (sigma_y)**2)
	# creates filter of shape based on mathworks imgaussfilt fn
	shape = 2 * math.ceil(2*sigma)+1
	u, v = np.mgrid[-shape:shape+1, -shape:shape+1]
	const = 2 * (sigma**2)
	h = np.exp(-((u**2 + v**2)/const))
	return h/(math.pi*const)
