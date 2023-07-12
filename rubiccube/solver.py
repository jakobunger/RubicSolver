import rubiccube as rb
import numpy as np


class Solver():

    # Returns the color pair list of all corners
    def get_corner_list(self, cube: rb):
        list = [cube.top[0, 0][0] + cube.left[0, 0][0] + cube.back[2, 0][0],
                cube.top[2, 0][0] + cube.left[0, 2][0] + cube.front[0, 0][0],
                cube.top[0, 2][0] + cube.right[0, 2][0] + cube.back[2, 2][0],
                cube.top[2, 2][0] + cube.right[0, 0][0] + cube.front[0, 2][0],

                cube.bottom[2, 0][0] + cube.left[2, 0][0] + cube.back[0, 0][0],
                cube.bottom[0, 0][0] + cube.left[2, 2][0] + cube.front[2, 0][0],
                cube.bottom[2, 2][0] + cube.right[2, 2][0] + cube.back[0, 2][0],
                cube.bottom[0, 2][0] + cube.right[2, 0][0] + cube.front[2, 2][0]]

        for i in range(0, 8):
            # sort list to be able to compare the lists
            list[i] = sorted(list[i])

        # coordinates of edges. Origin is on the left lower front corner
        positions = [[0, 2, 2], [0, 0, 2], [2, 2, 2], [2, 0, 2],
                     [0, 2, 0], [0, 0, 0], [2, 2, 0], [2, 0, 0]]

        # return colors and coordinates
        res = (list, positions)
        return res

        # Returns the color pair list of all edges
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
            # sort list to be able to compare the lists
            list[i] = sorted(list[i])
            # unicolor edges do not exist!
            assert not list[i][0] == list[i][1]

        # coordinates of edges. Origin is on the left lower front corner
        positions = [[1, 2, 2], [0, 1, 2], [2, 1, 2], [1, 0, 2],
                     [0, 2, 1], [2, 2, 1], [0, 0, 1], [2, 0, 1],
                     [1, 2, 0], [0, 1, 0], [2, 1, 0], [1, 0, 0]]

        # return colors and coordinates
        res = (list, positions)
        return res

    # temporary, will be deleted
    def check_edge_list(self, cube: rb):
        listcheck = self.get_edge_list(cube)[0]
        print(listcheck)
        ground_truth = sorted([['g', 'o'], ['b', 'w'], ['b', 'y'], ['g', 'r'], ['b', 'o'], ['r', 'y'], ['g', 'w'], ['b', 'r'], ['o', 'y'], ['r', 'w'], ['g', 'y'], ['o', 'w']])
        listcheck = sorted(listcheck)
        # The edges cannot be altered- just moved.
        assert listcheck == ground_truth

    def check_corner_list(self, cube: rb):
        ground_truth = [['g', 'r', 'w'], ['b', 'r', 'w'], ['b', 'o', 'w'], ['g', 'o', 'w'],
                        ['g', 'r', 'y'], ['b', 'r', 'y'], ['b', 'o', 'y'], ['g', 'o', 'y']]
        listcheck = sorted(self.get_corner_list(cube)[0])
        ground_truth = sorted(ground_truth)
        assert listcheck == ground_truth


    def get_edge(self, cube: rb, color1, color2):
        edge_list = self.get_edge_list(cube)
        search_for_colorpair = sorted([color1, color2])
        for i in range(0, len(edge_list[0])):
            if edge_list[0][i] == search_for_colorpair:
                return edge_list[1][i]
        # should not end here, edge not found
        assert 0

    def get_corner(self, cube: rb, color1, color2, color3):
        corner_list = self.get_corner_list(cube)
        color_list = sorted([color1, color2, color3])
        for i in range(0, len(corner_list[0])):
            if corner_list[0][i] == color_list:
                return corner_list[1][i]
        # should not end here, edge not found
        assert 0

    # First step of algorithm: Get a white cross
    def step_1(self, cube: rb):
        # require default rotation

        # get edge list of cube
        edge_list = self.get_edge_list(cube)
        target = []
        white_edge_list = []

        # filter all edges with white brick
        for ind in range(0, len(edge_list[0])):
           if edge_list[0][ind][1] == 'w' or edge_list[0][ind][0] == 'w':
                if edge_list[0][ind][1] == 'w':
                    second_color = edge_list[0][ind][0]
                elif edge_list[0][ind][0] == 'w':
                    second_color = edge_list[0][ind][1]
                else:
                    assert 0

                white_edge_list.append([edge_list[0][ind][0], 'w'])

                # set target position for all 4 white edges
                if second_color == 'g':
                    target.append([1, 0, 2])
                elif second_color == 'o':
                    target.append([0, 1, 2])
                elif second_color == 'r':
                    target.append([2, 1, 2])
                elif second_color == 'b':
                    target.append([1, 2, 2])
                else:
                    assert 0

        # assure source.len = target.len

        # move all edges to target position
        for i in range(0, len(white_edge_list)):
            s = self.get_edge(cube, white_edge_list[i][0], white_edge_list[i][1])
            t = target[i]

            # 1st step: move all sources to intermediate position [1,0,0]

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
            assert cube.bottom[0, 1][0] == 'w' or cube.front[2, 1][0] == 'w'

            # 2nd step: move edges to target positions
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

        # if colors are switched then correct alignment
        for i in range(0, 4):

            if(not cube.top[1, 2][0] == 'w'):
                cube.rotright(1)
                cube.rotup()
                cube.rotfront(1)
                cube.rotup(1)

            # move on to next side
            cube.rot_cube_left_cw()


    # Second step of algorithm: put all white corners to the correct opsition
    def step_2(self, cube: rb):
        # toDo: Check normal alignment

        # move correct white corner to its corresponding target position
        for i in range(0, 4):
            target_colors = ['w', cube.front[1, 1][0], cube.right[1, 1][0]]
            source_corner_pos = self.get_corner(cube, *target_colors)

            if source_corner_pos == [0, 2, 2]:
                cube.rotleft(1)
                cube.rotdown()
                cube.rotdown()
                cube.rotleft()
            elif source_corner_pos == [0, 0, 2]:
                cube.rotleft()
                cube.rotdown()
                cube.rotleft(1)
            elif source_corner_pos == [2, 2, 2]:
                cube.rotright()
                cube.rotdown(1)
                cube.rotright(1)
            elif source_corner_pos == [2, 0, 2]:
                # correct position, check if alignment is correct
                if cube.front[0, 2] == cube.front[1, 1] and cube.top[2, 2] == cube.top[1, 1] and cube.right[0, 0] == cube.right[1, 1]:
                    # yes, continue with next side
                    continue
            elif source_corner_pos == [0, 2, 0]:
                cube.rotdown()
                cube.rotdown()
            elif source_corner_pos == [0, 0, 0]:
                cube.rotdown()
            elif source_corner_pos == [2, 2, 0]:
                cube.rotdown(1)

            x=0

 #               [0, 2, 2], [0, 0, 2], [2, 2, 2], [2, 0, 2],
#                      [0, 2, 0], [0, 0, 0], [2, 2, 0], [2, 0, 0]