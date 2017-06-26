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
		p1 = lines.Point(line[0][0], line[0][1])
		p2 = lines.Point(line[0][2], line[0][3])
		if p1.x == p2.x and p1.y == p2.y:
			continue
		new_line = lines.Line(p1, p2)
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

def printPoints(line1,line2):
	arr = []
	str1 = ""
	str2 = ""
	for index in range(0,int(line1.count)):
		arr.append([line1.p1.x + index * line1.sin, line1.p1.y + index * line1.cos])
		str1 = str1 + "({},{})".format(line1.p1.x + index * line1.sin ,line1.p1.y + index * line1.cos) 
		print "{} {}".format(line1.p1.x + index * line1.sin ,line1.p1.y + index * line1.cos)
		if index != line1.count - 1:
			str1 = str1 + ","

	for index in range(0,int(line2.count)):
		arr.append([line2.p1.x + index * line2.sin, line2.p1.y + index * line2.cos])
		str2 = str2 + "({},{})".format(line2.p1.x + index * line2.sin ,line2.p1.y + index * line2.cos)
		print "{} {}".format(line2.p1.x + index * line2.sin ,line2.p1.y + index * line2.cos)
		if index != line2.count - 1:
			str2 = str2 + ","
	print arr
	print str1
	print str2