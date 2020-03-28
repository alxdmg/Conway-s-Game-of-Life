"""
This module contains the dense implementation of the GameOfLife object
used in Animation.py
"""
import numpy as np
import os


class GameOfLife():
    """
    ---March 2020---
    This class implements a simple way of simulating Conway's Game of Life.
    The class has two main attributes:
    -Board: The numpy boolean matrix that contains the current status of the game
    -elems: A dict with all the seed figures you can initialize through new_elem()
    """
    def __init__(self, x_size=50, y_size=50):
        self.Board = np.zeros((x_size, y_size), dtype=np.uint8)

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

        # initializer can be a n x 2 sized python list
        if isinstance(initializer, list):
            for elem in initializer:
                self.Board[elem[0], elem[1]] = 1

        # initializer can also be a n x np.array (bool or int)
        # the board will be resized accordingly
        elif isinstance(initializer, type(np.array)):
            self.Board = np.copy(initializer.astype(np.uint8))
        # initializer can also be a filename with padding
        elif isinstance(initializer, str):
            self.Board = self.LoadFromTxt(figure=initializer, ones="*", zeros=".")

        # Finally add padding if it was passed as argument
        if pad is not 0:
            self.Board = np.pad(self.Board, ((pad, pad), (pad, pad)), mode='constant', constant_values=0)

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
            for j in range(loaded_board.shape[1]):
                self.Board[top_left_x + x_dir * i, top_left_y + y_dir * j] = loaded_board[i][j]

    def next_gen(self):
        """
        This method takes no parameters, and simply returns a np.array of ints containing
        the next generation of the board, updating the self.Board attribute
        """
        temp_old_gen = np.copy(self.Board)
        for i in range(temp_old_gen.shape[0]):
            for j in range(temp_old_gen.shape[1]):
                neighbours = self.num_neighbours(i, j, temp_old_gen)
                self.Board[i, j] = self.new_cell_value(temp_old_gen[i][j], neighbours)
        return self.Board

    def num_neighbours(self, x_orig, y_orig, board=None):
        """
        Returns the number of neighbours a cell has given the x and y coordinates,
        and a np.array board (the board can be np.int or np.bool_).
        If no board is given, self.Board is passed as default
        """

        if isinstance(board, type(None)):
            tmp = self.Board  # default board is self.board
        else:
            tmp = board

        num = 0
        for i in range(x_orig - 1, x_orig + 2):
            for j in range(y_orig - 1, y_orig + 2):
                if self.__isvalidcell_(i, j):
                    if tmp[i, j] == 1:
                        num = num + 1

        if tmp[x_orig, y_orig] == 1:
            return num - 1
        else:
            return num

    def __isvalidcell_(self, i, j):
        """
        Checks if a set of indexes is within the range of self.Board
        """

        if i in range(self.Board.shape[0]) and j in range(self.Board.shape[1]):
            return True
        else:
            return False

    def new_cell_value(self, curr_cell_status, num):
        """
        Returns the updated cell status according to Conway's rules
        """

        # if cell is alive
        if curr_cell_status == 1:
            if num == 2 or num == 3:
                return 1
            else:
                return 0
        # if cell is dead
        elif curr_cell_status == 0:
            if num == 3:
                return 1
            else:
                return 0
        else:
            raise Exception("Cell isn't 1 or 0")

    def getBoard(self):
        return self.Board

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


if __name__ == "__main__":

    Test_obj = GameOfLife(12, 12)
    print("-----")
    Test_obj.list_elems()
    print("-----")
    Test_obj.new_elem(figure="acorn", top_left_x=3, top_left_y=3)
    print(Test_obj.getBoard())
    print("Gen 1")
    print("-----")
    print(Test_obj.next_gen())
    print("Gen 2")
    print("-----")
    exit()
    print(Test_obj.next_gen())
    print("Gen 3")
    print("-----")
    print(Test_obj.next_gen())
    print("Gen 4")
    print("-----")
