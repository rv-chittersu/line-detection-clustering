import cv2
import numpy as np
import math
import clus
import util
import colorsys
import sys

file_name = sys.argv[1]

canny_min_threshold = 200
canny_max_threshold = 400

hough_threshold = 30

gray_sacle_image = cv2.imread('../testData/'+file_name, cv2.IMREAD_GRAYSCALE)
canny_edge_image = cv2.Canny(gray_sacle_image,canny_min_threshold,canny_max_threshold)

util.showImage(canny_edge_image,'Canny Edge Detection')

rho = 1                  #resolution of r in pixels
theta = np.pi/180.0      #resolution of theta in radians
hough_lines = cv2.HoughLinesP(np.copy(canny_edge_image), rho, theta, hough_threshold)

hough_lines = util.vectorToLines(hough_lines)

util.showImage(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR), 'Hough Line Detection', hough_lines)

slope_clustered_lines = clus.clusterBasedOnSlope(hough_lines, 2, 0.37)

util.showImage(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR), 'Slope based Line Clustering', slope_clustered_lines, True)

join_clustered_lines = clus.joinClustering(slope_clustered_lines, 20, 0.6, 30)

filtered_lines = util.filter(join_clustered_lines)

util.showImage(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR), 'Join Line Clustering', filtered_lines, True, file_name)
