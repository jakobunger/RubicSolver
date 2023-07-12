# This is a sample Python script.

import rubiccube.rubiccube as rc
import rubiccube.solver as sol
import numpy as np

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    r = rc.Rubiccube()
    s = sol.Solver()
    r.shuffle()

    #r.rotfront(0)
    r.rotdown(1)
    #r.rotfront(1)
    r.rotleft(0)
    r.rotright()
    r.rotup()
    r.rotdown()
    r.rotright()
    r.rotfront(1)

    #s.check_edge_list(r)
    #s.check_corner_list(r)
    s.step_1(r)
    s.step_2(r)
    #r.print()
    #r.shuffle()
    #s.check_edge_list(r)
#    r.print()
#    r.rot_cube_left_cw()
#    r.print()
#right, left, up, down, front

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
