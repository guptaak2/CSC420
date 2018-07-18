import numpy as np
from skimage.segmentation import slic
from sklearn.neural_network import MLPClassifier
from skimage.feature import hog
import cv2
import glob

# Label all pixels and generate segmentation images.
def main():
    # Multiclass (i.e clothes).
    segmentation(False)
    # Binary (i.e person).
    segmentation(True)

def segmentation(personOnly = False):
    # Open all images.
    images = [cv2.imread(f) for f in glob.glob("images/*.jpg")]
    trainImgs = images[:300]
    valImgs = images[300:360]
    testImgs = images[360:]
    
    labelType = 'clothes'
    labelFactor = 14
    if personOnly:
        labelType = 'person'
        labelFactor = 255
        
    # Open all label images.
    labelImages = [cv2.imread(f, cv2.IMREAD_GRAYSCALE) / labelFactor
                   for f in glob.glob('labels/*_' + labelType + '.png')]
    trainLabels = labelImages[:300]
    valLabels = labelImages[300:360]
    testLabels = labelImages[360:]
    
    # Compute superpixels for each image.
    superpixels = [slic(img.astype(float)) for img in images]
    trainSP = superpixels[:300]
    valSP = superpixels[300:360]
    testSP = superpixels[360:]
    
    # Compute feature vectors and labels for training data. Also get the
    # Features per image to map the segments to the correct image.
    trainFeatures, trainLabels, trainFPI = computeAllFeaturesAndLabels(
                                                             trainImgs,
                                                             trainLabels,
                                                             trainSP,
                                                             personOnly)
    # Compute feature vectors and labels for validation data. Also get the
    # Features per image to map the segments to the correct image.
    valFeatures, valLabels, valFPI = computeAllFeaturesAndLabels(valImgs,
                                                             valLabels,
                                                             valSP,
                                                             personOnly)
    # Compute feature vectors and labels for test data. Also get the
    # Features per image to map the segments to the correct image.
    testFeatures, testLabels, testFPI = computeAllFeaturesAndLabels(testImgs,
                                                             testLabels,
                                                             testSP,
                                                             personOnly)
    # Train clasifier.
    clf = MLPClassifier(hidden_layer_sizes=(200, 200, 200), max_iter=10000)
    clf.fit(trainFeatures, trainLabels)
    
    # Predict validation images.
    predictionsVal = clf.predict(valFeatures)
    predictedImgsVal = labelPixels(predictionsVal, valSP, valFPI)
    # Predict Test images.
    predictionsTest = clf.predict(testFeatures)
    predictedImgsTest = labelPixels(predictionsTest, valSP, valFPI)
    # Predict train images.
    predictionsTrain = clf.predict(trainFeatures)
    predictedImgsTrain = labelPixels(predictionsTrain, valSP, valFPI)
    
    # Save all the predicted images.
    saveSegImages(predictedImgsTrain + predictedImgsVal + predictedImgsTest,
                  personOnly, labelFactor, 1)
    
    

# Compute the feature vectors and labels for all 'images' using 'labelImages'
# and 'superpixels'.
def computeAllFeaturesAndLabels(images, labelImages, superpixels, personOnly):
    # Keep track of the number of features per image.
    featuresPerImage = []
    # List of all feature vectors of all images.
    allFeatures = []
    # List of all labels of all images.
    allLabels = []
    
    for i in range(len(images)):
        curFeatures, labels = computeFeaturesAndLabelsPerImage(images[i],
                                                               labelImages[i],
                                                               superpixels[i],
                                                               personOnly)
        featuresPerImage.append(len(curFeatures))
        allFeatures += curFeatures
        allLabels += labels
    
    return allFeatures, allLabels, featuresPerImage

# Compute the feature vectors and labels for 'image' using 'labelImage' and
# 'superpixels'.
def computeFeaturesAndLabelsPerImage(image, labelImage,
                                     superpixels, personOnly):
    # Use this many pixels squared of each segment.
    SEG_SIZE = 28
    features= []
    labels = []
    
    # Convert image to grayscale.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Loop through each segment label in 'superpixels'.
    for segLabel in range(np.max(superpixels) + 1):
        # Get the first 'SEG_SIZE' squared pixel coordinates in the current 
        # segment (y, x).
        segCoords = np.argwhere(superpixels == segLabel)[:SEG_SIZE ** 2]
        Xs = segCoords[:, 1]
        Ys = segCoords[:, 0]

        # Reshape the segment into a square.
        segment = image[Ys, Xs].reshape(SEG_SIZE, SEG_SIZE)
        featureVector = hog(segment)
        features.append(featureVector)
        
        # Most common label in this segment.
        labelPixelVal = np.argmax(np.bincount(labelImage[Ys, Xs]))
        # One-hot encoded value.
        numberOfClasses = 7
        if personOnly:
            numberOfClasses = 2
        label = np.zeros(numberOfClasses)
        # Changing the pixel value of the label to be in range 0-6 (or 0-1).
        label[min(labelPixelVal, 6)] = 1
        labels.append(label)
        
    return features, labels

# Label all pixels in all images.      
def labelPixels(labels, superpixels, featuresPerImage):
    # Contains all the labeled images.
    labeledImages = []
    # Starting index of the labels for the current image.
    start = 0
    for i in range(len(featuresPerImage)):
        # Ending index of the labels for the current image.
        end = start + featuresPerImage[i]
        labeledImages.append(labelPixelsSingleImage(labels[start: end],
                                                    superpixels[i]))
        start = end
    
    return labeledImages

# Label individual pixels based on what segment they belong to 
# indicated by 'superpixels'. 
def labelPixelsSingleImage(labels, superpixels):
    nonZeros = 0
    labeled = np.copy(superpixels)
    # The index of labels corresponds to the segment label in its image.
    for i in range(len(labels)):
        # Assign the label to all pixels in the segment.
        labeled[labeled == i] = np.argmax(labels[i])
        if np.argmax(labels[i]) > 0:
            nonZeros += 1
     
    return labeled

# Save the segmented images.
def saveSegImages(images, personOnly, labelFactor, firstImgNum):
    segType = 'clothes'
    if personOnly:
        segType = 'person'
    
    for i in range(len(images)):
        fileName = 'results-seg/' + format(i + firstImgNum,
                                           '04') + '_' + segType + '.png'
        cv2.imwrite(fileName, images[i] * labelFactor)

if __name__== "__main__":
    main() 
    