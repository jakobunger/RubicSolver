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

    # temporary, checking edge consistency
    def check_edge_list(self, cube: rb):
        listcheck = self.get_edge_list(cube)[0]
        ground_truth = sorted([['g', 'o'], ['b', 'w'], ['b', 'y'], ['g', 'r'], ['b', 'o'], ['r', 'y'], ['g', 'w'], ['b', 'r'], ['o', 'y'], ['r', 'w'], ['g', 'y'], ['o', 'w']])
        listcheck = sorted(listcheck)
        # The edges cannot be altered- just moved.
        assert listcheck == ground_truth

    # temporary, checking corner consistency
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
        cube.normalized_rotation()

        # get edge list of cube
        edge_list = self.get_edge_list(cube)

        # list of edges with white color
        white_edge_list = []
        # target positions
        target = []

        # filter all edges with white color
        for ind in range(0, len(edge_list[0])):
           if edge_list[0][ind][1] == 'w' or edge_list[0][ind][0] == 'w':
                if edge_list[0][ind][1] == 'w':
                    second_color = edge_list[0][ind][0]
                elif edge_list[0][ind][0] == 'w':
                    second_color = edge_list[0][ind][1]
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
                # target edges green, orange, red, blue only
                else:
                    assert 0

        # move all edges to target position
        for i in range(0, len(white_edge_list)):
            s = self.get_edge(cube, white_edge_list[i][0], white_edge_list[i][1])
            t = target[i]

            # 1st step: move all sources to intermediate position [1,0,0]

            # source in row 0
            if s == [0, 1, 0]:
                cube.rotdown()
            if s == [1, 2, 0]:
                cube.rotdown()
                cube.rotdown()
            if s == [2, 1, 0]:
                cube.rotdown(1)

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
                cube.rot_cube_left_cw(1)
                cube.rotdown()
                cube.rotdown()
                cube.rotleft()
                cube.rotleft()
                cube.rot_cube_left_cw()

        # if colors are switched then correct alignment
        for i in range(0, 4):

            if not cube.top[1, 2][0] == 'w':
                cube.rotright(1)
                cube.rotup()
                cube.rotfront(1)
                cube.rotup(1)

            # move on to next side
            cube.rot_cube_left_cw()

        # assert white cross
        assert cube.top[0, 1][0] == 'w'
        assert cube.top[1, 0][0] == 'w'
        assert cube.top[1, 1][0] == 'w'
        assert cube.top[1, 2][0] == 'w'
        assert cube.top[2, 1][0] == 'w'


    # Second step of algorithm: put all white corners to the correct opsition
    def step_2(self, cube: rb):
        # ensure default rotation
        cube.normalized_rotation()

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
                cube.rotdown()
                cube.rotright(1)
                cube.rotdown(1)
                cube.rotdown(1)

            elif source_corner_pos == [2, 0, 2]:
                # correct position, check if alignment is correct
                if cube.front[0, 2][0] == cube.front[1, 1][0] and cube.top[2, 2][0] == cube.top[1, 1][0] and cube.right[0, 0][0] == cube.right[1, 1][0]:
                    # alignment correct, continue with next side
                    cube.rot_cube_left_cw()
                    continue
                else:
                    cube.rotright(1)
                    cube.rotdown(1)
                    cube.rotright()
                    cube.rotdown()
            elif source_corner_pos == [0, 2, 0]:
                cube.rotdown()
                cube.rotdown()
            elif source_corner_pos == [0, 0, 0]:
                cube.rotdown()
            elif source_corner_pos == [2, 2, 0]:
                cube.rotdown(1)

            # repeat r', d', r, d until corner in correct position with correct alignment
            for k in range(0, 10):
                cube.rotright(1)
                cube.rotdown(1)
                cube.rotright()
                cube.rotdown()
                if cube.front[0, 2][0] == cube.front[1, 1][0] and cube.top[2, 2][0] == cube.top[1, 1][0] and cube.right[0, 0][0] == cube.right[1, 1][0]:
                    break
                if k == 10:
                    assert 0

            cube.rot_cube_left_cw()

    # Third step of algorithm: put all mid level edges to the correct position
    def step_3(self, cube: rb):

        cube.rot_cube_down_cw()
        cube.rot_cube_down_cw()

        # source edges that need to be placed
        source_edges = [['b', 'o'], ['b', 'r'], ['g', 'r'], ['g', 'o']]
        source = []
        source_colors = []

        # if there are edges left that need to be placed, repeat
        while source_edges:
            source = []
            for i in range(0, len(source_edges)):
                source_edge_pos = self.get_edge(cube, source_edges[i][0], source_edges[i][1])

                # if edge is in medium vertical position, then skip. Try to find on tp level first.
                if source_edge_pos[2] < 2:
                    continue

                source = source_edge_pos
                source_colors = [source_edges[i][0], source_edges[i][1]]

            # if no target edge on top level available
            if not source:
                # move source edge to top row
                source = self.get_edge(cube, source_edges[i][0], source_edges[i][1])
                if not source:
                    assert 0

                rot_action = -1;
                if source == [0, 0, 1]:
                    # rot left
                    rot_action = 0
                if source == [2, 0, 1]:
                    # rot right
                    rot_action = 1
                if source == [0, 2, 1]:
                    cube.rot_cube_left_cw(1)
                    # rot left
                    rot_action = 0
                if source == [2, 2, 1]:
                    cube.rot_cube_left_cw()
                    # rot right
                    rot_action = 1

                if rot_action == 0:
                    cube.rotup(1)
                    cube.rotleft(1)
                    cube.rotup()
                    cube.rotleft()
                    cube.rotup()
                    cube.rotfront()
                    cube.rotup(1)
                    cube.rotfront(1)
                if rot_action == 1:
                    cube.rotup()
                    cube.rotright()
                    cube.rotup(1)
                    cube.rotright(1)
                    cube.rotup(1)
                    cube.rotfront(1)
                    cube.rotup()
                    cube.rotfront()
                if rot_action == -1:
                    assert 0
                continue

            # move target edge to correct face
            if source == [1, 2, 2]:
                cube.rot_cube_left_cw(1)
                cube.rot_cube_left_cw(1)
            if source == [0, 1, 2]:
                cube.rot_cube_left_cw(1)
            if source == [2, 1, 2]:
                cube.rot_cube_left_cw()

            for i in range(0, 4):
                if cube.front[0, 1][0] == cube.front[1, 1][0]:
                    break
                cube.rot_cube_left_cw()
                cube.rotup(1)

            # check if we need to rotate it clock- or counterclockwise
            if cube.top[2, 1][0] == cube.right[1, 1][0]:
                # rotate clockwise
                cube.rotup()
                cube.rotright()
                cube.rotup(1)
                cube.rotright(1)
                cube.rotup(1)
                cube.rotfront(1)
                cube.rotup()
                cube.rotfront()
            elif cube.top[2, 1][0] == cube.left[1, 1][0]:
                # rotate counter-clockwise
                cube.rotup(1)
                cube.rotleft(1)
                cube.rotup()
                cube.rotleft()
                cube.rotup()
                cube.rotfront()
                cube.rotup(1)
                cube.rotfront(1)
            else:
                assert 0
            # edge correctly positioned. Remove it from list.
            source_edges.remove(source_colors)

        # rotate back, white on top
        cube.rot_cube_down_cw()
        cube.rot_cube_down_cw()

    # Fourth step of algorithm: Create yellow cross
    def step_4(self, cube: rb):

        cube.rot_cube_down_cw()
        cube.rot_cube_down_cw()

        phase = -1
        while 1:
            if cube.top[0, 1][0] == 'y' and cube.top[2,1][0] == 'y' and cube.top[1,0][0] == 'y' and cube.top[1,2][0] == 'y':
                # yellow cross is already there
                phase = 4
                break

            # yellow line, rotate it horizontally
            elif cube.top[0, 1][0] == 'y' and cube.top[2,1][0] == 'y':
                phase = 3
                cube.rot_cube_left_cw()
            elif cube.top[1, 0][0] == 'y' and cube.top[1,2][0] == 'y':
                phase = 3

            # yellow angle
            elif cube.top[1, 0][0] == 'y' and cube.top[0, 1][0] == 'y':
                phase = 2
            elif cube.top[0, 1][0] == 'y' and cube.top[1, 2][0] == 'y':
                phase = 2
                cube.rot_cube_left_cw(1)
            elif cube.top[1, 2][0] == 'y' and cube.top[2, 1][0] == 'y':
                phase = 2
                cube.rot_cube_left_cw(1)
                cube.rot_cube_left_cw(1)
            elif cube.top[2, 1][0] == 'y' and cube.top[1, 0][0] == 'y':
                phase = 2
                cube.rot_cube_left_cw()

            # just center brick is yellow
            else:
                phase = 1

            # transfer to phase+1
            cube.rotfront()
            cube.rotright()
            cube.rotup()
            cube.rotright(1)
            cube.rotup(1)
            cube.rotfront(1)

    # Fifth step of algorithm: match colors of top level edges
    def step_5(self, cube: rb):

        while 1:
            # check if edges already match colors
            if cube.front[0, 1][0] == cube.front[1, 1][0] and cube.right[0, 1][0] == cube.right[1, 1][0] and cube.back[2, 1][0] == cube.back[1, 1][0] and cube.left[0, 1][0] == cube.left[1, 1][0]:
                #done
                break
            if cube.front[0, 1][0] == cube.right[1, 1][0] and cube.right[0, 1][0] == cube.back[1, 1][0] and cube.back[2, 1][0] == cube.left[1, 1][0] and cube.left[0, 1][0] == cube.front[1, 1][0]:
                cube.rotup(1)
                break
            if cube.front[0, 1][0] == cube.back[1, 1][0] and cube.right[0, 1][0] == cube.left[1, 1][0] and cube.back[2, 1][0] == cube.front[1, 1][0] and cube.left[0, 1][0] == cube.right[1, 1][0]:
                cube.rotup(1)
                cube.rotup(1)
                break
            if cube.front[0, 1][0] == cube.left[1, 1][0] and cube.right[0, 1][0] == cube.front[1, 1][0] and cube.back[2, 1][0] == cube.right[1, 1][0] and cube.left[0, 1][0] == cube.back[1, 1][0]:
                cube.rotup()
                break

            # Make sure that only one side center matches the face color
            for i in range(0, 4):
                if cube.front[0, 1][0] == cube.front[1, 1][0] and not cube.left[0, 1][0] == cube.left[1, 1][0] and not cube.back[2, 1][0] == cube.back[1, 1][0] and not cube.right[0, 1][0] == cube.right[1, 1][0]:
                    break
                cube.rotup()

            # Then permute the colors of the remaining top edges
            cube.rotright()
            cube.rotup()
            cube.rotright(1)
            cube.rotup()
            cube.rotright()
            cube.rotup()
            cube.rotup()
            cube.rotright(1)

    # Sixth step of algorithm: Check if top corners are positioned (but not necessary aligned) correctly
    def step_6(self, cube: rb):

        first_run = 1

        while 1:

            corner_tl = sorted([cube.top[0, 0][0], cube.left[0, 0][0], cube.back[2, 0][0]])
            corner_bl = sorted([cube.top[2, 0][0], cube.left[0, 2][0], cube.front[0, 0][0]])
            corner_tr = sorted([cube.top[0, 2][0], cube.right[0, 2][0], cube.back[2, 2][0]])
            corner_br = sorted([cube.top[2, 2][0], cube.right[0, 0][0], cube.front[0, 2][0]])

            corner_target_tl = sorted([cube.top[1, 1][0], cube.left[1, 1][0], cube.back[1, 1][0]])
            corner_target_bl = sorted([cube.top[1, 1][0], cube.left[1, 1][0], cube.front[1, 1][0]])
            corner_target_tr = sorted([cube.top[1, 1][0], cube.right[1, 1][0], cube.back[1, 1][0]])
            corner_target_br = sorted([cube.top[1, 1][0], cube.right[1, 1][0], cube.front[0, 1][0]])

            correct_positioned_corners = 0
            rot0 = 0
            rot_ccw = 0
            rot_2ccw = 0
            rot_cw = 0

            # check how many corners are positioned correctly
            if corner_br == corner_target_br:
                correct_positioned_corners = correct_positioned_corners + 1
                rot0 = 1
            if corner_tl == corner_target_tl:
                correct_positioned_corners = correct_positioned_corners + 1
                rot_2ccw = 1
            if corner_bl == corner_target_bl:
                correct_positioned_corners = correct_positioned_corners + 1
                rot_ccw = 1
            if corner_tr == corner_target_tr:
                correct_positioned_corners = correct_positioned_corners + 1
                rot_cw = 1

            # if =4 then we are done with this step
            if correct_positioned_corners == 4:
                # all corners are positioned correctly.
                break

            # make sure that top right corner is correct before starting the algorithm
            if rot0 == 0 and first_run:
                if rot_cw == 1:
                    cube.rot_cube_left_cw()
                elif rot_ccw == 1:
                    cube.rot_cube_left_cw(1)
                elif rot_2ccw == 1:
                    cube.rot_cube_left_cw(1)
                    cube.rot_cube_left_cw(1)

            if correct_positioned_corners > 0:
                first_run = 0
            else:
                # no matching corners, rotate top row and check again
                cube.rotup()
                continue

            cube.rotup()
            cube.rotright()
            cube.rotup(1)
            cube.rotleft(1)
            cube.rotup()
            cube.rotright(1)
            cube.rotup(1)
            cube.rotleft()

 # Seventh step of algorithm: Align all top corners correctly
    def step_7(self, cube: rb):

        #check if alignment is correct (then we are done)
        check_br = (cube.top[2, 2] == cube.top[1, 1] and cube.front[0, 2] == cube.front[1, 1] and cube.right[0, 0] == cube.right[1, 1])
        check_tr = (cube.top[0, 2] == cube.top[1, 1] and cube.back[2, 2] == cube.back[1, 1] and cube.right[0, 2] == cube.right[1, 1])
        check_tl = (cube.top[0, 0] == cube.top[1, 1] and cube.back[2, 0] == cube.back[1, 1] and cube.left[0, 0] == cube.left[1, 1])
        check_bl = (cube.top[2, 0] == cube.top[1, 1] and cube.front[0, 0] == cube.front[1, 1] and cube.left[0, 2] == cube.left[1, 1])
        if check_br and check_tr and check_tl and check_bl:
            # done
            return

        for i in range(0, 4):
            # repeat algorithm and rotate top row if corner is aligned correctly. Repeat for all 4 corners
            while not (cube.top[2, 2][0] == cube.top[2, 1][0] and cube.front[0, 2][0] == cube.front[0, 1][0] and cube.right[0, 0][0] == cube.right[0, 1][0]):
                cube.rotright(1)
                cube.rotdown(1)
                cube.rotright()
                cube.rotdown()

            cube.rotup()

