import argparse
import numpy as np

def get_coordinates(coordinates, map):


    CLI = argparse.ArgumentParser()
    
    CLI.add_argument(
        '-origin',
        nargs = '+',
        type = int

    )

    CLI.add_argument(
        '-goal',
        nargs = '+',
        type = int

    )


    args = CLI.parse_args()

    args.origin = tuple(args.origin)
    args.goal = tuple(args.goal)

    if map[args.origin[0]][args.origin[1]] == 0 or map[args.goal[0]][args.goal[1]] == 0:
        print("Refer to the co-ordinate list to enter relevant co-ordinate points")
        print("Haven't got a starting point yet? Try 0, 16 and 0, 16")
        
        print(args.origin, "--->", map[args.origin[0]][args.origin[1]])
        print(args.goal, "--->", map[args.goal[0]][args.goal[1]])

        return (0, 16), (0, 18)

    else:
        print(args.origin, "--->", map[args.origin[0]][args.origin[1]])
        print(args.goal, "--->", map[args.goal[0]][args.goal[1]])

        
        with open('array.txt', 'w') as f:
            f.write(str(coordinates))
        

        return args.origin, args.goal
