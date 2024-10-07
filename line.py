import math
import numpy as np
import unittest

class Line:
    def __init__(self, p1, p2):
        self.l = ((p2[0] - p1[0])**2) + ((p2[1] - p1[1])**2)
        self.ang = (math.atan2(p2[1]-p1[1], p2[0]- p1[0])  *180/math.pi)%180
        self.p1 = p1
        self.p2 = p2
        self.mid = [int((p1[i]+p2[i])/2) for i in range(2)]
        
    def __lt__(self, other):
        return self.l < other.l
    
    def __str__(self):
        return str(self.p1) + " " + str(self.p2)
    def __eq__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return all(self.p1 == other.p1) and all(self.p2 == other.p2)


    # returns the lowest point on the y axis
    def get_lowest_pos(self) -> int:
        return max(self.p1[1], self.p2[1])

    # TODO verify
    def low_point(self):
        return self.p1 if self.p1[1] > self.p2[1] else self.p2

    # TODO verify
    def high_point(self):
        return self.p1 if self.p1[1] < self.p2[1] else self.p2

class Quad:
    def __init__(self, l1: Line, l2: Line):
        self.l1 = l1
        self.l2 = l2

        test1 = Line(l1.p1, l2.p1)
        test2 = Line(l1.p1, l2.p2)

        if test1.l < test2.l:
            temp = Line(l1.p2, l2.p2)
            self.mid = Line(test1.mid, temp.mid)
        else:
            temp = Line(l1.p2, l2.p1)
            self.mid = Line(test2.mid, temp.mid)

class TestLine(unittest.TestCase):
    def setUp(self):
        self.l1 = Line([0, 0], [100, 100])

    def test_line_ang(self):
        self.assertEqual(self.l1.ang, 45)

    def test_line_mid(self):
        self.assertTrue(self.l1.mid == [50, 50])

class TestQuad(unittest.TestCase):
    def setUp(self):
        self.l1: Line = Line([0 , 0], [0, 10])
        self.l2: Line = Line([10, 0], [10, 10])
    " Check that the angle is the average of the other two angles"
    def test_quad_mid_angle(self):
        # this generates a ton of lines and checks them
        for i in range(1, 100, 10):
            line1 = Line([i , 0], [0, 10])
            line2 = Line([10, 10], [10, i])
            quad = Quad(self.l1, self.l2)
            self.assertEqual(quad.mid.ang, float(self.l1.ang + self.l2.ang)/2)

    def test_quad_mid_points(self):
        quad = Quad(self.l1, self.l2)
        self.assertTrue(all(quad.mid.p1 == np.divide(np.add(self.l1.p1, self.l2.p1), 2)))
        self.assertTrue(all(quad.mid.p2 == np.divide(np.add(self.l1.p2, self.l2.p2), 2)))

