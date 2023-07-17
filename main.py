# This is a sample Python script.

import rubiccube.rubiccube as rc
import rubiccube.solver as sol
import numpy as np


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Instantiate cube
    r = rc.Rubiccube()

    # Instantiate solver
    s = sol.Solver()

    # Shuffle cube
    r.shuffle()

    # Solve rubic cube
    s.step_1(r)
    s.step_2(r)
    s.step_3(r)
    s.step_4(r)
    s.step_5(r)
    s.step_6(r)
    s.step_7(r)
    r.print()

