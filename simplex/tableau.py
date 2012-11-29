'''
Created on 2012/11/22

@author: SuzukiRyota
'''

class Variable:
    def __init__(self, val, slack, dom=None, dom_type=None):
        self.val = val
        self.slack = bool(slack)
        self.dom = dom
        self.type = dom_type

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

    def __str__(self):
        if self.dom is None:
            return '(%f, %s)' % (self.val, self.slack)
        else:
            return ('(%f %s %f, %s)' %
                    (self.val, self.type, self.dom, self.slack))

    def flip_slack(self):
        self.slack = not self.slack

    def domain_condition(self, arg):
        return self.cond(arg)

    def self_condition(self):
        return self.cond(self.val)

    def satisfy_condition(self):
        if not self.domain_condition(self.val):
            self.val = self.dom

    def get_dom_sub_val(self):
        # if type == '>=': retval > 0 else: retval < 0
        return self.dom - self.val


class RowLine:
    def __init__(self, coef_list):
        self.coef = coef_list

    def __str__(self):
        return 'Row' + str(self.coef)

    def __sub__(self, other):
        return RowLine(map(lambda x, y: x - y, self.coef, other))

    def __mul__(self, const):
        return RowLine(map(lambda x: x * const, self.coef))

    def __rmul__(self, const):
        return self.__mul__(const)

    def __div__(self, const):
        return RowLine(map(lambda x: x / const, self.coef))

    def __getitem__(self, index):
        return self.coef[index]


class Tableau:
    def __init__(self, var, rows):
        self.var = var
        self.rows = rows

    def __str__(self):
        info_var = 'var:['
        for v in self.var:
            info_var += str(v)
            info_var += ', '
        info_var += ']\n'
        info_row = ''
        for r in self.rows:
            info_row += str(r)
            info_row += '\n'
        return info_var + info_row

    def gaussian_elimination(self, ipivot, jpivot):
        # divide pivot coefficient to 1
        self.rows[ipivot] /= self.rows[ipivot][jpivot]
        # sweep out the slack variable
        for i, v in enumerate(self.var):
            if v.slack:
                self.rows[i] -= self.rows[ipivot] * self.rows[i][jpivot]
        # change the new slack variable
        self.rows[jpivot] -= self.rows[ipivot]

    def simplex_method(self):
        # search the slack variable that not satisfies condition
        for i, v in enumerate(self.var):
            if v.slack and not v.self.condition():
                slack_i = i
                slack_diff = v.get_dom_sub_val()
                slack_dom = v.dom
                break
            return 'Satisfiable.'  # all variables satisfy condition
        # search the non-slack variable to satisfy condition
        for i, v in enumerate(self.var):
            coef = self.rows[slack_i][i]  # rows expresses the coefficients
            if not v.slack:  # find a non-slack variable
                if slack_diff > 0:  # increase to minimum
                    if ((coef < 0 and v.val > slack_dom) or
                        (coef > 0 and v.val < slack_dom)):
                        nslack_i = i
                        break
                elif slack_diff < 0:  # decrease to maximum
                    if ((coef < 0 and v.val < slack_dom) or
                        (coef > 0 and v.val > slack_dom)):
                        nslack_i = i
                        break
            return 'Unsatisfiable.'  # not found the non-slack variable
        # exchange the slack variable
        self.var[slack_i].flip_slack()
        self.var[nslack_i].flip_slack()
        # update the value
        self.var[slack_i].satisfy_condition()
        self.var[nslack_i].val += slack_diff / coef
        # gaussian elimination
        self.gaussian_elimination(slack_i, nslack_i)
        # update the variables
        pass


if __name__ == '__main__':
    table = Tableau([Variable(0, False),
                     Variable(0, False),
                     Variable(0, True, 2, '>='),
                     Variable(0, True, 0, '>='),
                     Variable(0, True, 1, '>=')],
                    [RowLine([0, 0, 0, 0, 0]),
                    RowLine([0, 0, 0, 0, 0]),
                    RowLine([1, 1, -1, 0, 0]),
                    RowLine([2, -1, 0, -1, 0]),
                    RowLine([-1, 2, 0, 0, -1])])
    print table
    table.gaussian_elimination(2, 0)
    print table
