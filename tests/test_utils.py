__author__ = "Jerome Thai"
__email__ = "jerome.thai@berkeley.edu"

import unittest
from utils import doIntersect, isInside, isInsideBox, areInside


class TestUtils(unittest.TestCase):


    def test_dointersect(self):
        p1, q1, p2, q2 = [1,1], [10,1], [1,2], [10,2]
        self.assertTrue(doIntersect(p1, q1, p2, q2) is False)
        p1, q1, p2, q2 = [10,0], [0,10], [0,0], [10,10]
        self.assertTrue(doIntersect(p1, q1, p2, q2) is True)
        p1, q1, p2, q2 = [-5,-5], [0,0], [1,1], [10,10]
        self.assertTrue(doIntersect(p1, q1, p2, q2) is False)


    def test_isInside(self):
        polygon1 = [[0,0], [10,0], [10,10], [0,10]]
        n = len(polygon1)
        p = [20,20]
        self.assertTrue(isInside(polygon1, n, p) is False)

        p = [5,5]
        self.assertTrue(isInside(polygon1, n, p) is True)

        polygon2 = [[0,0], [5,5], [5,0]]
        p = [3,3]
        n = len(polygon2)
        self.assertTrue(isInside(polygon2, n, p) is True)

        p = [5,1]
        self.assertTrue(isInside(polygon2, n, p) is True)

        p = [8,1]
        self.assertTrue(isInside(polygon2, n, p) is False)

        polygon3 =  [[0, 0], [10, 0], [10, 10], [0, 10]];
        p = [-1,10]
        n = len(polygon3)
        self.assertTrue(isInside(polygon3, n, p) is False)


    def test_isInsideBox(self):
        box1 = [[0,0],[10,10]]
        box2 = [[10,10],[0,0]]
        box3 = [[0,10],[10,0]]
        box4 = [[10,0],[0,10]]
        p1, p2, p3 = [0,0], [5,5], [5, 10.1]
        self.assertTrue((isInsideBox(box1, p1) and isInsideBox(box1, p2)) is True)
        self.assertTrue((isInsideBox(box2, p1) and isInsideBox(box2, p2)) is True)
        self.assertTrue((isInsideBox(box3, p1) and isInsideBox(box3, p2)) is True)
        self.assertTrue((isInsideBox(box4, p1) and isInsideBox(box4, p2)) is True) 

        self.assertTrue(isInsideBox(box1, p3) is False)
        self.assertTrue(isInsideBox(box2, p3) is False)
        self.assertTrue(isInsideBox(box3, p3) is False)
        self.assertTrue(isInsideBox(box4, p3) is False)


    def test_areInside(self):
        polygon1 = [[0,0], [5,5], [5,0]]
        n = len(polygon1)
        ps = [[3,3], [5,1], [8,1]]
        self.assertTrue(areInside(polygon1, n, ps) == [1,1,0])


if __name__ == '__main__':
    unittest.main()