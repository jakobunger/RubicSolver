import numpy
import numpy as np
import copy
import random


class Rubiccube():

    log_history = list()
    logging = 0

    def __init__(self):
        # Initialize rubic cube
        self.top = np.array([['w', 'w', 'w'], ['w', 'w', 'w'], ['w', 'w', 'w']], dtype=str)
        self.left = np.array([['o', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']], dtype=str)
        self.right = np.array([['r', 'r', 'r'], ['r', 'r', 'r'], ['r', 'r', 'r']], dtype=str)
        self.bottom = np.array([['y', 'y', 'y'], ['y', 'y', 'y'], ['y', 'y', 'y']], dtype=str)
        self.back = np.array([['b', 'b', 'b'], ['b', 'b', 'b'], ['b', 'b', 'b']], dtype=str)
        self.front = np.array([['g', 'g', 'g'], ['g', 'g', 'g'], ['g', 'g', 'g']], dtype=str)

    def print(self):
        print("front")
        print(self.front)
        print("right")
        print(self.right)
        print("back")
        print(self.back)
        print("left")
        print(self.left)
        print("top")
        print(self.top)
        print("bottom")
        print(self.bottom)

    # Left side rotation clockwise and counter-clockwise (inverse)
    def rotleft(self, inverse=0):
        if inverse == 0:
            tempcol = copy.copy(self.top[:, 0])
            self.top[:, 0] = self.back[:, 0]
            self.back[:, 0] = self.bottom[:, 0]
            self.bottom[:, 0] = self.front[:, 0]
            self.front[:, 0] = tempcol
            self.left = numpy.rot90(self.left, k=3)  # clockwise
        if inverse == 1:
            tempcol = copy.copy(self.top[:, 0])
            self.top[:, 0] = self.front[:, 0]
            self.front[:, 0] = self.bottom[:, 0]
            self.bottom[:, 0] = self.back[:, 0]
            self.back[:, 0] = tempcol
            self.left = np.rot90(self.left, k=1)  # counter-clockwise
        move = "rotleft("+str(inverse)+")"
        self.log_history.append(move)
        return move

    # Right side rotation clockwise and counter-clockwise (inverse)
    def rotright(self, inverse=0):
        if inverse == 0:
            tempcol = copy.copy(self.top[:, 2])
            self.top[:, 2] = self.front[:, 2]
            self.front[:, 2] = self.bottom[:, 2]
            self.bottom[:, 2] = self.back[:, 2]
            self.back[:, 2] = tempcol
            self.right = np.rot90(self.right, k=3)  # clockwise
        if inverse == 1:
            tempcol = copy.copy(self.top[:, 2])
            self.top[:, 2] = self.back[:, 2]
            self.back[:, 2] = self.bottom[:, 2]
            self.bottom[:, 2] = self.front[:, 2]
            self.front[:, 2] = tempcol
            self.right = np.rot90(self.right, k=1)  # counter-clockwise
        move = "rotright(" + str(inverse) + ")"
        self.log_history.append(move)
        return

    # Upper side rotation clockwise and counter-clockwise (inverse)
    def rotup(self, inverse=0):
        if inverse == 0:
            tempcol = copy.copy(self.front[0, :])
            self.front[0, :] = self.right[0, :]
            self.right[0, :] = (np.flip(self.back[2, :]))
            self.back[2, :] = (np.flip(self.left[0, :]))
            self.left[0, :] = tempcol
            self.top = np.rot90(self.top, k=3)  # clockwise
        if inverse == 1:
            tempcol = copy.copy(self.front[0, :])
            self.front[0, :] = self.left[0, :]
            self.left[0, :] = (np.flip(self.back[2, :]))
            self.back[2, :] = (np.flip(self.right[0, :]))
            self.right[0, :] = tempcol
            self.top = numpy.rot90(self.top, k=1)  # counter-clockwise
        move = "rotup(" + str(inverse) + ")"
        self.log_history.append("rotup(" + str(inverse) + ")")
        return move

    # ^Lower side rotation clockwise and counter-clockwise (inverse)
    def rotdown(self, inverse=0):
        if inverse == 0:
            tempcol = copy.copy(self.front[2, :])
            self.front[2, :] = self.left[2, :]
            self.left[2, :] = (np.flip(self.back[0, :]))
            self.back[0, :] = (np.flip(self.right[2, :]))
            self.right[2, :] = tempcol
            self.bottom = np.rot90(self.bottom, k=3)  # clockwise
        if inverse == 1:
            tempcol = copy.copy(self.front[2, :])
            self.front[2, :] = self.right[2, :]
            self.right[2, :] = (np.flip(self.back[0, :]))
            self.back[0, :] = (np.flip(self.left[2, :]))
            self.left[2, :] = tempcol
            self.bottom = numpy.rot90(self.bottom, k=1)  # counter-clockwise
        move = "rotdown(" + str(inverse) + ")"
        self.log_history.append(move)
        return move

    # Front side rotation clockwise and counter-clockwise (inverse)
    def rotfront(self, inverse=0):
        if inverse == 0:
            tempcol = copy.copy(self.top[2, :])
            self.top[2, :] = np.flip(self.left[:, 2])
            self.left[:, 2] = self.bottom[0, :]
            self.bottom[0, :] = np.flip(self.right[:, 0])
            self.right[:, 0] = tempcol
            self.front = np.rot90(self.front, k=3)  # clockwise
        if inverse == 1:
            tempcol = copy.copy(self.top[2, :])
            self.top[2, :] = (self.right[:, 0])
            self.right[:, 0] = np.flip(self.bottom[0, :])
            self.bottom[0, :] = (self.left[:, 2])
            self.left[:, 2] = np.flip(tempcol)
            self.front = np.rot90(self.front, k=1)  # counter-clockwise
        move = "rotfront(" + str(inverse) + ")"
        self.log_history.append(move)
        return move

    # Rotate the entire cube downwards clockwise and upwards (inverse)
    def rot_cube_down_cw(self, inverse= 0):
        if inverse == 0:
            self.left = np.rot90(self.left, k=3)  # clockwise
            self.right = np.rot90(self.right, k=1)  # counter-clockwise
            tempface = self.top
            self.top = self.back
            self.back = self.bottom
            self.bottom = self.front
            self.front = tempface
        if inverse == 1:
            self.left = np.rot90(self.left, k=1)  # counter-clockwise
            self.right = np.rot90(self.right, k=3)  # clockwise
            tempface = copy.copy(self.top)
            self.top = self.front
            self.front = self.bottom
            self.bottom = self.back
            self.back = tempface
        move = "rot_cube_up(" + str(inverse) + ")"
        self.log_history.append(move)
        return move

    # Rotate the entire cube clockwise and counter-clockwise (inverse)
    def rot_cube_left_cw(self, inverse=0):
        if inverse == 0:
            self.top = np.rot90(self.top, k=3)  # clockwise
            self.bottom = np.rot90(self.bottom, k=1)  # counter-clockwise
            tempface = copy.copy(self.left)
            self.left = self.front
            self.front = self.right
            self.right = np.fliplr(np.flipud(self.back))
            self.back = np.fliplr(np.flipud(tempface))
        if inverse == 1:
            self.top = np.rot90(self.top, k=1)  # counter-clockwise
            self.bottom = np.rot90(self.bottom, k=3)  # clockwise
            tempface = copy.copy(self.left)
            self.left = np.fliplr(np.flipud(self.back))
            self.back = np.fliplr(np.flipud(self.right))
            self.right = self.front
            self.front = tempface
        move = "rot_cube_left(" + str(inverse) + ")"
        self.log_history.append(move)
        return move

    def shuffle(self):
        no_of_moves = random.randint(30, 100)
        for i in range(1, no_of_moves):
            move = random.randint(0, 4)
            inv = random.randint(0, 1)
            move_history = []
            if move == 0:
                move_history.append(self.rotfront(inv))
            elif move == 1:
                move_history.append(self.rotdown(inv))
            elif move == 2:
                move_history.append(self.rotright(inv))
            elif move == 3:
                move_history.append(self.rotup(inv))
            elif move == 4:
                move_history.append(self.rotleft(inv))

    # white center points upwards, green is the front surface
    def normalized_rotation(self):
        if not self.top[1, 1][0] == 'w':
            if self.right[1, 1][0] == 'w':
                self.rot_cube_left_cw(1)
            elif self.left[1, 1][0] == 'w':
                self.rot_cube_left_cw()

        # move white center to the top
        for i in range(0, 4):
            self.rot_cube_down_cw()
            if self.top[1, 1][0] == 'w':
                break

        # move green to the front face
        for i in range(0, 4):
            if self.front[1, 1][0] == 'g':
                break
            self.rot_cube_left_cw()

    def start_logging_moves(self):
        logging = 1

    def stop_logging_moves(self):
        logging = 0

    def delete_move_history(self):
        logging = 0

    def get_moves_history(self):
        return self.log_history
