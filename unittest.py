"""CSC148 Assignment1: Treasure Hunt


=== Module description ===
This module contains sample tests for Assignment 1

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.
Please note no unit tests have been provided for TreasureHunt
(and none will be provided until the assignment is due).
"""

import unittest


from container import Container, PriorityQueue
from grid import Grid, Node
from treasurehunt import TreasureHunt


class Helper:
    """
    The Helper class contains helper functions needed for testing
    """
    @classmethod
    def shorter(cls, a, b):
        return len(a) < len(b)


class TestPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.queue = PriorityQueue(Helper.shorter)
        self.queue.add('fred')
        self.queue.add('arju')
        self.queue.add('monalisa')
        self.queue.add('hat')

    def test_pq_add(self):
        actual = self.queue._queue
        expected = ['monalisa', 'arju', 'fred', 'hat']
        msg = "We expected {}, but found {}".format(str(expected), str(actual))
        self.assertEqual(actual, expected, msg)

    def test_pq_remove(self):
        pq = self.queue._queue
        actual = self.queue.remove()
        expected = 'hat'
        msg = "Applied remove() to {}, expected {}, actual {}".format(pq, expected, actual)
        self.assertEqual(actual, expected, msg)


class TestNode(unittest.TestCase):

    def setUp(self):
        self.n1 = Node(True, 1, 2)
        self.n2 = Node(True, 2, 2)
        self.n3 = Node(True, 2, 2)

    def test_node_str(self):
        actual = str(self.n1)
        expected = "."
        msg = "Navigable node(1, 2), expected: {}, got {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_node_equality(self):
        actual = self.n2 == self.n3
        msg = "Nodes (True, 2, 2) and (True, 2, 2) must be equal"
        self.assertTrue(actual, msg)


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.data = ["..+..++", "++.B..+", ".....++", "++.....", ".T....+"]
        self.grid = Grid("", self.data)

    def test_grid_width(self):
        actual = self.grid.width
        expected = 7
        msg = "Grid " + str(self.data) + ": expected width {}, got {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_grid_height(self):
        actual = self.grid.height
        expected = 5
        msg = "Grid " + str(self.data) + ": expected height {}, got {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_grid_node(self):
        actual = self.grid.map[6][4]
        expected = Node(False, 6, 4)
        msg = "Expected non-navigable node (4, 6), got {}".format(actual)
        self.assertEqual(actual, expected, msg)

    def test_grid_boat(self):
        actual = self.grid.boat
        expected = Node(True, 3, 1)
        msg = "Expected boat in (3, 1), got {}".format(actual)
        self.assertEqual(actual, expected, msg)

    def test_grid_path(self):
        boat = self.grid.boat
        treasure = self.grid.treasure
        self.grid.find_path(boat, treasure)
        actual = len(self.grid.retrace_path(boat, treasure))
        expected = 4
        msg = "Expected path length {}, got {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)
        
if __name__ == '__main__':
    unittest.main(exit=False)