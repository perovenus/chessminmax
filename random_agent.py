import random

class RandomPlayer():
    def __init__(self) -> None:
        pass
    def get_move(self, board):
        move = random.choice(list(board.legal_moves))
        return move