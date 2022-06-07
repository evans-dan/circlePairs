#
# circlePairs.py - classify a set of circles into different relationships
#

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
