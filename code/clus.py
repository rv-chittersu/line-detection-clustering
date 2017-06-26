import math
import lines
import util
import cv2
import numpy as np
from numpy import linalg as LA

def clusterBasedOnSlope(lines, dist_threshold, slope_threshold,image):
	lines_count = len(lines)
	current_count = lines_count

	active_lines = [1 for x in range(lines_count)]
	mutualSlope = [[0 for x in range(lines_count)] for y in range(lines_count)]
	mutualDistance = [[0 for x in range(lines_count)] for y in range(lines_count)]

	for index1 in range(lines_count):
		for index2 in range(index1 + 1, lines_count):
			mutualDistance[index1][index2] = mutualDistance[index2][index1] = getMinimalDistance(lines[index1], lines[index2])
			mutualSlope[index1][index2] = mutualSlope[index2][index1] = getSlopeBtwnLines(lines[index1],lines[index2])

	while(True):
		print current_count
		min_pair = []
		min_dist_observed = dist_threshold
		for index1 in range(lines_count):
			if active_lines[index1] == 0:
				continue
			for index2 in range(index1 + 1, lines_count):
				if active_lines[index2] == 0:
					continue
				if mutualDistance[index1][index2] <= min_dist_observed and abs(mutualSlope[index1][index2]) < slope_threshold:
					min_dist_observed = mutualDistance[index1][index2]
					min_pair = [index1, index2]
		if len(min_pair) == 0:
			break
		new_line = getMergedLine(lines[min_pair[0]], lines[min_pair[1]])

		#string = "l1 - {},l2 - {}, dist - {}, slope - {}".format(lines[min_pair[0]], lines[min_pair[1]], getMinimalDistance(lines[min_pair[0]],lines[min_pair[1]]), getSlopeBtwnLines(lines[min_pair[0]],lines[min_pair[1]]))
		#util.drawObservations(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR),lines[min_pair[0]],lines[min_pair[1]], new_line,string)
		
		lines[min_pair[0]] = new_line
		active_lines[min_pair[1]] = 0
		#update

		updated_index = min_pair[0]

		for index in range(lines_count):
			if active_lines[index] == 1 and index != updated_index:
				mutualDistance[index][updated_index] = mutualDistance[updated_index][index] = getMinimalDistance(lines[index],lines[updated_index])
				mutualSlope[index][updated_index] = mutualSlope[updated_index][index] = getSlopeBtwnLines(lines[index],lines[updated_index])
		current_count = current_count - 1

	result_lines = []
	for index in range(lines_count):
		if active_lines[index] == 1:
			result_lines.append(lines[index])

	return result_lines


def joinClustering(lines, dist_threshold, slope_threshold, offset_threshold,gray_sacle_image):
	lines_count = len(lines)
	
	current_count = lines_count
	active_lines = [1 for x in range(lines_count)]
	mutualSlope = [[0 for x in range(lines_count)] for y in range(lines_count)]
	mutualDistance = [[0 for x in range(lines_count)] for y in range(lines_count)]
	mutualOffset = [[0 for x in range(lines_count)] for y in range(lines_count)]

	for index1 in range(lines_count):
		for index2 in range(index1 + 1, lines_count):
			mutualDistance[index1][index2] = mutualDistance[index2][index1] = getMinimalDistance(lines[index1], lines[index2])
			mutualSlope[index1][index2] = mutualSlope[index2][index1] = getDevtnSlopeBtwnLines(lines[index1],lines[index2])
			mutualOffset[index1][index2] = mutualOffset[index2][index1] = getOffset(lines[index1],lines[index2])


	while(True):
		print current_count
		min_pair = []
		min_value_observed = dist_threshold * offset_threshold
		for index1 in range(lines_count):
			if active_lines[index1] == 0:
				continue
			for index2 in range(index1 + 1, lines_count):
				if active_lines[index2] == 0:
					continue
				if mutualDistance[index1][index2]*mutualOffset[index1][index2] <= min_value_observed and abs(mutualSlope[index1][index2]) < slope_threshold and mutualDistance[index1][index2] < dist_threshold and mutualOffset[index1][index2] < offset_threshold:
					min_value_observed = mutualDistance[index1][index2]*mutualOffset[index1][index2]
					min_pair = [index1, index2]
		if len(min_pair) == 0:
			break
		new_line = getMergedLine(lines[min_pair[0]], lines[min_pair[1]])

		string = "l1 - {},l2 - {}, dist - {}, slope - {}".format(lines[min_pair[0]], lines[min_pair[1]], getMinimalDistance(lines[min_pair[0]],lines[min_pair[1]]), getSlopeBtwnLines(lines[min_pair[0]],lines[min_pair[1]]))
		util.drawObservations(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR),lines[min_pair[0]],lines[min_pair[1]], new_line,string)
		
		lines[min_pair[0]] = new_line
		active_lines[min_pair[1]] = 0
		#update

		updated_index = min_pair[0]

		for index in range(lines_count):
			if active_lines[index] == 1 and index != updated_index:
				mutualDistance[index][updated_index] = mutualDistance[updated_index][index] = getMinimalDistance(lines[index],lines[updated_index])
				mutualSlope[index][updated_index] = mutualSlope[updated_index][index] = getDevtnSlopeBtwnLines(lines[index],lines[updated_index])
				mutualOffset[index][updated_index] = mutualOffset[updated_index][index] = getOffset(lines[index],lines[updated_index])
		current_count = current_count - 1


	result_lines = []
	for index in range(lines_count):
		if active_lines[index] == 1:
			result_lines.append(lines[index])

	return result_lines

def regClustering(lines, dist_threshold, area_threshold,gray_sacle_image):
	lines_count = len(lines)
	
	current_count = lines_count
	active_lines = [1 for x in range(lines_count)]
	mutualInfo = [[None for x in range(lines_count)] for y in range(lines_count)]

	for index1 in range(lines_count):
		for index2 in range(index1 + 1, lines_count):
			mutualInfo[index1][index2] = mutualInfo[index2][index1] = orthoRegression(lines[index1], lines[index2])


	while(True):
		print current_count
		min_pair = []
		min_value_observed = area_threshold
		for index1 in range(lines_count):
			if active_lines[index1] == 0:
				continue
			for index2 in range(index1 + 1, lines_count):
				if active_lines[index2] == 0:
					continue
				if mutualInfo[index1][index2]['area'] <= min_value_observed and mutualInfo[index1][index2]['distance'] < dist_threshold:
					min_value_observed = mutualInfo[index1][index2]['area']
					min_pair = [index1, index2]
		if len(min_pair) == 0:
			break
		new_line = mutualInfo[min_pair[0]][min_pair[1]]['line']

		#string = "l1 - {},l2 - {}, dist - {}, area - {}".format(lines[min_pair[0]], lines[min_pair[1]], mutualInfo[min_pair[0]][min_pair[1]]['distance'], mutualInfo[min_pair[0]][min_pair[1]]['area'])
		#util.drawObservations(cv2.cvtColor(gray_sacle_image, cv2.COLOR_GRAY2BGR),lines[min_pair[0]],lines[min_pair[1]], new_line,string)
		
		lines[min_pair[0]] = new_line
		active_lines[min_pair[1]] = 0
		#update

		updated_index = min_pair[0]

		for index in range(lines_count):
			if active_lines[index] == 1 and index != updated_index:
				mutualInfo[index][updated_index] = mutualInfo[updated_index][index] = orthoRegression(lines[index],lines[updated_index])
		current_count = current_count - 1


	result_lines = []
	for index in range(lines_count):
		if active_lines[index] == 1:
			result_lines.append(lines[index])

	return result_lines


def getDistanceBtwPoints(point1, point2):
	return math.hypot(point1.x - point2.x, point1.y - point2.y)

def getMergedLine(line1, line2):
	new_line_lengths = []

	new_line_lengths.append(getDistanceBtwPoints(line1.p1,line2.p1))
	new_line_lengths.append(getDistanceBtwPoints(line1.p1,line2.p2))
	new_line_lengths.append(getDistanceBtwPoints(line1.p2,line2.p1))
	new_line_lengths.append(getDistanceBtwPoints(line1.p2,line2.p2))
	new_line_lengths.append(line1.length)
	new_line_lengths.append(line2.length)

	max_index = 0
	max_length = new_line_lengths[0]

	for index in range(1,6):
		if new_line_lengths[index] > max_length:
			max_index = index
			max_length = new_line_lengths[index]
	
	if max_index == 0:
		return lines.Line(line1.p1,line2.p1)

	if max_index == 1:
		return lines.Line(line1.p1,line2.p2)

	if max_index == 2:
		return lines.Line(line1.p2,line2.p1)

	if max_index == 3:
		return lines.Line(line1.p2,line2.p2)

	if max_index == 4:
		return line1

	if max_index == 5:
		return line2
	

def getMinimalDistance(line1, line2):
	return lines.segments_distance(line1, line2)



def getSlopeBtwnLines(line1, line2):
	product_of_slopes = line1.slope*line2.slope
	if product_of_slopes == -1:
		return 99999
	return abs(float(line1.slope - line2.slope)/(1 + product_of_slopes))

def getDevtnSlopeBtwnLines(line1,line2):
	long_line = line1
	if line2.length > line1.length:
		long_line = line2

	new_line = getMergedLine(line1,line2)

	return getSlopeBtwnLines(long_line,new_line)

def getMinMid(line1,line2):
	new_line_lengths = []

	new_line_lengths.append(getDistanceBtwPoints(line1.p1,line2.p1))
	new_line_lengths.append(getDistanceBtwPoints(line1.p1,line2.p2))
	new_line_lengths.append(getDistanceBtwPoints(line1.p2,line2.p1))
	new_line_lengths.append(getDistanceBtwPoints(line1.p2,line2.p2))
	new_line_lengths.append(line1.length)
	new_line_lengths.append(line2.length)

	min_index = 0
	min_length = new_line_lengths[0]

	for index in range(1,6):
		if new_line_lengths[index] < min_length:
			min_length = new_line_lengths[index]
			min_index = index
	
	if min_index == 0:
		return lines.Point((line1.p1.x + line2.p1.x)*0.5, (line1.p1.y + line2.p1.y)*0.5)

	if min_index == 1:
		return lines.Point((line1.p1.x + line2.p2.x)*0.5, (line1.p1.y + line2.p2.y)*0.5)

	if min_index == 2:
		return lines.Point((line1.p2.x + line2.p1.x)*0.5, (line1.p2.y + line2.p1.y)*0.5)

	if min_index == 3:
		return lines.Point((line1.p2.x + line2.p2.x)*0.5, (line1.p2.y + line2.p2.y)*0.5)

	if min_index == 4:
		return lines.Point((line1.p1.x + line1.p2.x)*0.5, (line1.p1.y + line1.p2.y)*0.5)

	if min_index == 5:
		return lines.Point((line2.p1.x + line2.p2.x)*0.5, (line2.p1.y + line2.p2.y)*0.5)

def getOffset(line1, line2):
	new_line = getMergedLine(line1, line2)
	mid_point = getMinMid(line1, line2)
	return lines.perDist(new_line.p1.x, new_line.p1.y, new_line.p2.x, new_line.p2.y, mid_point.x, mid_point.y)

def getMergedLineByReg(line1,line2):
	net_count = line1.count + line2.count
	net_mean_x = (line1.count * line1.mean.x + line2.count * line2.mean.x)/net_count
	net_mean_y = (line1.count * line1.mean.y + line2.count * line2.mean.y)/net_count

	net_cov_xy = line1.sXY + line2.sXY - net_count * net_mean_x * net_mean_y
	net_var_x = line1.sXX + line2.sXX - net_count * net_mean_x * net_mean_x

	if net_var_x < 0:
		print " "
		print "{} - {}".format(line1, line1.length)
		print "{} - {}".format(line2, line2.length)
		print " "
	if net_var_x == 0:
		#line parllel to y - axis
		y_cords = [line1.p1.y, line1.p2.y, line2.p1.y, line2.p2.y]
		l =  lines.Line(lines.Point(net_mean_x, min(y_cords)), lines.Point(net_mean_x, max(y_cords)))
		d =  lines.segments_distance(lines.Line(lines.Point(net_mean_x, line1.p1.y), lines.Point(net_mean_x, line1.p2.y)), lines.Line(lines.Point(net_mean_x, line2.p1.y), lines.Point(net_mean_x, line2.p2.y)))
		net_area = (getArea(line1,l) + getArea(line2,l))/net_count

		return {
		 'line' : l,
		  'distance' :d,
		  'area' : net_area
		}
	if net_cov_xy == 0:
		#line parllel to x - axis
		x_cords = [line1.p1.x, line1.p2.x, line2.p1.x, line2.p2.x]
		l =  lines.Line(lines.Point(min(x_cords), net_mean_y), lines.Point(max(x_cords), net_mean_y))
		d =  lines.segments_distance(lines.Line(lines.Point(line1.p1.x, net_mean_y), lines.Point(line1.p2.x, net_mean_y)), lines.Line(lines.Point(line2.p1.x, net_mean_y), lines.Point(line2.p2.x, net_mean_y)))
		net_area = (getArea(line1,l) + getArea(line2,l))/net_count
		return {
		 'line' : l,
		  'distance' :d,
		  'area' : net_area
		}
	else:
		slope = net_cov_xy/net_var_x
		y_int = net_mean_y - slope * net_mean_x

		#print slope
		#print y_int
 
		pers = []
		pers.append(get_per(line1.p1,slope,y_int))
		pers.append(get_per(line1.p2,slope,y_int))
		pers.append(get_per(line2.p1,slope,y_int))
		pers.append(get_per(line2.p2,slope,y_int))

		#for index in range(0,4):
		#	print pers[index]

		min_index = 0
		max_index = 0

		for index in range(1,4):
			if pers[index].x < pers[min_index].x:
				min_index = index
			elif pers[index].x > pers[max_index].x:
				max_index = index

		#print min_index
		#print max_index

		l = lines.Line(pers[min_index],pers[max_index])
		d = lines.segments_distance(lines.Line(pers[0],pers[1]), lines.Line(pers[2], pers[3]))
		net_area = (getArea(line1,l) + getArea(line2,l))/net_count
		return {
		 'line' : l,
		  'distance' :d,
		  'area' : net_area
		}



def get_per(point, slope, y_int):
	denom = 1 + slope*slope
	x_cord = (point.x + slope * point.y - slope * y_int)/denom
	y_cord = (slope * point.x + slope * slope * point.y + y_int)/denom

	return lines.Point(x_cord,y_cord)


def getArea(line, reg_line):
	h1 = lines.point_segment_distance(line.p1, reg_line)
	h2 = lines.point_segment_distance(line.p2, reg_line)
	if lines.segments_intersect(line, reg_line):
		return (0.5) * reg_line.length * (h1 * h1 + h2 * h2)/(h1 + h2)
	else:
		return  (0.5) * reg_line.length * (h1 + h2)


def orthoRegression(l1,l2):
	nc = l1.count + l2.count
	sxx = l1.sXX + l2.sXX - (1/nc)*(l1.sX + l2.sX)*(l1.sX + l2.sX)
	syy = l1.sYY + l2.sYY - (1/nc)*(l1.sY + l2.sY)*(l1.sY + l2.sY)
	sxy = l1.sXY + l2.sXY - (1/nc)*(l1.sX + l2.sX)*(l1.sY + l2.sY)

	w, v = LA.eig(np.array([[sxx, sxy], [sxy, syy]]))

	first_comp = 0
	if w[1] > w[0]:
		first_comp = 1

	numerator = v[1][first_comp]
	deneominator = v[0][first_comp]

	line1 = l1
	line2 = l2
	net_count = nc
	net_mean_x = (1/nc) * (l1.sX + l2.sX)
	net_mean_y = (1/nc) * (l1.sY + l2.sY)

	if deneominator == 0:
		#line parllel to y - axis
		y_cords = [line1.p1.y, line1.p2.y, line2.p1.y, line2.p2.y]
		l =  lines.Line(lines.Point(net_mean_x, min(y_cords)), lines.Point(net_mean_x, max(y_cords)))
		d =  lines.segments_distance(lines.Line(lines.Point(net_mean_x, line1.p1.y), lines.Point(net_mean_x, line1.p2.y)), lines.Line(lines.Point(net_mean_x, line2.p1.y), lines.Point(net_mean_x, line2.p2.y)))
		net_area = (getArea(line1,l) + getArea(line2,l))/net_count

		return {
		 'line' : l,
		  'distance' :d,
		  'area' : net_area
		}
	if numerator == 0:
		#line parllel to x - axis
		x_cords = [line1.p1.x, line1.p2.x, line2.p1.x, line2.p2.x]
		l =  lines.Line(lines.Point(min(x_cords), net_mean_y), lines.Point(max(x_cords), net_mean_y))
		d =  lines.segments_distance(lines.Line(lines.Point(line1.p1.x, net_mean_y), lines.Point(line1.p2.x, net_mean_y)), lines.Line(lines.Point(line2.p1.x, net_mean_y), lines.Point(line2.p2.x, net_mean_y)))
		net_area = (getArea(line1,l) + getArea(line2,l))/net_count
		return {
		 'line' : l,
		  'distance' :d,
		  'area' : net_area
		}
	else:
		slope = numerator/deneominator
		y_int = (1/nc)*((l1.sY + l2.sY) - slope * (l1.sX + l2.sX))

		#print slope
		#print y_int
	
		pers = []
		pers.append(get_per(line1.p1,slope,y_int))
		pers.append(get_per(line1.p2,slope,y_int))
		pers.append(get_per(line2.p1,slope,y_int))
		pers.append(get_per(line2.p2,slope,y_int))

		#for index in range(0,4):
		#	print pers[index]

		min_index = 0
		max_index = 0

		for index in range(1,4):
			if pers[index].x < pers[min_index].x:
				min_index = index
			elif pers[index].x > pers[max_index].x:
				max_index = index

		#print min_index
		#print max_index

		l = lines.Line(pers[min_index],pers[max_index])
		d = lines.segments_distance(lines.Line(pers[0],pers[1]), lines.Line(pers[2], pers[3]))
		net_area = (getArea(line1,l) + getArea(line2,l))/nc
		return {
		 'line' : l,
		  'distance' :d,
		  'area' : net_area
		}


