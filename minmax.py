import math
import random
from gomoku import GomokuGame

def minimax(game, depth, maximizingPlayer):
    if depth == 0 or game.check_win():
        return game.evaluate() , None

    validMoves = game.valid_moves()
    if not validMoves:
        return 0 , None

    bestMove = None

    if maximizingPlayer:
        maxVal = -float('inf')
        for move in validMoves:
            x , y = move
            game.make_move(x, y)
            eval = minimax(game , depth - 1 , False)
            game.undo_move(x,y)

            if eval > maxVal:
                maxVal = eval
                bestMove = move
        return maxVal , bestMove
    else:
        minVal = float('inf')
        for move in validMoves:
            x , y = move
            game.make_move(x,y)
            eval = minimax(game , depth - 1 , True)
            game.undo_move(x,y)
            if eval < minVal:
                eval = minVal
                bestMove = move

        return eval , bestMove

def get_best_move_minimax(game, depth):
    """Returns a random valid move instead of using minimax algorithm"""
    valid_moves = game.get_valid_moves()
    return random.choice(valid_moves) if valid_moves else None
