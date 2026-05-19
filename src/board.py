

import numpy as np
import time
import constants
from tile import Tile

"""
Board is the rules and state for a turn-based game.

- State: the grid of cell values (0 = empty, non-zero = a player's identifier)
- Rules: what moves are legal, how moves are applied, and how to detect win/tie

When changing this class to create new game you must:
- Define how a move is applied and verify the move is legal
- Update the game state after each move is applied
- Define how a winner, and or tie is determined

Note: All rendering should be done elsewhere.

"""

class Board:
    def __init__(self):
        self.rows = constants.NUM_ROWS
        self.cols = constants.NUM_COLS

        self.game_board = np.zeros((self.rows, self.cols))

        # last move as a tuple (row, col) on game_board
        self.last_move = None
        self.board_empty = True
        self.moves = 0


    def apply_move(self, col: int, player_identifier) -> bool:

        """
        Try to place a player's move on the board at (row, col) specified by move.
        Returns True if move was successfully applied to the board, otherwise False.
        """

        if self.is_move_valid(col):
            row = constants.NUM_ROWS -1

            while self.game_board[row, col] == 1.0 or self.game_board[row, col] == -1.0:
                row -= 1

            self.game_board[row, col] = player_identifier
            self.last_move = [row, col]
            self.moves += 1
            return True

        return False

    def animate_minimax(self):
        for col in self.get_possible_moves():

            position = self.get_position(col)

            self.game_board[position[0]][position[1]] = 12 + 5
            time.sleep(0.5)


    def reset(self):

        """
        Clear the game board and reset last_move for new game
        """

        self.game_board = np.zeros((self.rows, self.cols))
        self.last_move = None
        self.board_empty = True
        self.moves = 0



    def is_move_valid(self, col: int) -> bool:

        """
        Return True if the move (row, col) specified by move is valid. A move is valid if
        (row, col) is a valid index on the game board and (row, col) does not already have a move
        """

        if col is None:
            return False

        if col < 0 or col >= self.cols:
            return False

        # If the top row of the column is full, then the entire column is full
        return self.game_board[0][col] != 1.0 and self.game_board[0][col] != -1.0

    def is_board_empty(self) -> bool:
        return self.board_empty


    def check_winner(self) -> None|str|int:

        """
        Check whether the most recent move ended the game (win or tie).
        - If the most recent move won the game, return the identifier of the player who made the most recent move.
        - If the most recent move ended the game in a tie, return "Tie"
        - If the most recent move did not end the game, return None
        """

        if self.last_move is None:
            return None

        last_move_identifier = self.game_board[self.last_move[0]][self.last_move[1]]

        win_directions = [
            (1, 0),  # vertical win (same column different rows)
            (0, 1),  # horizontal win (same row different columns)
            (1, 1),  # diagonal win (top left to bottom right)
            (1, -1),  # diagonal win (top right to bottom left)
        ]

        # For each direction, count how many of the last player's pieces are connected in a straight line through the last move.
        # Example for (1, 0) = vertical:
        #   - Start at the last move.
        #   - Walk down (1, 0) while the same identifier continues.
        #   - Walk up (-1, 0) while the same identifier continues.
        # If the total connected count reaches the required length, we found a winner.

        for row_dir, col_dir in win_directions:
            same_identifier_count = 1

            current_row = self.last_move[0] + row_dir
            current_col = self.last_move[1] + col_dir

            while 0 <= current_row < self.rows and 0 <= current_col < self.cols:
                if self.game_board[current_row][current_col] == last_move_identifier:
                    same_identifier_count += 1
                    current_row = current_row + row_dir
                    current_col = current_col + col_dir
                else:
                    break

            current_row = self.last_move[0] - row_dir
            current_col = self.last_move[1] - col_dir

            while 0 <= current_row < self.rows and 0 <= current_col < self.cols:
                if self.game_board[current_row][current_col] == last_move_identifier:
                    same_identifier_count += 1
                    current_row = current_row - row_dir
                    current_col = current_col - col_dir
                else:
                    break

            if same_identifier_count >= constants.WIN_COUNT:
                return last_move_identifier

        # If no winner, then check for tie
        if len(self.get_possible_moves()) == 0:
            return "Tie"

        return None


    def get_possible_moves(self) -> list[int]:

        """
        Returns a list of all empty (row, col) cells
        """

        possible_moves = []
        for col in range(self.cols):
            if self.game_board[0][col] == 0:
                possible_moves.append(col)
        return possible_moves

    def get_position(self, col) -> tuple[int, int]|None:
        row = constants.NUM_ROWS - 1

        while self.game_board[row, col] != 0.0:
            row -= 1

        return row, col




