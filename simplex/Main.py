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
        stdscr.addstr(0, 0, 'Simplex Method Program v0.1 by Suzuki Ryota',
                      curses.COLOR_GREEN)
    
        # input number of formulas and variables
        attr_win = stdscr.subwin(2, 0)
        attr_win.addstr(0, 0, 'Input the number of...')
        for_mes = 'formulas: '
        var_mes = 'variables: '
        attr_win.addstr(1, 0, for_mes)
        attr_win.addstr(2, 0, var_mes)
        cur_y, cur_x = 1, len(for_mes)
        attr_win.move(cur_y, cur_x)
        
        while True:
            c = stdscr.getkey()
            stdscr.addstr(c)
            if c == 'q':
                exit_mes = 'Program successfully exit.'
                break

    except Exception, e:
        exit_mes = '%s, %s' % (type(e), e)

    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        print exit_mes
