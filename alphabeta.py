import random
import math
from gomoku import GomokuGame
from copy import deepcopy

def alphabeta(game, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or game.check_win():
        return game.evaluate(), None

    validMoves = game.valid_moves()
    if not validMoves:
        return 0, None

    bestMove = None

    if maximizingPlayer:
        maxVal = -float('inf')
        for move in validMoves:
            x, y = move
            game.make_move(x, y)
            eval, _ = alphabeta(game, depth - 1, alpha, beta, False)
            game.undo_move(x, y)

            if eval > maxVal:
                maxVal = eval
                bestMove = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxVal, bestMove
    else:
        minVal = float('inf')
        for move in validMoves:
            x, y = move
            game.make_move(x, y)
            eval, _ = alphabeta(game, depth - 1, alpha, beta, True)
            game.undo_move(x, y)

            if eval < minVal:
                minVal = eval
                bestMove = move

            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minVal, bestMove

def get_best_move_alphabeta(game, depth):
    """Returns a random valid move instead of using minimax algorithm"""
    valid_moves = game.get_valid_moves()
    return random.choice(valid_moves) if valid_moves else None

