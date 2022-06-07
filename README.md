circlePairs - a class to categorize pairs of circles

# Overview

This includes a class called CirclePairs that will, when given a list of six numbers, classify the pair into one of several relationships. The numbers are:
Ax: the x coordinate of circle A's centre
Ay: the y coordinate of circle A's centre
Ar: the radius of circle B
Bx: the x coordinate of circle B's centre
By: the y coordinate of circle B's centre
Br: the radius of circle B

The possible relationships are:
* ***Identical***: The pairs have the same centre and radius
* ***Concentric***: The pairs have the same centre, different radii
* ***Disjoint-inner***: The pairs have different centres, different radii, but one circle is entirely within the other
* ***Disjoint-outer***: The two circles overlap, but each covers area not in the other
* ***Nonoverlapping***: The two circles do not cover any common area

Note: For this exercise, _overlap_ means there is a nonzero amount of area bounded by the circumference of both circles. This means two circles who share a single point (e.g. `CirclePair([0,0,1,0,2,1])`) _do not overlap_ as points do not have area.

A small amount of testing is done to ensure the list used to initialize the CirclePair is sane: some type checking, and positive radii.

# Usage example (see circlePairs.py):
```
from CirclePair import CirclePair
test_list = [
  [0, 1, 1, 0, 1, 1], # Identical
  [1, 1, 1, 1, 1, 3], # concentric
  [2, 2, 5, 1, 2, 1], # disjoint-inside
  [2, 2, 3, 4, 4, 3], # disjoint-outside
  [2, 3, 4, -6, -6, 2] # nonoverlapping
]

for pair_coords in test_list:

    one_pair = CirclePair(pair_coords)
    one_pair.classify_pair()
    print(one_pair.pair_type)
```
