'''
Created on 2012/11/22

@author: SuzukiRyota
'''


class Variable:
    def __init__(self, val, slack, dom=None, dom_type=None):
        self.val = float(val)
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
            return '(%.1f, %s)' % (self.val, self.slack)
        else:
            return ('(%.1f %s %.1f, %s)' %
                    (self.val, self.type, self.dom, self.slack))

    def flip_slack(self):
        self.slack = not self.slack

    def self_condition(self):
        return self.cond(self.val)

    def satisfy_condition(self):
        if not self.self_condition():
            self.val = self.dom

    def get_dom_sub_val(self):
        # if type == '>=': retval > 0 else: retval < 0
        return self.dom - self.val

    def val_not_slack(self):
        return self.val if not self.slack else 0


class RowLine:
    def __init__(self, coef_list):
        self.coef = coef_list

    def __str__(self):
        return 'Row' + str(self.coef)

    def __sub__(self, other):
        return RowLine(map(lambda x, y: x - y, self.coef, other))

    def __mul__(self, const):
        return RowLine(map(lambda x: x * float(const), self.coef))

    def __div__(self, const):
        return RowLine(map(lambda x: x / float(const), self.coef))

    def __getitem__(self, index):
        return self.coef[index]


class Tableau:
    def __init__(self, var, row_list):
        self.var = var
        self.rows = row_list

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
        return info_var + info_row + '\n'

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
        print 'Initial:'
        print self
        print 'Searching the slack variable that not satisfies condition...'
        found = False
        for i, v in enumerate(self.var):
            if v.slack and not v.self_condition():
                slack_i = i
                slack_diff = v.get_dom_sub_val()
                slack_dom = v.dom
                found = True
                print v
                break
        if not found:  # all variables satisfy condition
            print 'Satisfiable.'
            return
        print 'Searching the non-slack variable to satisfy condition...'
        found = False
        for i, v in enumerate(self.var):
            coef = self.rows[slack_i][i]  # expresses the coefficients
            if not v.slack:  # found a non-slack variable
                if slack_diff > 0:  # increase to minimum
                    if ((coef < 0 and v.val > slack_dom) or
                        (coef > 0 and v.val < slack_dom)):
                        nslack_i = i
                        found = True
                        print coef, v
                        break
                elif slack_diff < 0:  # decrease to maximum
                    if ((coef < 0 and v.val < slack_dom) or
                        (coef > 0 and v.val > slack_dom)):
                        nslack_i = i
                        found = True
                        print coef, v
                        break
        if not found:  # the non-slack variable
            print 'Unsatisfiable.'
            return
        print 'Exchange the slack variable.'
        self.var[slack_i].flip_slack()
        self.var[nslack_i].flip_slack()
        print self
        print 'Update the value.'
        self.var[slack_i].satisfy_condition()
        self.var[nslack_i].val += slack_diff / coef
        print self
        print 'Do Gaussian elimination.'
        self.gaussian_elimination(slack_i, nslack_i)
        print self
        print 'Update the slack variables.'
        nslack_vars = [v.val_not_slack() for v in self.var]
        for i, v in enumerate(self.var):
            if v.slack:
                self.var[i].val = reduce(lambda x, y: x + y,
                                         map(lambda x, y: x * y,
                                             nslack_vars, self.rows[i].coef))
        print self
        print 'Iteration.'
        self.simplex_method()
