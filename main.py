from time import sleep
import minimax_agent
import random_agent
import chess
from setup import *


def main():
    p.init()
    PLAYER = True
    screen = p.display.set_mode((WIDTH, HEIGHT))
    board = chess.Board()
    player1 = minimax_agent.MinMaxPlayer(PLAYER)
    player2 = random_agent.RandomPlayer()
    drawboard(screen)
    loadImage()
    while not board.is_game_over():
        if board.turn == player1.player:
            move = player1.get_move(board, 1)
            board.push(move)
        else:
            move = player2.get_move(board)
            board.push(move)
        drawpiece(screen, convert_to_int(board))
        p.display.flip()
        sleep(0.5)
    print(board.result())


main()
