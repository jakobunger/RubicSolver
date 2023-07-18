# This is a sample Python script.

import rubiccube.rubiccube as rc
import rubiccube.solver as sol
import time
import numpy as np


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Instantiate cube
    r = rc.Rubiccube()

    # Instantiate solver
    s = sol.Solver()

    # Shuffle cube
    r.shuffle()

    # Initial config
    print("Initial cube state:\n")
    r.print()

    # Solve rubic cube
    r.start_logging_moves()
    start_time = time.time()
    s.step_1(r) # white cross
    s.step_2(r) # complete white side (position + alignment)
    s.step_3(r) # complete mid-level edges
    s.step_4(r) # yellow cross
    s.step_5(r) # positioning of top-level edges
    s.step_6(r) # positioning of top-level corners
    s.step_7(r) # alignment of top-level corners
    print("\n\n\nFinal cube state:\n")
    r.print()

    print("\n\n\nMoves:\n")
    moves = r.get_moves_history()
    print("Number of moves: " + str(len(moves)) )
    print( moves )
    print("\n")
    print("Processing time:  %s seconds" % (time.time() - start_time))
    r.delete_move_history()

