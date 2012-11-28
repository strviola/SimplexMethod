'''
Created on 2012/11/22

@author: SuzukiRyota
'''

class Variable:
    def __init__(self, val, slack, dom=None, dom_type=None):
        self.val = float(val)
        self.slack = bool(slack)
        self.dom = dom

        # define the domain condition
        if dom is None and dom_type is None:
            # no domain condition (whole area)
            self.cond = lambda dummy_arg: True
        elif dom is not None and dom_type is not None:
            # there is domain condition
            if dom_type == '<=':
                self.cond = lambda x: x <= dom
            elif dom_type == '>=':
                self.cond = lambda x: x >= dom
            else:
                raise TypeError
        else:
            raise TypeError

    def flip_slack(self):
        self.slack = not self.slack

    def domain_condition(self, arg):
        return self.cond(arg)

    def satisfy_condition(self):
        if not self.domain_condition(self.val):
            diff = self.val - self.dom
            self.val = self.dom
            # if type is <= then diff > 0, else diff < 0
            return diff


class RowLine:
    def __init__(self, coef_list):
        self.coef = coef_list

    def calc_template(self, other, op):
        return map(op, self.coef, other)

    def __add__(self, other):
        return self.calc_template(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self.calc_template(other, lambda x, y: x - y)

    def __mul__(self, const):
        return self.calc_template(const, lambda x, y: x * y)

    def __div__(self, const):
        return self.calc_template(const, lambda x, y: x / y)

    def __getitem__(self, index):
        return self.coef[index]


class Tabuleau:
    def __init__(self, var, rows):
        self.var = var
        self.rows = rows

    def gaussian_eliminate(self):
        pass
