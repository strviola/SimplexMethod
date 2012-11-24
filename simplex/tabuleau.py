'''
Created on 2012/11/22

@author: SuzukiRyota
'''

class Variable:
    def __init__(self, val, slack, dom=None, dom_type=None):
        self.val = float(val)
        self.slack = bool(slack)

        # define the domain condition
        if dom is None and dom_type is None:
            # no domain condition
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


class RowLine:
    def __init__(self, var, coefficients):
        self.var = var
        self.coef = coefficients

    def __add__(self, other):
        return map(lambda x, y: x + y, self.coef, other.coef)

    def __mul__(self, const):
        return map(lambda x: x * const, self.coef)

    def __getitem__(self, index):
        return self.coef[index]


class Tabuleau:
    def __init__(self, rows):
        self.rows = rows

    def gaussian_eliminate(self):
        pass
