# This module contains the objects and methods used in the main program

import numpy as np

# Redefinitions of numpy booleans for less verbose syntax
bTrue = np.bool_(True)
bFalse = np.bool_(False)


def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


class GameOfLife():
    """
    ---March 2020---
    This class implements a simple way of simulating Conway's Game of Life.
    The class has two main attributes:
    -Board: The numpy boolean matrix that contains the current status of the game
    -elems: A dict with all the seed figures you can initialize through new_elem()
    """
    def __init__(self, x_size=50, y_size=50, config=None):
        self.Board = np.zeros((x_size, y_size), dtype=np.bool_)

        # Gliders and different figures
        self.elems = {
            "stills": {
                "block": {
                    "cells": [[0, 0], [0, 1], [1, 0], [1, 1]],
                    "x_width": 2,
                    "y_width": 2
                },
                "beehive": {
                    "cells": [[0, 1], [0, 2], [1, 0], [1, 3], [2, 1], [2, 2]],
                    "x_width": 4,
                    "y_width": 3
                }
            },
            "oscillators": {
                "acorn": {
                    "cells": [[0, 1], [1, 3], [2, 0], [2, 1], [2, 4], [2, 5], [2, 6]],
                    "x_width": 7,
                    "y_width": 3
                }
            },
            "ships": {
                "glider": {
                    "cells": [[0, 1], [1, 2], [2, 0], [2, 1], [2, 2]],
                    "x_width": 3,
                    "y_width": 3
                },
                "lwss": {
                    "cells": [[0, 3], [1, 1], [1, 5], [2, 0], [3, 0], [3, 5], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]],
                    "x_width": 6,
                    "y_width": 5
                }
            }
        }

    def list_elems(self):
        """
        Prints a list of available elements that can be passed as strings to new_elem()
        """

        print("Available elements can be added to the board through the new_elem() method:")
        for category in self.elems:
            for figure in self.elems[category]:
                print("-", str(figure))

    def init_board(self, list_of_initial_cells):
        """
        This method sets the board to the passed parameter, and it accepts:
        -n x 2 sized list (x & y pairs)
        -np.array that will be cast to a np-bool_ array
        """

        # list_of_initial_cells must be a n x 2 sized python list
        if isinstance(list_of_initial_cells, type(list)):
            for elem in list_of_initial_cells:
                self.Board[elem[0], elem[1]] = bTrue
        # list_of_initial_cells must be a n x np.array (bool or int)
        # the board will be resized accordingly
        elif isinstance(list_of_initial_cells, type(np.array)):
            self.Board = np.copy(list_of_initial_cells.astype(np.bool_))

    def new_elem(self, figure="glider", top_left_x=0, top_left_y=0, x_dir=1, y_dir=1):
        """
        This method adds any available element to the board, by first clearing the area.
        Parameters are the x and y coordinates of the corner, and the figure can be flipped
        on either axis with x_dir and y_dir parameters
        Available figures are listed through the list_elems() method.
        """

        # Breadth-first search of the correct category
        for category in self.elems:
            if figure in self.elems[category]:
                category = str(category)
                break
        # Clear existing cells to introduce the figure (neighbouring cells aren't cleared!)
        for i in range(self.elems[category][figure]["x_width"]):
            for j in range(self.elems[category][figure]["y_width"]):
                self.Board[top_left_x + x_dir * i, top_left_y + y_dir * j] = bFalse
        # Set correct cells to bTrue
        for elem in self.elems[category][figure]["cells"]:
            self.Board[top_left_x + x_dir * elem[0], top_left_y + y_dir * elem[1]] = bTrue

    def next_gen(self):
        """
        This method takes no parameters, and simply returns a np.array of ints containing
        the next generation of the board, updating the self.Board attribute
        """

        temp_old_gen = np.copy(self.Board)
        for i in range(temp_old_gen.shape[0]):
            for j in range(temp_old_gen.shape[1]):
                neighbours = self.num_neighbours(i, j, temp_old_gen)
                self.Board[i, j] = self.update_cell_value(temp_old_gen[i][j], neighbours)
                # self.Board[i, j] = self.update_cell(i, j, temp_old_gen, neighbours)
        return self.Board.astype(int)

    def num_neighbours(self, x_orig, y_orig, board=None):
        """
        Returns the number of neighbours a cell has given the x and y coordinates,
        and a np.array board (the board can be np.int or np.bool_).
        If no board is given, self.Board is passed as default
        """

        if isinstance(board, type(None)):
            tmp = np.copy(self.Board)  # default board is self.board
        else:
            tmp = np.copy(board)

        num = 0
        for i in range(x_orig - 1, x_orig + 2):
            for j in range(y_orig - 1, y_orig + 2):
                if self.valid_cell(i, j):
                    if tmp[i, j] == bTrue:
                        num = num + 1

        if tmp[x_orig, y_orig] is bTrue:
            return num - 1
        else:
            return num

    def valid_cell(self, i, j):
        """
        Checks if a set of indexes is within the range of self.Board
        """

        if i in range(self.Board.shape[0]) and j in range(self.Board.shape[1]):
            return True
        else:
            return False

    def update_cell_value(self, curr_cell_status, num):
        """
        Returns the updated cell status according to Conway's rules
        """

        # if cell is alive
        if curr_cell_status == bTrue:
            if num == 2 or num == 3:
                return bTrue
            else:
                return bFalse
        # if cell is dead
        elif curr_cell_status == bFalse:
            if num == 3:
                return bTrue
            else:
                return bFalse
        else:
            raise Exception("Cell isn't bTrue or bFalse")


if __name__ == "__main__":
    Test_obj = GameOfLife(12, 12)
    # print(help(GameOfLife))
    # print("-----")
    # exit()
    print("-----")
    Test_obj.list_elems()
    print("-----")
    exit()
    # Test_obj.init_board([[1, 1], [2, 3], [3, 2], [3, 3], [1, 4]])
    Test_obj.new_elem(figure="glider", top_left_x=3, top_left_y=3)
    print("Gen 1")
    print("-----")
    print(Test_obj.next_gen())
    print("Gen 2")
    print("-----")
    print(Test_obj.next_gen())
    print("Gen 3")
    print("-----")
    print(Test_obj.next_gen())
    print("Gen 4")
    print("-----")
    print(Test_obj.next_gen())
