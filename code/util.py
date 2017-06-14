import cv2
import os
import sys
import lines

def showImage(image, str, lines = [], colors = False, file_name = False):
	pid = os.fork()
	if(pid != 0):
		return
	lines_count = len(lines)
	if(colors):
		HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    	RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

    index = 0
    for line in lines:
    	if(colors):
        	cv2.line(image, (line.p1.x, line.p1.y), (line.p2.x, line.p2.y),tuple([255*x for x in RGB_tuples[index]]) , 2)
        else:
        	cv2.line(image, (line.p1.x, line.p1.y), (line.p2.x, line.p2.y), [0,255,0] , 2)
        index = index + 1


    if(file_name)
    	cv2.imwrite('result/'+file_name,image)

    cv2.imshow(str,image)
    cv2.waitKey(0)
    sys.exit()

def vectorToLines(vectorLines):
	lines = []
	for line in vector_lines:
		new_line = Line(Point(line[0][0], line[0][1]), Point(line[0][2], line[0][3]))
		if(new_line.length != 0):
			lines.append(new_line)

	return lines

def filter(lines):
	result_lines = []
	max_length = 0
	for line in lines:
		max_length = max(max_length,line.length)
	for line in lines:
		if(line.length > 0.1 *max_length):
			result_lines.append(line)

	return result_lines