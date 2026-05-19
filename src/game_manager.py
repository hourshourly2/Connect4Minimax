from board import Board
from enum import Enum


"""
game_manager.py

GameManager runs the turn-based game loop logic (NOT the pygame loop).

Responsibilities:
- Owns the Board and the two Player objects
- Tracks whose turn it is
- Asks the current player to choose a move
- Applies the move to the board (using board.apply_move)
- Checks for a winner/tie after each valid move
- Switches turns when the game continues
- During AI training: records AI states and feeds rewards when the game ends

Important:
- GameManager contains no rendering or pygame code.
- Player objects only CHOOSE moves. GameManager applies moves and advances the game.
"""



class GameState(Enum):
    PLAYING = 0     # game is active, moves are still being applied
    GAME_OVER = 1   # a player has won the game, or game ended in a tie
    RESET = 2       # waiting to reset (waiting to start a new game)


class GameManager:

    def __init__(self, player1, player2):
        self.board = Board()

        # players can either be Human or AI players
        self.player1 = player1
        self.player2 = player2

        self.current_player = self.player1
        self.game_state = GameState.PLAYING
        self.training_identifier = 2


    def animate_minimax(self):
        self.board.animate_minimax()


    def update(self, pending_move):

        """
        Advance the game by at most ONE move.

        pending_move: Human player only - (x, y) mouse click pixels

        Each move follows the following rules:
        1. Ask the current player to choose a move
        2. Apply the chosen move to the board
        3. If move was valid:
            - If current player is AI player record the move state
            - Check for game over (winner or tie)
            - If game over:
                - AI players feed reward
                - restart game
            - If not game over then set current player to other player

        """


        if self.game_state != GameState.PLAYING:
            return

        chosen_move = self.current_player.choose_move(self.board, pending_move)

        if self.board.apply_move(chosen_move, self.current_player.identifier):

            winner = self.board.check_winner()
            self.board.board_empty = False
            if winner is not None:
                self.update_ai_player_testing_diagnostics(winner)
                self.game_state = GameState.GAME_OVER
            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1




    def update_ai_player_testing_diagnostics(self, winning_player_identifier):
        if winning_player_identifier == "Tie":
            if self.player1.is_ai_player:
                self.player1.update_testing_diagnostics("ties")
            if self.player2.is_ai_player:
                self.player2.update_testing_diagnostics("ties")
        elif winning_player_identifier == self.player1.identifier:
            if self.player1.is_ai_player:
                self.player1.update_testing_diagnostics("wins")
            if self.player2.is_ai_player:
                self.player2.update_testing_diagnostics("losses")
        elif winning_player_identifier == self.player2.identifier:
            if self.player1.is_ai_player:
                self.player1.update_testing_diagnostics("losses")
            if self.player2.is_ai_player:
                self.player2.update_testing_diagnostics("wins")



    def is_player_one_turn(self):
        return self.current_player == self.player1

    def is_player_two_turn(self):
        return self.current_player == self.player2

    def player_one_won(self):
        winner = self.board.check_winner()
        return winner == self.player1.identifier

    def player_two_won(self):
        winner = self.board.check_winner()
        return winner == self.player2.identifier

    def reset(self):

        """
        Reset the game back to a fresh starting state.

        - Clears the board
        - Sets the turn back to player1
        - Returns the game to PLAYING
        """

        self.board.reset()
        self.game_state = GameState.PLAYING

        if self.player1.is_minimaxing:
            self.player1.max_move_look_ahead = 2
        if self.player2.is_minimaxing:
            self.player2.max_move_look_ahead = 2



        self.current_player = self.player1

