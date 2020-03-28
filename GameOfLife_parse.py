"""
This module contains the parse implementation of the GameOfLife object
used in Animation.py
"""
import numpy as np
import os


class GameOfLife():
    """
    ---March 2020---
    This class implements a simple way of simulating Conway's Game of Life.
    The class has two main attributes:
    -living: A list of tuples of the living cells for every generation
    -figures: A list with all the seed figures you can initialize through new_elem()
    -
    """
    def __init__(self, x_size=50, y_size=50):
        self.living = []
        self.deadnear = []
        self.board_dim = (x_size, y_size)
        self.Board = None
        # Gliders and different figures are stored in a folder in the same directory as this file
        try:
            self.figure_dir = os.getcwd() + "\\figures"
            os.chdir(self.figure_dir)
            aux = os.listdir()
            self.figures = []
            for elem in aux:
                thing = elem.split(".")[0]
                self.figures.append(thing)
            os.chdir('..')
        except:
            print("No figures found in figures folder, check the file system")

    def list_elems(self):
        """
        Prints a list of available elements that can be passed as strings to new_elem()
        """
        print(self.figures)

    def init_board(self, initializer, pad=0, ones="*", zeros="."):
        """
        This method sets the board to the passed parameter, and it accepts:
        -n x 2 sized list (x & y pairs)
        -np.array that will be cast to a np-bool_ array
        """
        self.living = []
        # initializer can be a list with x,y pair lists or tuples as its elements
        if isinstance(initializer, list):
            for elem in initializer:
                self.living.append((elem[0], elem[1]))

        # initializer can also be a n x np.array (bool or int)
        # the board will be resized accordingly
        elif isinstance(initializer, type(np.array)):
            for row in initializer:
                for col in row:
                    if initializer[row][col] == 1:
                        self.living.append((row, col))
        # initializer can also be a filename with padding
        elif isinstance(initializer, str):
            loaded_board = self.LoadFromTxt(figure=initializer, ones="*", zeros=".")
            for row in loaded_board:
                for col in row:
                    if loaded_board[row][col] == 1:
                        self.living.append((row, col))

    def new_elem(self, figure=None, top_left_x=0, top_left_y=0, x_dir=1, y_dir=1):
        """
        This method adds any available element to the board, by first clearing the area.
        Parameters are the x and y coordinates of the corner, and the figure can be flipped
        on either axis with x_dir and y_dir parameters
        Available figures are listed through the list_elems() method.
        """

        loaded_board = self.LoadFromTxt(figure=figure, ones="*", zeros=".")
        # Clear existing cells to introduce the figure (neighbouring cells aren't cleared!)
        for i in range(loaded_board.shape[0]):
            row = top_left_x + x_dir * i
            for j in range(loaded_board.shape[1]):
                col = top_left_y + x_dir * j
                if self.__isvalidcell_(row, col):
                    if loaded_board[i][j] == 1:
                        self.living.append((row, col))
                    else:  # If the loaded value is 0, try to remove from living
                        try:
                            self.living.remove((row, col))
                        except:
                            pass

    def next_gen(self):
        """
        This method takes no parameters, and simply returns a np.array of ints containing
        the next generation of the board
        """

        next_living = []
        checked_dead = []
        for cell in self.living:
            if self.num_neighbours(cell, self.living, cell_status=1) in [2, 3]:
                next_living.append(cell)
            else:  # If the living cell doesn't have 2 or 3 neighbours, it doesn't survive
                pass
            # loop through all neighbouring cells
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):
                    # Check if cell is on the board, and if it isn't the "center" living cell
                    if self.__isvalidcell_(i, j) and (i, j) != cell:
                        # Check if it has been checked already this round, and if it is dead
                        if ((i, j) not in checked_dead) and ((i, j) not in self.living):
                            checked_dead.append((i, j))
                            if self.num_neighbours((i, j), self.living, cell_status=0) == 3:
                                next_living.append((i, j))

        self.living = next_living
        return self.ListToNumpy(self.living)

    def num_neighbours(self, cell, living_list, cell_status=0):
        """
        Returns the number of neighbours a cell has given the x and y coordinates,
        and a np.array board (the board can be np.int or np.bool_).
        If no board is given, self.Board is passed as default
        """

        num = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                    if (i, j) in living_list:
                        num = num + 1

        if cell_status == 1:
            return num - 1
        else:
            return num

    def __isvalidcell_(self, i, j):
        """
        Checks if a set of indexes is within the range of self.Board
        """

        if i in range(self.board_dim[0]) and j in range(self.board_dim[1]):
            return True
        else:
            return False

    def getBoard(self):
        return self.ListToNumpy(self.living)

    def LoadFromTxt(self, figure, ones="*", zeros="."):
        aux_list = []
        os.chdir(self.figure_dir)
        with open(figure + ".txt", "r") as f:
            for num_rows, line in enumerate(f, 1):
                clean_line = line.strip("\n")
                clean_line = clean_line.replace(ones, "1")
                clean_line = clean_line.replace(zeros, "0")
                num_cols = len(clean_line)
                for char in clean_line:
                    aux_list.append(np.uint8(char))
        aux_mat = np.asarray(aux_list, dtype=np.uint8)
        aux_mat = np.reshape(aux_mat, (num_rows, num_cols))
        os.chdir('..')
        return aux_mat

    def ListToNumpy(self, list_to_convert):
        aux_mat = np.zeros(self.board_dim, dtype=np.uint8)
        for elem in list_to_convert:
            aux_mat[elem[0], elem[1]] = 1
        return aux_mat


if __name__ == "__main__":

    Test_obj = GameOfLife(12, 12)

    print("-----")
    Test_obj.list_elems()
    print("-----")
    Test_obj.new_elem(figure="glider", top_left_x=3, top_left_y=3)
    print(Test_obj.getBoard())
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
