import cv2
import os
import sys
import lines
import clus
import colorsys

def showImage(image, str, input_lines = [], colors = False, file_name = False):
	lines_count = len(input_lines)
	HSV_tuples = []
	RGB_tuples = []
	if(colors):
		HSV_tuples = [(x*1.0/lines_count, 0.5, 0.5) for x in range(lines_count)]
    	RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

	index = 0
	for line in input_lines:
		if(colors):
			cv2.line(image, (int(line.p1.x), int(line.p1.y)), (int(line.p2.x), int(line.p2.y)),tuple([255*x for x in RGB_tuples[index]]) , 2)
		else:
			cv2.line(image, (int(line.p1.x), int(line.p1.y)), (int(line.p2.x), int(line.p2.y)), [0,255,0] , 2)
		index = index + 1

	if file_name:
		cv2.imwrite('../'+file_name,image)

	cv2.imshow(str,image)
	cv2.waitKey(0)

def vectorToLines(vector_lines):
	new_lines = []
	for line in vector_lines:
		new_line = lines.Line(lines.Point(line[0][0], line[0][1]), lines.Point(line[0][2], line[0][3]))
		if(new_line.length != 0):
			new_lines.append(new_line)

	return new_lines

def filter(lines):
	result_lines = []
	max_length = 0
	for line in lines:
		max_length = max(max_length,line.length)
	for line in lines:
		if(line.length > 0.1 *max_length):
			result_lines.append(line)

	return result_lines

def drawObservations(image,line1,line2,line3,string):
	cv2.line(image, (int(line1.p1.x), int(line1.p1.y)), (int(line1.p2.x), int(line1.p2.y)), [255,0,0] , 2)
	cv2.line(image, (int(line2.p1.x), int(line2.p1.y)), (int(line2.p2.x), int(line2.p2.y)), [0,255,0] , 2)
	cv2.line(image, (int(line3.p1.x), int(line3.p1.y)), (int(line3.p2.x), int(line3.p2.y)), [0,0,255] , 2)
	cv2.imshow(string,image)
	cv2.waitKey(0)

def drawObservation(image,line1,string):
	cv2.line(image, (int(line1.p1.x), int(line1.p1.y)), (int(line1.p2.x), int(line1.p2.y)), [255,0,0] , 2)
	cv2.imwrite('../res/{}.jpg'.format(string),image)

def commbinedInfo(line1,line2):
	print line1
	print line2
	print clus.getMinimalDistance(line1,line2)
	print clus.getDevtnSlopeBtwnLines(line1,line2)
	print clus.getOffset(line1, line2)
	print " "