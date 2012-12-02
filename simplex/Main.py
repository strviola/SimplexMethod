'''
Created on 2012/11/22

@author: SuzukiRyota
'''

import curses


def bottom_alert(window, sentence):
    win_bottom = window.getmaxyx()[0] - 1
    window.move(win_bottom, 0)
    window.addstr(sentence)


if __name__ == '__main__':
    try:
        terminate = Exception('Program terminated by quit key.')
        # start curses
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)

        # initialization
        stdscr.addstr(0, 0, 'Simplex Method Program v0.1 by Suzuki Ryota')
        stdscr.addstr(1, 0, "Press 'Q' to quit.")
        stdscr.addstr(2, 0, "Press 'D' key to delete a character.")
        stdscr.refresh()

        # draw the input window
        attr_win = stdscr.subwin(4, 0)
        attr_win.addstr(0, 0, 'Input the number of...')
        for_mes = 'formulas: '
        var_mes = 'variables: '
        attr_win.addstr(1, 0, for_mes)
        attr_win.addstr(2, 0, var_mes)
        # cursor position
        cur_y, cur_x = 1, len(for_mes)
        win_bottom = attr_win.getmaxyx()[0] - 1
        # initialize input environment
        attr_win.move(cur_y, cur_x)
        cursor_on_formula = True
        attr_buf = [''] * 2
        input_nth = 0

        # user input to number of formulas and variables
        while True:
            attr_win.move(cur_y, cur_x)
            c = attr_win.getkey()
            # delete the alert message
            attr_win.move(win_bottom, 0)
            attr_win.deleteln()
            # input condition
            if c in '0123456789':  # digit
                attr_win.move(cur_y, cur_x)
                attr_win.addstr(c)
                attr_buf[input_nth] += c
                cur_x += 1
                attr_win.move(cur_y, cur_x)
            elif c == '\n':  # enter key
                if input_nth == 0:  # move cursor from formula to variable
                    input_nth += 1
                    cur_y, cur_x = 2, len(var_mes)
                else:  # determine the input
                    if (attr_buf[0] == '' or attr_buf[1] == '' or
                        int(attr_buf[0]) == 0 or int(attr_buf[1]) == 0):
                        # no input or number is 0
                        bottom_alert(attr_win, 'The input is not valid.')
                        attr_win.move(cur_y, cur_x)
                    else:
                        break
            elif c == 'D' or c == 'd':  # arrow left key: backspace
                if len(attr_buf[input_nth]) >= 1:
                    attr_win.delch(cur_y, cur_x - 1)
                    attr_buf[input_nth] = attr_buf[input_nth][: -1]
                    cur_x -= 1
                    attr_win.move(cur_y, cur_x)
                else:
                    bottom_alert(attr_win, 'The input is already empty.')
            elif c == 'q':  # quit
                raise terminate
            else:
                bottom_alert(attr_win, 'The input %s is not a digit.' % c)

        # result of each numbers
        for_num = int(attr_buf[0])
        var_num = int(attr_buf[1])
        # change the window
        attr_win.erase()
        form_win = stdscr.subwin(4, 0)
        form_win.addstr(0, 0, 'Input %d formulas with %d variables.' %
                        (for_num, var_num))
        usage_text = 'For example: '
        for i in range(var_num):
            usage_text += '%d ' % i
        usage_text += '>= %d' % var_num
        form_win.addstr(for_num + 2, 0, usage_text)
        # cursor usage
        cur_y = 1
        cur_x = 0
        form_win.move(cur_y, cur_x)
        first_flag = True
        win_bottom = form_win.getmaxyx()[0] - 1
        # remember for max input number
        for_nth = 0  # <= for_num
        var_nth = 0  # var_nth[n] <= var_num
        # buffers
        buf = [''] * for_num
        # user input to formulas
        while True:
            form_win.move(cur_y, cur_x)
            c = form_win.getkey()
            # delete the alert message
            form_win.move(win_bottom, 0)
            form_win.deleteln()
            form_win.move(cur_y, cur_x)
            if c in '0123456789':
                if var_nth <= var_num - 1 or var_nth == var_num + 1:
                    buf[for_nth] += c
                    form_win.addstr(c)
                    cur_x += 1
                    first_flag = False
                else:
                    bottom_alert(form_win, 'Input a sign of inequality')
            elif c == '-':
                if first_flag:
                    form_win.addstr(c)
                    buf[for_nth] += c
                    cur_x += 1
                    first_flag = False
                else:
                    bottom_alert(form_win, 'You cannot input %s to here.' % c)
            elif c == ' ':
                if var_nth <= var_num - 1 and not first_flag:
                    form_win.addstr(c)
                    buf[for_nth] += c
                    var_nth += 1
                    cur_x += 1
                    first_flag = True
                else:
                    bottom_alert(form_win, 'You cannot input space here.')
            elif (c == '<' or c == '>') and first_flag:
                if var_nth == var_num:
                    form_win.addstr(c + "=")
                    buf[for_nth] += c + '= '
                    cur_x += 3
                    var_nth += 1
                    first_flag = False
                else:
                    bottom_alert(form_win, 'You cannot input %s here.' % c)
            elif c == '\n':  # move to next formula
                if for_nth <= for_num - 2:
                    var_nth = 0
                    cur_y += 1
                    cur_x = 0
                    for_nth += 1
                    first_flag = True
                else:
                    break
            elif c == 'd' or c == 'D':
                if len(attr_buf[for_nth]) >= 1:
                    form_win.delch(cur_y, cur_x - 1)
                    if buf[for_nth][-1] == ' ':  # last token is space
                        var_nth -= 1
                        first_flag = True
                    buf[for_nth] = buf[for_nth][: -1]
                    cur_x -= 1
                else:
                    bottom_alert(form_win, 'The input is already empty.')
            elif c == 'q':
                raise terminate
            else:
                bottom_alert(form_win, 'You cannot input %s to here.' % c)

        exit_mes = 'Processing...'

    except Exception, e:
        exit_mes = '%s, %s' % (type(e), e)

    finally:
        # return to normal window
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()

        # convert the input to simplex tableau
        print exit_mes
        print buf
