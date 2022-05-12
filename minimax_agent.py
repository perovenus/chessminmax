from chess import Board, Move
import chess
import math
from move_ordeing import organize_moves, organize_moves_quiescence
from PeSTOS import board_evaluation
from constants import (CHECKMATE_SCORE, CHECKMATE_THRESHOLD, NULL_MOVE_R,
                       QUIESCENCE_SEARCH_DEPTH)
from random import choice


class MinMaxPlayer():
    def __init__(self, player) -> None:
        self.player = player

    def random_move(self, board: Board):
        move = choice([move for move in board.legal_moves])
        return move

    def quiescence_search(self, board: Board, depth: int, alpha: float, beta: float) -> float:
        if board.is_stalemate():
            return 0

        if board.is_checkmate():
            return -CHECKMATE_SCORE

        stand_pat = board_evaluation(board)

        # recursion base case
        if depth == 0:
            return stand_pat

        # beta-cutoff
        if(stand_pat >= beta):
            return beta

        # alpha update
        if(alpha < stand_pat):
            alpha = stand_pat

        # get moves for quiescence search
        moves = organize_moves_quiescence(board)

        for move in moves:
            # make move and get score
            board.push(move)
            score = -self.quiescence_search(board, -beta, -alpha, depth-1)
            board.pop()

            # beta-cutoff
            if(score >= beta):
                return beta

            # alpha-update
            if(score > alpha):
                alpha = score

        return alpha

    def negamax(self, board: Board, depth: int, null_move: bool, alpha: float = float("-inf"), beta: float = float("inf")):
        # check if board was already evaluated

        if board.is_checkmate():
            return (-CHECKMATE_SCORE, None)

        if board.is_stalemate():
            return (0, None)

        # recursion base case
        if depth <= 0:
            # evaluate current board
            board_score = self.quiescence_search(
                board, alpha, beta, QUIESCENCE_SEARCH_DEPTH)
            return board_score, None

        # null move prunning
        if null_move and depth >= (NULL_MOVE_R+1) and not board.is_check():
            board_score = board_evaluation(board)
            if board_score >= beta:
                board.push(Move.null())
                board_score = - \
                    self.negamax(board, depth - 1 - NULL_MOVE_R,
                                 False,  -beta, -beta+1)[0]
                board.pop()
                if board_score >= beta:
                    return beta, None

        best_move = None

        # initializing best_score
        best_score = float("-inf")
        moves = organize_moves(board)

        for move in moves:
            # make the move
            board.push(move)

            board_score = - \
                self.negamax(board, depth-1, null_move, -beta, -alpha)[0]
            if board_score > CHECKMATE_THRESHOLD:
                board_score -= 1
            if board_score < -CHECKMATE_THRESHOLD:
                board_score += 1

            # take move back
            board.pop()

            # beta-cutoff
            if board_score >= beta:
                return board_score, move

            # update best move
            if board_score > best_score:
                best_score = board_score
                best_move = move

            # setting alpha variable to do pruning
            alpha = max(alpha, board_score)

            # alpha beta pruning when we already found a solution that is at least as good as the current one
            # those branches won't be able to influence the final decision so we don't need to waste time analyzing them
            if alpha >= beta:
                break

        # if no best move, make a random one
        if not best_move:
            best_move = self.random_move(board)

        # save result before returning
        return best_score, best_move

    def get_move(self, board: Board, depth: int):
        return self.negamax(board, depth, True)[1]
