import math
import lines

def clusterBasedOnSlope(lines, dist_threshold, slope_threshold):
	int lines_count = len(lines)
	active_lines = [1 for x in range(lines_count)]
	mutualSlope = [[0 for x in range(lines_count)] for y in range(lines_count)]
	mutualDistance = [[0 for x in range(lines_count)] for y in range(lines_count)]

	for index1 in range(lines_count):
		for index2 in range(index1 + 1, lines_count):
			mutualDistance[index1][index2] = mutualDistance[index2][index1] = getMinimalDistance(lines[index1], lines[index2])
			mutualSlope[index1][index2] = mutualSlope[index2][index1] = getSlopeBtwnLines(lines[index1],lines[index2])

	while(True):
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
		lines[min_pair[0]] = new_line
		active_lines[min_pair[1]] = 0
		#update

		updated_index = min_pair[0]

		for index in range(lines_count):
			if active_lines[index] == 1 and index != updated_index:
				mutualDistance[index][updated_index] = mutualDistance[updated_index][index] = getMinimalDistance(lines[index],lines[updated_index])
				mutualSlope[index][updated_index] = mutualSlope[updated_index][index] = getSlopeBtwnLines(lines[index],lines[updated_index])

	result_lines = []
	for index in range(lines_count):
		if active_lines[index] == 1:
			result_lines.append(lines[index])

	return result_lines


def joinClustering(lines, dist_threshold, slope_threshold, offset_threshold):
	int lines_count = len(lines)
	active_lines = [1 for x in range(lines_count)]
	mutualSlope = [[0 for x in range(lines_count)] for y in range(lines_count)]
	mutualDistance = [[0 for x in range(lines_count)] for y in range(lines_count)]
	mutualOffset = [[0 for x in range(lines_count)] for y in range(lines_count)]

	for index1 in range(lines_count):
		for index2 in range(index1 + 1, lines_count):
			mutualDistance[index1][index2] = mutualDistance[index2][index1] = getMinimalDistance(lines[index1], lines[index2])
			mutualSlope[index1][index2] = mutualSlope[index2][index1] = getDevtnSlopeBtwnLines(lines[index1],lines[index2])
			mutualOffset[index1][index2] = mutualSlope[index2][index1] = getOffset(lines[index1],lines[index2])


	while(True):
		min_pair = []
		min_value_observed = slope_threshold * offset_threshold
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
		lines[min_pair[0]] = new_line
		active_lines[min_pair[1]] = 0
		#update

		updated_index = min_pair[0]

		for index in range(lines_count):
			if active_lines[index] == 1 and index != updated_index:
				mutualDistance[index][updated_index] = mutualDistance[updated_index][index] = getMinimalDistance(lines[index],lines[updated_index])
				mutualSlope[index][updated_index] = mutualSlope[updated_index][index] = getDevtnSlopeBtwnLines(lines[index],lines[updated_index])
				mutualOffset[index][updated_index] = mutualSlope[updated_index][index] = getOffset(lines[index],lines[updated_index])

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

	max_index = 0
	max_length = new_line_lengths[0]

	for index in range(1,4):
		if new_line_lengths[index] > max_length:
			max_index = index
	
	if max_index == 0
		return Line(line1.p1,line2.p1)

	if max_index == 1
		return Line(line1.p1,line2.p2)

	if max_index == 2
		return Line(line1.p2,line2.p1)

	if max_index == 3
		return Line(line1.p2,line2.p2)
	

def getMinimalDistance(line1, line2):
	return lines.segments_distance(line1, line2)



def getSlopeBtwnLines(line1, line2):
	product_of_slopes = line1.slope*line2,slope
	if product_of_slopes == -1:
		return 99999
	return float(line1.slope - line2.slope)/(1 + product_of_slopes)

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

	min_index = 0
	min_length = new_line_lengths[0]

	for index in range(1,4):
		if new_line_lengths[index] < min_length:
			min_length = index
	
	if min_length == 0
		return Point((line1.p1.x + line2.p1.x)*0.5, (line1.p1.y + line2.p1.y)*0.5)

	if min_length == 1
		return Point((line1.p1.x + line2.p2.x)*0.5, (line1.p1.y + line2.p2.y)*0.5)

	if min_length == 2
		return Point((line1.p2.x + line2.p1.x)*0.5, (line1.p2.y + line2.p1.y)*0.5)

	if min_length == 3
		return Point((line1.p2.x + line2.p2.x)*0.5, (line1.p2.y + line2.p2.y)*0.5)

def getOffset(line1, line2):
	new_line = getMergedLine(line1, line2)
	mid_point = getMinMid(line1, line2)
	return lines.perDist(new_line.p1.x, new_line.p1.y, new_line.p2.x, new_line.p2.y, mid_point.x, mid_point.y)