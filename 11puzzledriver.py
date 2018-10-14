###################################
## Claudia Della Serra, 26766048 ##
###################################

import argparse
from heapq import heappush, heappop

from Node import Node
from time import time

parser = argparse.ArgumentParser(description="Take in an 11d puzzle")

parser.add_argument("puzzle", type=int, nargs='+', help="Order of tiles for the 11d puzzle.")

args = parser.parse_args()
puzzle_start_state = Node(args.puzzle, None, 0)
puzzle_tile_positions = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]
puzzle_end_state = Node([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0], None, None)
open_list = []
closed_list = []

puzzle_width = 4
puzzle_height = 3
max_depth = 6


def output_solution(current, output, start_time):
    move_count = 0
    final_configurations = []
    while current.get_parent is not None:
        final_configurations.insert(0, current.value)
        move_count += 1
        if not current == puzzle_start_state:
            current = current.get_parent()
        else: break

    for config in final_configurations:
        if config == puzzle_start_state.value:
            print(0, config, file=output)
        else:
            print(puzzle_tile_positions[config.index(0)], config, file=output)
    print("\nMove count: ", move_count, "\nTime Taken: ", (time()-start_time), " seconds", file=output)
    output.close()


#####################################################
################ Depth First Search #################
# Searches a Node's children before its siblings    #
#####################################################
def depth_first_search():
    open_list.append(puzzle_start_state)
    output = open("puzzleDFS.txt", "w")
    start = time()

    while open_list:
        current = open_list.pop(0)
        if current == puzzle_end_state:
            output_solution(current, output, start)
            break

        closed_list.insert(0, current)

        # You only want to generate children that aren't beyond the max depth
        if (max_depth-1) > current.get_level():
            next_moves = current.derive_children(current.get_level())
            #next_moves = current.get_children()

            # We reverse the children because they are derived in prioritized order,
            # appending them in their original order would have the least prioritized node visited first
            for move in reversed(next_moves):
                if move not in closed_list and move not in open_list:
                    open_list.insert(0, move)


#######################################################################
#                      Best first search                              #
#     searches the best path according to an admissible heuristic     #
#######################################################################
def best_first_search(heuristic):
    heappush(open_list, puzzle_start_state)
    start = time()

    while open_list:
        current = heappop(open_list)
        if current.cost is None:
            h = 0
            if heuristic is "Hamming":
                h = hamming_distance(current, 0)
            elif heuristic is "OORC":
                h = out_of_row_column(current, 0)
            current.set_cost(h)

        if current == puzzle_end_state:
            if heuristic is "Hamming":
                output = open("puzzleBFS-h1.txt", "w")
            elif heuristic is "OORC":
                output = open("puzzleBFS-h2.txt", "w")
            output_solution(current, output, start)
            break

        next_moves = current.derive_children(current.get_level())
        #next_moves = current.get_children()
        closed_list.append(current)

        for move in next_moves:
            h = 0
            if move not in closed_list and move not in open_list:
                if heuristic is "Hamming":
                    h = hamming_distance(move, 0)
                elif heuristic is "OORC":
                    h = out_of_row_column(move, 0)
                move.set_cost(h)
                heappush(open_list, move)


#######################################################################
#                          A star search                              #
#  searches the best path according to the total cost of the path     #
#######################################################################
def a_star_algorithm(heuristic):
    # open list is a priority queue sorted by total cost
    heappush(open_list, puzzle_start_state)
    start = time()

    while open_list:
        current = heappop(open_list)
        if current.cost is None:
            if heuristic is "Hamming":
                hamming_distance(current, current.get_level())
            elif heuristic is "OORC":
                out_of_row_column(current, current.get_level())

        if current == puzzle_end_state:
            if heuristic is "Hamming":
                output = open("puzzleAS-h1.txt", "w")
            elif heuristic is "OORC":
                output = open("puzzleAs-h2.txt", "w")
            output_solution(current, output, start)
            break

        next_moves = current.derive_children(current.get_level())
        #next_moves = current.get_children()
        closed_list.append(current)

        for move in next_moves:
            if move not in closed_list:
                h = move.get_level()
                if heuristic is "Hamming":
                    h = hamming_distance(current, h)
                elif heuristic is "OORC":
                    h = out_of_row_column(current, h)
                move.set_cost(h)
                if move in open_list:
                    # If the node is already in the open list, but the current path is shorter, replace it and
                    # take this path
                    current_move_in_list = open_list.pop(open_list.index(move))
                    current_cost = current_move_in_list.get_cost()
                    if h < current_cost:
                        heappush(open_list, move)
                    else:
                        heappush(open_list, current_move_in_list)
                else:
                    heappush(open_list, move)


# Though we are passing a "total cost" to the function, the total cost is only used for algorithm A*
# in the best first algorithm, a 0 is passed as no other costs are considered
def hamming_distance(node, total_cost):
    configuration = node.value
    h = total_cost
    for i in range(0, len(configuration)):
        if configuration[i] != puzzle_end_state.value[i] and configuration[i] != 0:
            h += 1
    return h


def out_of_row_column(node, total_cost):
    configuration = node.value
    h = total_cost
    for i in range(0, len(configuration)):
        if configuration[i] == 0:
            continue
        # check for out of row
        if (i >= 0 and i < 4 and configuration[i] > 4) or (i >= 4 and i < 8 and (configuration[i] < 5 or
                    configuration[i] > 8)) or (i >= 8 and i < 12 and configuration[i] < 9):
            h += 1
        #check out of column
        if ((i % 4) == 0 and (configuration[i] != 1 and configuration[i] != 5 and configuration[i] != 9)) or \
                ((i % 4) == 1 and (configuration[i] != 2 and configuration[i] != 6 and configuration[i] != 10)) or\
                ((i % 4) == 2 and (configuration[i] != 3 and configuration[i] != 7 and configuration[i] != 11)) or \
                ((i % 4) == 3 and (configuration[i] != 4 and configuration[i] != 8)):
            h += 1
    return h


#depth_first_search()
#best_first_search("Hamming")
#best_first_search("OORC")
#a_star_algorithm("Hamming")
#a_star_algorithm("OORC")


