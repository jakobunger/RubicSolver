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

        positions = [[1, 2, 2], [0, 1, 2], [2, 1, 2], [1, 0, 2],
                     [0, 2, 1], [2, 2, 1], [0, 0, 1], [2, 0, 1],
                     [1, 2, 0], [0, 1, 0], [2, 1, 0], [1, 0, 0]]

        res = (list, positions)
        return res

    def check_edge_list(self, cube: rb):
        listcheck = self.get_edge_list(cube)[0]
        print(listcheck)
        ground_truth = sorted([['g', 'o'], ['b', 'w'], ['b', 'y'], ['g', 'r'], ['b', 'o'], ['r', 'y'], ['g', 'w'], ['b', 'r'], ['o', 'y'], ['r', 'w'], ['g', 'y'], ['o', 'w']])
        listcheck = sorted(listcheck)
        if not listcheck == ground_truth:
            print(" INCONSISTENCY!! ")

    def get_edge(self, cube: rb, color1, color2):
        list = self.get_edge_list(cube)
        search_for_colorpair = sorted([color1, color2])
        for i in range(0, len(list[0])):
            if list[0][i] == search_for_colorpair:
                return list[1][i]
        # should not end here, edge not found
        return [-1, -1, -1]

    def step_1(self, cube: rb):
        # require default rotation

        list = self.get_edge_list(cube)

        #source = []
        target = []

        white_edge_list = []

        for ind in range(0, len(list[0])):
           if list[0][ind][1] == 'w' or list[0][ind][0] == 'w':
                if list[0][ind][1] == 'w':
                    second_color = list[0][ind][0]
                elif list[0][ind][0] == 'w':
                    second_color = list[0][ind][1]
                else:
                    print("Exc")
                    #raise logicexception.LogicException("There should be no white-white edge")

                white_edge_list.append([list[0][ind][0], 'w'])

                #source.append(list[1][ind])
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

        print("\n")
        print(target)
        # assure source.len = target.len

        for i in range(0, len(white_edge_list)):
            s = self.get_edge(cube, white_edge_list[i][0], white_edge_list[i][1])
            t = target[i]

            # move all sources to intermediate position [1,0,0]

            # source in row 0
            if s == [0, 1, 0]:
                cube.rotdown()
                cube.print()
            if s == [1, 2, 0]:
                cube.rotdown()
                cube.rotdown()
                cube.print()
            if s == [2, 1, 0]:
                cube.rotdown(1)
                cube.print()

            # source in row 1
            if s == [0, 0, 1]:
                cube.rotleft()
                cube.rotdown()
                cube.rotleft(1)
            if s == [0, 2, 1]:
                cube.rotleft(1)
                cube.rotdown()
                cube.rotleft()
            if s == [2, 0, 1]:
                cube.rotright(1)
                cube.rotdown(1)
                cube.rotright()
            if s == [2, 2, 1]:
                cube.rotright()
                cube.rotdown(1)
                cube.rotright(1)

            # source in row 2
            if s == [0, 1, 2]:
                cube.rotleft()
                cube.rotleft()
                cube.rotdown()
            if s == [1, 0, 2]:
                cube.rotfront()
                cube.rotfront()
            if s == [2, 1, 2]:
                cube.rotright()
                cube.rotright()
                cube.rotdown(1)
            if s == [1, 2, 2]:
                print("source in back")
                cube.rot_cube_left_cw(1)
                cube.rotleft()
                cube.rotleft()
                cube.rot_cube_left_cw()
                cube.rotdown()
                cube.rotdown()

            # assert white edge in intermediate position
            if cube.bottom[0, 1][0] == 'w' or cube.front[2, 1][0] == 'w':
                print('yes')
            else:
                print('no!')

            # Target
            if t == [0, 1, 2]:
                cube.rotdown(1)
                cube.rotleft()
                cube.rotleft()
            if t == [1, 0, 2]:
                cube.rotfront()
                cube.rotfront()
            if t == [2, 1, 2]:
                cube.rotdown()
                cube.rotright()
                cube.rotright()
            if t == [1, 2, 2]:
                print("target in back")
                cube.rot_cube_left_cw(1)
                cube.rotdown()
                cube.rotdown()
                cube.rotleft()
                cube.rotleft()
                cube.rot_cube_left_cw()

        for i in range(0, 4):

            if(not cube.top[1, 2][0] == 'w'):
                cube.rotright(1)
                cube.rotup()
                cube.rotfront(1)
                cube.rotup(1)
            cube.rot_cube_left_cw()