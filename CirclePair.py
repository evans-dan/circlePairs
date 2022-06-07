#
# CirclePair class - a pair of circles defined by the x,y coordinates of their
#   centres, and their radius.
#

import numpy as np
from math import acos

class CirclePair():
    """
    Base class of a pair of circles defined by the coordinates of their centres, and their radii
    """

    def __init__(self, coords):
        """
        Creating a new pair of circles
        Input: six element list of coordinates in the following order:
            Ax, Ay, Ar, Bx, By, Br, with Nx and Ny being cartesian coordinates, and r the radius
        Output: none; modifies local attributes
        """
        self.Ax = 0 # circle A x coord
        self.Ay = 0 # circle A y coord
        self.Ar = 0 # circle A radius
        self.Bx = 0 # circle B x coord
        self.By = 0 # circle B y coord
        self.Br = 0 # circle B radius
        self.distance = 0 # distance between centres
        self.overlap = 0 # area of overlap
        self.AA = 0 # area of circle A
        self.BA = 0 # area of circle B
        self.pair_type = None # type of overlap: identical, concentric, disjoint-inside, disjoint-outside, nonoverlapping

        if len(coords) != 6:
            raise Exception(f"Error: requires exactly six int/float arguments; received {len(coords)}")

        for i in coords:
                if (type(i) is not int) and (type(i) is not float):
                    raise Exception(f"Error: requires exactly six int/float arguments, received type {type(i)}")

        if coords[2] <= 0 or coords[5] <= 0:
            raise Exception(f"Error: radii must be nonnegative numbers; received radii: {coords[2]}, {coords[5]}")

        [self.Ax, self.Ay, self.Ar, self.Bx, self.By, self.Br] = list(map(float, coords))
        self.AA = self.Ar**2 * np.pi
        self.BA = self.Br**2 * np.pi

        self._calculate_distance()

    def _calculate_distance(self):
        """
        Calculate the distance between the two circle centres
        Inputs: none.
        Outputs: none; modifies local attributes.
        """
        self.distance = np.sqrt((self.Ax - self.Bx)**2 + (self.Ay - self.By)**2)

    def _calculate_overlap(self):
        """
        Calculates the area of overlap between the two circles, None if they do not overlap.
        Calculation taken from: https://iliauk.wordpress.com/2016/03/22/circle-overlaps-with-numpy/
        Inputs: none.
        Outputs: none; modifies local attributes.
        """

        try:

            a = (self.Ar**2)*acos(((self.distance**2)+(self.Ar**2)-(self.Br**2))/(2*self.distance*self.Ar))
            b = (self.Br**2)*acos(((self.distance**2)+(self.Br**2)-(self.Ar**2))/(2*self.distance*self.Br))
            c = (0.5*((-self.distance+self.Ar+self.Br)*(self.distance+self.Ar-self.Br)*(self.distance-self.Ar+self.Br)*(self.distance+self.Ar+self.Br))**0.5)

            area = a + b - c

        except ValueError: # the circles don't overlap, or one is entirely inside the other

            if self.distance < max(self.Ar, self.Br): # one inside the other, so overlap is the smaller circle's area

                area = min(self.Ar, self.Br)**2 * np.pi

            else: # circles are separate (or tangential)

                area = 0

        self.overlap = area

    def classify_pair(self):
        """
        Classifies the relationship between the two circles. Note: two unit-radius circles with centres two units apart
            intersect at one point, and therefore do not overlap.
        Identical: same centres, same radii
        Concentric: same centres, different radii
        Disjoint-inside: different centres, one completely inside the other (implies different radii)
        Disjoint-outside: different centres, area of overlap different from area of A or B
        Nonoverlapping: different centers, area of overlap is 0
        """
        if self.Ax == self.Bx and self.Ay == self.By: # same centre, so either identical or concentric circles

            if self.Ar == self.Br: # all characteristics are the same
                self.pair_type = 'Identical'
            else:
                self.pair_type = 'Concentric'

        else: # different centres, so check overlap amount

            self._calculate_overlap()

            if self.overlap != 0: # one of the disjoints
                if self.overlap == self.AA or self.overlap == self.BA: # one smaller circle entirely within the other, but not Concentric
                    self.pair_type = 'Disjoint-inside'
                else: # overlapping, with each circle having area not included in the other
                    self.pair_type = 'Disjoint-outside'
            else: # only one type left
                self.pair_type = 'Nonoverlapping'

    def __str__(self):
        return f"CirclePair A x,y={self.Ax},{self.Ay} r={self.Ar} B x,y={self.Bx},{self.By} r={self.Br} distance={self.distance}"

import unittest

class Test_CirclePair(unittest.TestCase):

    def test_validate_CirclePair_arglen(self):
        """
        Ensure the right number of values are passed in
        """
        test_list = [
            [],
            [1],
            [1,2],
            [1,2,3],
            [1,2,3,4],
            [1,2,3,4,5],
            [1,2,3,4,5,6],
            [1,2,3,4,5,6,7],
            [8,7,6,5,4,3,2,1]
        ]

        for t in test_list:
            if len(t) != 6:
                self.assertRaises(Exception, CirclePair, t)

    def test_validate_CirclePair_argtype(self):
        """
        ensure invalid types throw an Exception
        """
        test_list = [
            [1,2,'test string',4,5,6], # no strings
            [True, False, 3, 4.0, 5, sum], # no boolean values or functions
            [-1, -1, -1, -1, -1, 0] # radii must be > 0
        ]
        for t in test_list:
            self.assertRaises(Exception, CirclePair, t)

    def test_validate_pair_types(self):
        """
        One of each type of circle pair
        """
        test_list = [
            [0, 1, 1, 0, 1, 1], # Identical
            [3.21, 5.67, 1, 3.21, 5.67, 3], # concentric
            [2, 2, 5, 1, 2, 1], # disjoint-inside
            [2, 2, 3.1, 4, 4, 3.1], # disjoint-outside
            [2, 3, 4, -6, -6, 2], # nonoverlapping
            [0, 0, 1, 2, 0, 1] # nonoverlapping but intersecting
        ]
        answer_list = [
            'Identical',
            'Concentric',
            'Disjoint-inside',
            'Disjoint-outside',
            'Nonoverlapping',
            'Nonoverlapping'
        ]

        for i in range(len(test_list)):
            circpair = CirclePair(test_list[i])
            circpair.classify_pair()
            answer_type = answer_list[i]
            pairtype = circpair.pair_type
            self.assertEqual(pairtype, answer_type)

if __name__ == '__main__':
    unittest.main()
