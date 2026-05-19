import copy
import random

from player_base import Player
from board import Board
from game_manager import GameDifficulty


class AIPlayer(Player):
    def __init__(self, is_player_one, choose_random_move):
        super().__init__(is_player_one)
        self.is_ai_player = True
        self.choose_random_move = choose_random_move
        self.is_minimaxing = True
        if choose_random_move:
            self.is_minimaxing = False
        self.max_move_look_ahead = 3
        self.scaling = 4 # keep as a multiple of 2 ALWAYS!!!!!!!!!!!!!!!!!!!!!!!

        self.testing_diagnostics = {
            "wins" : 0,
            "losses" : 0,
            "ties" : 0,
        }

    def choose_move(self, board, move_input, difficulty) -> tuple[int, int] | None:

        if self.choose_random_move:
            moves = board.get_possible_moves()
            random_move = random.choice(moves)
            return random_move
        else:
            best_move = self.find_best_move(board)
            if difficulty == "HARD":
                if board.moves % self.scaling == 1:
                    self.max_move_look_ahead += 1
            else:
                self.max_move_look_ahead = 3

            return best_move



    def find_best_move(self, board) -> tuple[int, int] | None:

        possible_moves = board.get_possible_moves()

        opponent_identifier = self.get_other_player_identifier()

        print(self.max_move_look_ahead)


        if len(possible_moves) == 0:
            print("No possible moves - This should not happen.")
            return None


        if board.is_board_empty():
            return random.choice(possible_moves)

        max_score = float("-inf")
        best_move = None

        non_zero_score_change = False

        for col in possible_moves:


            board_copy = copy.deepcopy(board)
            move = col
            board_copy.apply_move(move, self.identifier)

            position = board.get_position(move)

            score = self.minimax(board_copy, 0, is_maximizing=False, opponent_identifier=opponent_identifier, alpha=float("-inf"), beta=float("inf"))

            # board.game_board[position[0]][position[1]] = 12 + score
            # 12 because score is +- 10, so the lowest it could be is 2. So we check if
            # the board at that position is greater than 2, then we subtract that value by 12
            # EX: score is 7, so board[position[0]][position[1]] = 19
            # 19 - 12 = 7, so it will display a 7
            # EX: score is -4, so board[position[0]][position[1]] = 8
            # 8 - 12 = -4, so it will display a -4

            if score > max_score:

                if max_score > float("-inf"):
                    non_zero_score_change = True

                max_score = score
                best_move = col

        # if not non_zero_score_change:
        #     best_move = random.choice(possible_moves)

        return best_move

    def evaluate(self, board: Board, depth: int, opponent_identifier: int) -> int|None:

        winner_identifier = board.check_winner()
        if winner_identifier == self.identifier:
            return 10 - depth
        elif winner_identifier == opponent_identifier:
            return -10 + depth

        if len(board.get_possible_moves()) == 0:
            return 0

        if depth >= self.max_move_look_ahead:
            return 0
            # return self.score_position(board.game_board, self.identifier)


        return None


    def minimax(self, board: Board, depth: int, is_maximizing: bool, opponent_identifier: int, alpha: float, beta: float) -> int:

        score = self.evaluate(board, depth, opponent_identifier)
        if score is not None:
            return score

        if len(board.get_possible_moves()) == 0:
            print("Minimax: No possible moves - This should not happen.")
            return 0

        if is_maximizing:

            max_score = float("-inf")

            for col in board.get_possible_moves():

                board_copy = copy.deepcopy(board)
                move = col
                board_copy.apply_move(move, self.identifier)

                score = self.minimax(board_copy, depth + 1, not is_maximizing, opponent_identifier, alpha, beta)

                max_score = max(max_score, score)

                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break

            return max_score

        else:

            min_score = float("inf")

            for col in board.get_possible_moves():

                board_copy = copy.deepcopy(board)
                move = col
                board_copy.apply_move(move, opponent_identifier)

                score = self.minimax(board_copy, depth + 1, not is_maximizing, opponent_identifier, alpha, beta)

                min_score = min(min_score, score)

                beta = min(beta, min_score)
                if beta <= alpha:
                    break

            return min_score

    def score_position(self, board, identifier):
        values = [2, 3, 4, 5, 4, 3, 2]
        highest_value = 2
        print(board)
        for row, col in board:
            if board[row][col] == identifier:
                if values[col] > highest_value:
                    highest_value = values[col]

        return highest_value



    def update_testing_diagnostics(self, last_game_result):

        if last_game_result in self.testing_diagnostics:
            self.testing_diagnostics[last_game_result] += 1

        player = "player 1" if self.is_player_one else "player 2"
        ai_mode = "choose random move" if self.choose_random_move else "minimax"
        print("-------------------------------------------------")
        print(f"Testing diagnostics for {player}:")
        print(f"AI mode: {ai_mode}")
        print(f"wins: {self.testing_diagnostics['wins']}, losses: {self.testing_diagnostics['losses']}, ties: {self.testing_diagnostics['ties']}")