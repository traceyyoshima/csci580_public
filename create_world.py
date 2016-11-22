import random
import sys

def world_to_string(x):
    obs = ""
    # check NW
    if x >= 128:
        x -= 128
        obs += "A"

    # check N
    if x >= 64:
        x -= 64
        obs += "N"

    # check NE
    if x >= 32:
        x -= 32
        obs += "B"

    # check E
    if x >= 16:
        x -= 16
        obs += "E"

    # check SE
    if x >= 8:
        x -= 8
        obs += "C"

    # check S
    if x >= 4:
        x -= 4
        obs += "S"

    # check SW
    if x >= 2:
        x -= 2
        obs += "D"

    # check W
    if x >= 1:
        x -= 1
        obs += "W"
    return obs

if len(sys.argv) > 3:
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    num_obs = int(sys.argv[3])
    debug = 0
    if len(sys.argv) > 4:
        debug = int(sys.argv[4])

    matrix = [[0 for x in range(width)] for y in range(height)]
    myworld = [[0 for x in range(width)] for y in range(height)]
    journey = [["X" for x in range(width)] for y in range(height)]

    if debug:
        print("the world\n1 = wall 0 = empty")

    # generate a width * height sized world
    # each square has a ~75% chance to be an empty square
    # and a ~25% chance  to be a wall
    for i in range(0,height):
        for j in range(0,width):
            # assign a random value between 0 and 100
            matrix[i][j] = random.randint(0,100)
            # if i am less than than 75 i am not a wall
            if matrix[i][j] < 75:
                matrix[i][j] = 0
            # otherwise i am a wall
            else:
                matrix[i][j] = 1

            # debug output
            if debug:
                print(matrix[i][j],end = " ")
        # debug output
        if debug:
            print()

    # determine the value of each square for myworld
    # world is read as ANBECSDW:
    # | A  | N   | B  | E  | C  | S  | D  | W  |
    # | NW | N   | NE | E  | SE | S  | SW | W  |
    # which can be represented as a 8 bit binary number
    # 00000001 = 128 = A
    # 00000010 =  64 = N
    # 00000100 =  32 = B
    # 00001000 =  16 = E
    # 00010000 =   8 = C
    # 00100000 =   4 = S
    # 01000000 =   2 = D
    # 10000000 =   1 = W
    # each obsevation of a wall adds to total of myworld[i][j]
    for i in range(0,height):
        for j in range(0,width):
            N = i - 1
            S = i + 1
            W = j - 1
            E = j + 1
            obs = "";

            # check NW
            if N < 0 or W < 0:
                obs += "A"
                myworld[i][j] += 128
            elif matrix[N][W]:
                obs += "A"
                myworld[i][j] += 128

            # check N
            if N < 0:
                obs += "N"
                myworld[i][j] += 64
            elif matrix[N][j]:
                obs += "N"
                myworld[i][j] += 64

            # check NE
            if N < 0 or E == width:
                obs += "B"
                myworld[i][j] += 32
            elif matrix[N][E]:
                obs += "B"
                myworld[i][j] += 32

            # check E
            if E == width:
                obs += "E"
                myworld[i][j] += 16
            elif matrix[i][E]:
                obs += "E"
                myworld[i][j] += 16

            # check SE
            if S == height or E == width:
                obs += "C"
                myworld[i][j] += 8
            elif matrix[S][E]:
                obs += "C"
                myworld[i][j] += 8

            # check S
            if S == height:
                obs += "S"
                myworld[i][j] += 4
            elif matrix[S][j]:
                obs += "S"
                myworld[i][j] += 4

            # check SW
            if S == height or W < 0:
                obs += "D"
                myworld[i][j] += 2
            elif matrix[S][W]:
                obs += "D"
                myworld[i][j] += 2

            # check W
            if W < 0:
                obs += "W"
                myworld[i][j] += 1
            elif matrix[i][W]:
                obs += "W"
                myworld[i][j] += 1

            if matrix[i][j] == 1:
                myworld[i][j] = 255

            # update the original world if the square is impossible to get out of
            # because we need the original world to generate observations
            if myworld[i][j] == 255:
                matrix[i][j] = 1

            if debug:
                print("myworld["+str(i)+"]["+str(j)+"] = " + str(myworld[i][j]), end = " ")
                print("obs: " + obs)


    test_debug_file = open("test.debug", "w")
    test_debug_file.write("My World: \n")
    for i in range(0,height):
        for j in range(0,width):
            test_debug_file.write(str(matrix[i][j]) + " ")
            if debug:
                print(matrix[i][j],end = " ")
        test_debug_file.write("\n")
        if debug:
            print()

    robot_input_file = open("test.in","w")
    for i in range(0,height):
        for j in range(0,width):
            robot_input_file.write(str(myworld[i][j]) + " ")
            if debug:
                print(myworld[i][j],end = " ")
        if debug:
            print()
        robot_input_file.write("\n")
    robot_input_file.close()

    robot_obs_file = open("test.obs", "w")
    longest = 1
    while True:
        row = random.randint(0,height - 1);
        col = random.randint(0,width - 1);
        if(matrix[row][col] == 0):
            break
    for i in range(num_obs):
        test_debug_file.write("@time["+str(i)+"] @ matrix["+str(row)+"]["+str(col)+"] ")
        if debug:
            print("obs @ location: ["+str(row)+"]["+str(col)+"]")
        robot_obs_file.write(world_to_string(myworld[row][col]) + " ")
        if journey[row][col] == "X":
            journey[row][col] = str(i)
        else:
            journey[row][col] += "," + str(i)
            longest += 1
        while True:
            go_north = random.randint(0,1)
            go_west = 0
            go_east = random.randint(0,1)
            go_south = 0
            temp_row = row;
            temp_col = col;
            went = ""
            if go_north:
                temp_row = row - 1
            else:
                go_south = random.randint(0,1)
                if go_south:
                    temp_row = row + 1
            if go_east:
                temp_col = col - 1
            else:
                go_west = random.randint(0,1)
                if go_west:
                    temp_col = col + 1
            if not (temp_row == row and temp_col == col):
                if go_north:
                    went += "North"
                    if go_east:
                        went += "East"
                    elif go_west:
                        went += "West"
                elif go_south:
                    went += "South"
                    if go_east:
                        went += "East"
                    elif go_west:
                        went += "West"
                elif go_east:
                    went += "East"
                elif go_west:
                    went += "west"
                if temp_row >= 0 and temp_row < width and temp_col >= 0 and temp_col < height:
                    if matrix[temp_row][temp_col] == 0:
                        test_debug_file.write("Went: " + went + "\n")
                        row = temp_row
                        col = temp_col
                        break

    robot_obs_file.write("\n")
    robot_obs_file.close()

    test_debug_file.write("Journey: \n")
    for i in range(0,height):
        for j in range(0,width):
            if journey[i][j] == "X":
                test_debug_file.write(journey[i][j] + (" " * (longest + 1)))
            else:
                test_debug_file.write(journey[i][j] + (" " * (longest - len(journey[i][j]) + 2)))
        test_debug_file.write("\n")

    test_debug_file.close()
