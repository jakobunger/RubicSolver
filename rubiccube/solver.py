import rubiccube as rb
import numpy as np


class Solver():

    def get_edge_list(self, cube: rb):
        list = [cube.top[0, 1][0] + cube.back[2, 1][0],
                cube.top[1, 0][0] + cube.left[0, 1][0],
                cube.top[1, 2][0] + cube.right[0, 1][0],
                cube.top[2, 1][0] + cube.front[0, 1][0],

                cube.back[1, 0][0] + cube.left[1, 0][0],
                cube.back[1, 2][0] + cube.right[1, 2][0],
                cube.front[1, 0][0] + cube.left[1, 2][0],
                cube.front[1, 2][0] + cube.right[1, 0][0],

                cube.bottom[2, 1][0] + cube.back[0, 1][0],
                cube.bottom[1, 0][0] + cube.left[2, 1][0],
                cube.bottom[1, 2][0] + cube.right[2, 1][0],
                cube.bottom[0, 1][0] + cube.front[2, 1][0]]

        for i in range(0, 12):
            list[i] = sorted(list[i])
            if list[i][0] == list[i][1]:
                print("Exc!")

        positions = [[1, 2, 2], [0, 1, 2], [2, 1, 2], [1, 2, 2],
                     [0, 2, 1], [2, 2, 1], [0, 0, 1], [2, 0, 1],
                     [1, 2, 0], [0, 1, 0], [2, 1, 0], [1, 0, 0]]

        res = (list, positions)
        return res

    def step_1(self, cube: rb):
        # require default rotation

        list = self.get_edge_list(cube)

        source = []
        target = []

        print(list)
        for ind in range(0, len(list[0])):
           if list[0][ind][1] == 'w' or list[0][ind][0] == 'w':
                if list[0][ind][1] == 'w':
                    second_color = list[0][ind][0]
                elif list[0][ind][0] == 'w':
                    second_color = list[0][ind][1]
                else:
                    print("Exc")
                    #raise logicexception.LogicException("There should be no white-white edge")
                source.append(list[1][ind])
                if second_color == 'g':
                    target.append([1, 0, 2])
                elif second_color == 'o':
                    target.append([0, 1, 2])
                elif second_color == 'r':
                    target.append([2, 1, 2])
                elif second_color == 'b':
                    target.append([1, 2, 2])
                else:
                    print("Exc")
                    #raise logicexception.LogicException("There are only white edges to green, orange, red, blue")

        print(source)
        print("\n")
        print(target)
        # assure source.len = target.len

        for i in range(0, len(source)):
            s = source[i]
            t = target[i]
            
