"""Calculate the distance between line segments."""

import math


class Point(object):
    """A two dimensional point."""
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


class Line(object):
    """A line segment in a two dimensional space."""
    def __init__(self, p1, p2):
        assert isinstance(p1, Point), \
            "p1 is not of type Point, but of %r" % type(p1)
        assert isinstance(p2, Point), \
            "p2 is not of type Point, but of %r" % type(p2)
        self.p1 = p1
        self.p2 = p2
        self.slope = self.getSlope()
        self.length = self.getLength()

    def getSlope(self):
    	if(self.p1.y == self.p2.y):
    		return 99999
    	return float(p2.x - p1.x)/(p2.y - p1.y)

    def getLength(self)
    	return math.hypot(p2.x - p1.x, p2.y - p1.y)


def segments_distance(segment1, segment2):
    """Calculate the distance between two line segments in the plane.

    >>> a = LineSegment(Point(1,0), Point(2,0))
    >>> b = LineSegment(Point(0,1), Point(0,2))
    >>> "%0.2f" % segments_distance(a, b)
    '1.41'
    >>> c = LineSegment(Point(0,0), Point(5,5))
    >>> d = LineSegment(Point(2,2), Point(4,4))
    >>> e = LineSegment(Point(2,2), Point(7,7))
    >>> "%0.2f" % segments_distance(c, d)
    '0.00'
    >>> "%0.2f" % segments_distance(c, e)
    '0.00'
    """
    if segments_intersect(segment1, segment2):
        return 0
    # try each of the 4 vertices w/the other segment
    distances = []
    distances.append(point_segment_distance(segment1.p1, segment2))
    distances.append(point_segment_distance(segment1.p2, segment2))
    distances.append(point_segment_distance(segment2.p1, segment1))
    distances.append(point_segment_distance(segment2.p2, segment1))
    return min(distances)


def segments_intersect(segment1, segment2):
    """Check if two line segments in the plane intersect.
    >>> segments_intersect(LineSegment(Point(0,0), Point(1,0)), \
                           LineSegment(Point(0,0), Point(1,0)))
    True
    """
    dx1 = segment1.p2.x - segment1.p1.x
    dy1 = segment1.p2.y - segment1.p2.y
    dx2 = segment2.p2.x - segment2.p1.x
    dy2 = segment2.p2.y - segment2.p1.y
    delta = dx2 * dy1 - dy2 * dx1
    if delta == 0:  # parallel segments
        # TODO: Could be (partially) identical!
        return False
    s = (dx1 * (segment2.p1.y - segment1.p1.y) +
         dy1 * (segment1.p1.x - segment2.p1.x)) / delta
    t = (dx2 * (segment1.p1.y - segment2.p1.y) +
         dy2 * (segment2.p1.x - segment1.p1.x)) / (-delta)
    return (0 <= s <= 1) and (0 <= t <= 1)


def point_segment_distance(point, segment):
    """
    >>> a = LineSegment(Point(1,0), Point(2,0))
    >>> b = LineSegment(Point(2,0), Point(0,2))
    >>> point_segment_distance(Point(0,0), a)
    1.0
    >>> "%0.2f" % point_segment_distance(Point(0,0), b)
    '1.41'
    """
    assert isinstance(point, Point), \
        "point is not of type Point, but of %r" % type(point)
    dx = segment.p2.x - segment.p1.x
    dy = segment.p2.y - segment.p1.y
    if dx == dy == 0:  # the segment's just a point
        return math.hypot(point.x - segment.p1.x, point.y - segment.p1.y)

    if dx == 0:
        if (point.y <= segment.p1.y or point.y <= segment.p2.y) and \
           (point.y >= segment.p2.y or point.y >= segment.p2.y):
            return abs(point.x - segment.p1.x)

    if dy == 0:
        if (point.x <= segment.p1.x or point.x <= segment.p2.x) and \
           (point.x >= segment.p2.x or point.x >= segment.p2.x):
            return abs(point.y - segment.p1.y)

    # Calculate the t that minimizes the distance.
    t = ((point.x - segment.p1.x) * dx + (point.y - segment.p1.y) * dy) / \
        (dx * dx + dy * dy)

    # See if this represents one of the segment's
    # end points or a point in the middle.
    if t < 0:
        dx = point.x - segment.p1.x
        dy = point.y - segment.p1.y
    elif t > 1:
        dx = point.x - segment.p2.x
        dy = point.y - segment.p2.y
    else:
        near_x = segment.p1.x + t * dx
        near_y = segment.p1.y + t * dy
        dx = point.x - near_x
        dy = point.y - near_y

    return math.hypot(dx, dy)
	
	
def perDist(x1,y1, x2,y2, x3,y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    something = px*px + py*py
	
    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = math.sqrt(dx*dx + dy*dy)

    return dist

if __name__ == '__main__':
    import doctest
    doctest.testmod()
