'''
Created on 2012/11/22

@author: SuzukiRyota
'''

import curses

if __name__ == '__main__':
    try:
        # start curses
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)

        # initialization
        stdscr.addstr(0, 0, 'Simplex Method Program v0.1 by Suzuki Ryota')
        stdscr.addstr(1, 0, "Press 'q' to quit.")
        stdscr.refresh()

        # draw the input window
        attr_win = stdscr.subwin(3, 0)
        attr_win.addstr(0, 0, 'Input the number of...')
        for_mes = 'formulas: '
        var_mes = 'variables: '
        attr_win.addstr(1, 0, for_mes)
        attr_win.addstr(2, 0, var_mes)
        attr_win.addstr(4, 0, 'Use W, S keys as arrow keys to move.')
        attr_win.addstr(5, 0, 'Press A key to delete a character.')
        # remember cursor
        for_cur_y, for_cur_x = 1, len(for_mes)
        var_cur_y, var_cur_x = 2, len(var_mes)
        win_bottom, win_right = attr_win.getmaxyx()
        win_bottom -= 1
        # initialize input environment
        attr_win.move(for_cur_y, for_cur_x)
        cursor_on_formula = True
        for_buf = ''
        var_buf = ''

        # user input to number of formulas and variables
        while True:
            c = attr_win.getkey()
            # delete the alert message
            attr_win.move(win_bottom, 0)
            attr_win.deleteln()
            # input condition
            if c in '0123456789':  # digit
                if cursor_on_formula:
                    attr_win.move(for_cur_y, for_cur_x)
                    attr_win.addstr(c)
                    for_buf += c
                    for_cur_x += 1
                    attr_win.move(for_cur_y, for_cur_x)
                else:
                    attr_win.move(var_cur_y, var_cur_x)
                    attr_win.addstr(c)
                    var_buf += c
                    var_cur_x += 1
                    attr_win.move(var_cur_y, var_cur_x)
            elif c == 'S' or c == 's' or c == '\n':
                # arrow down key or enter key
                if cursor_on_formula:  # move cursor from formula to variable
                    cursor_on_formula = False
                    attr_win.move(var_cur_y, var_cur_x)
                else:  # determine the input
                    if (for_buf == '' or var_buf == '' or
                        int(for_buf) == 0 or int(var_buf) == 0):
                        # no input or number is 0
                        attr_win.move(win_bottom, 0)
                        attr_win.addstr('The input is not valid.')
                        cursor_on_formula = True
                        attr_win.move(for_cur_y, for_cur_x)
                    else: break
            elif c == 'W' or c == 'w':
                # arrow up key: move cursor from variable to formula
                if not cursor_on_formula:
                    cursor_on_formula = True
                    attr_win.move(for_cur_y, for_cur_x)
            elif c == 'A' or c == 'a':  # arrow left key: backspace
                if cursor_on_formula:
                    if len(for_buf) >= 1:
                        attr_win.delch(for_cur_y, for_cur_x - 1)
                        for_buf = for_buf[0: len(for_buf) - 1]
                        for_cur_x -= 1
                        attr_win.move(for_cur_y, for_cur_x)
                else:
                    if len(for_buf) >= 1:
                        attr_win.delch(var_cur_y, var_cur_x - 1)
                        var_buf = var_buf[0: len(var_buf) - 1]
                        var_cur_x -= 1
                        attr_win.move(var_cur_y, var_cur_x)
            elif c == 'q':  # quit
                raise Exception('Exit by quit key.')
            else:
                attr_win.move(win_bottom, 0)
                attr_win.addstr('The input %s is not a digit.' % c)

        # result of each numbers
        for_num = int(for_buf)
        var_num = int(var_buf)
        # change the window
        attr_win.erase()
        form_win = stdscr.subwin(3, 0)
        form_win.addstr(0, 0, 'Input %d formulas with %d variables.' %
                        (for_num, var_num))
        usage_text = 'For example: '
        for i in range(var_num):
            usage_text += '%d ' % i
        usage_text += '>= %d' % var_num
        form_win.addstr(for_num + 2, 0, usage_text)
        # user input to formulas
        while True:
            c = form_win.getkey()
            if c == 'q': break

        exit_mes = 'Program terminated successfully.'

    except Exception, e:
        exit_mes = '%s, %s' % (type(e), e)

    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        print exit_mes
