import unittest

from campus_demo import GATE, GOAL, START, WALLS, astar, decision, posterior


class CourtyardTests(unittest.TestCase):
    def test_sensor(self):
        self.assertAlmostEqual(posterior(True), 24 / 38)
        self.assertAlmostEqual(posterior(False), 6 / 62)

    def test_routes(self):
        for alert, steps, expected_cost in [(False, 4, 4 + 4 * 6/62), (True, 6, 6)]:
            with self.subTest(alert=alert):
                path, cost = astar(posterior(alert))
                self.assertEqual((path[0], path[-1]), (START, GOAL))
                self.assertEqual(len(path) - 1, steps)
                self.assertAlmostEqual(cost, expected_cost)
                self.assertEqual(GATE in path, not alert)
                for a, b in zip(path, path[1:]):
                    self.assertNotIn(b, WALLS)
                    self.assertEqual(abs(a[0] - b[0]) + abs(a[1] - b[1]), 1)

    def test_policy(self):
        self.assertEqual(decision(posterior(True), True)[2], "WAIT")
        self.assertEqual(decision(posterior(False), True)[2], "MOVE")
        self.assertEqual(decision(posterior(True), False)[2], "MOVE")


if __name__ == "__main__":
    unittest.main()

