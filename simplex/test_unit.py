'''
Created on 2012/12/03

@author: SuzukiRyota
'''
import unittest
from tableau import Variable, RowLine, Tableau


class Test(unittest.TestCase):
    def setUp(self):
        # variables
        pre_var = [(0, True), (0, False), (0, False), (0, True), (0, True)]
        self.vars = [Variable(*v) for v in pre_var]
        # row lines
        pre_row = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, -1, 0, 0],
                        [2, -1, 0, -1, 0], [-1, 2, 0, 0, -1]]
        self.rows = [RowLine(r) for r in pre_row]
        # tableau
        self.table = Tableau(self.vars, self.rows)

    def tearDown(self):
        pass

    # tests about operators to help Gaussian elimination
    def test_row_subtraction(self):
        t_sub = self.rows[3] - self.rows[2]
        self.assertListEqual(t_sub.coef, [1, -2, 1, -1, 0])

    def test_row_multiplication(self):
        t_mul = self.rows[4] * 3
        self.assertListEqual(t_mul.coef, [-3, 6, 0, 0, -3])

    def test_row_division(self):
        t_div = self.rows[2] / 5
        self.assertListEqual(t_div.coef, [0.2, 0.2, -0.2, 0, 0])

    def test_getitem(self):
        # originally, this operation should be written self.rows[2].coef[0]
        # RowLine has __getitem__ method, so this abbreviation is able
        self.assertEqual(self.rows[2][0], 1)

    # main test
    def test_gaussian_elimination(self):
        self.table.gaussian_elimination(2, 0)
        coef = [r.coef for r in self.table.rows]
        self.assertListEqual(coef, [[-1, -1, 1, 0, 0], [0, 0, 0, 0, 0],
                             [1, 1, -1, 0, 0], [0, -3, 2, -1, 0],
                             [0, 3, -1, 0, -1]])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
