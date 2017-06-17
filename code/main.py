import cv2
import numpy as np
import math
import clus
import util
import colorsys
import sys

file_name = sys.argv[1]

canny_min_threshold = 40
canny_max_threshold = 100

hough_threshold = 30

gray_sacle_image = cv2.imread('../testData/'+file_name, cv2.IMREAD_GRAYSCALE)
canny_edge_image = cv2.Canny(gray_sacle_image,canny_min_threshold,canny_max_threshold)

util.showImage(canny_edge_image,'Canny Edge Detection')

rho = 1                  #resolution of r in pixels
theta = np.pi/180.0      #resolution of theta in radians
hough_lines = cv2.HoughLinesP(np.copy(canny_edge_image), rho, theta, hough_threshold)

hough_lines = util.vectorToLines(hough_lines)

#util.showImage(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR), 'Hough Line Detection', hough_lines, False ,'res1.jpg')

slope_clustered_lines = clus.clusterBasedOnSlope(hough_lines, 2, 0.37)

#for index in range(len(slope_clustered_lines)):
#	util.drawObservation(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR), slope_clustered_lines[index], "index{}".format(index))


#util.showImage(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR), 'Slope based Line Clustering', slope_clustered_lines, True, 'res2.jpg')

join_clustered_lines = clus.joinClustering(slope_clustered_lines, 20, 0.6, 10,gray_sacle_image)

#filtered_lines = util.filter(join_clustered_lines)

#for index in range(len(join_clustered_lines)):
#	util.drawObservation(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR), join_clustered_lines[index], "index{}".format(index))

#util.commbinedInfo(join_clustered_lines[0],join_clustered_lines[4])
#util.commbinedInfo(join_clustered_lines[6],join_clustered_lines[4])
#util.commbinedInfo(join_clustered_lines[0],join_clustered_lines[6])


util.showImage(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR), 'Join Line Clustering', join_clustered_lines, True, 'res3.jpg')