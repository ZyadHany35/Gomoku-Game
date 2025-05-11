import random
from copy import deepcopy

def alphabeta(game, depth, alpha, beta, maximizing_player):
    return

def get_best_move_alphabeta(game, depth):
    """Returns a random valid move instead of using minimax algorithm"""
    valid_moves = game.get_valid_moves()
    return random.choice(valid_moves) if valid_moves else None

