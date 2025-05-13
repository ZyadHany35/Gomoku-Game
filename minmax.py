# import math
# import random
# from gomoku import GomokuGame
#
# def minimax(game, depth, maximizingPlayer):
#     if depth == 0 or game.check_win():
#         return game.evaluate(game) , None
#
#     validMoves = game.get_valid_moves()
#     if not validMoves:
#         return 0 , None
#
#     bestMove = None
#
#     if maximizingPlayer:
#         maxVal = -float('inf')
#         for move in validMoves:
#             x , y = move
#             game.make_move(x, y)
#             eval = minimax(game , depth - 1 , False)
#             game.undo_move(x,y)
#
#             if eval > maxVal:
#                 maxVal = eval
#                 bestMove = move
#         return maxVal , bestMove
#     else:
#         minVal = float('inf')
#         for move in validMoves:
#             x , y = move
#             game.make_move(x,y)
#             eval = minimax(game , depth - 1 , True)
#             game.undo_move(x,y)
#             if eval < minVal:
#                 eval = minVal
#                 bestMove = move
#
#         return eval , bestMove
#
# def get_best_move_minimax(game, depth):
#     _ , bestMove = minimax(game, depth, True)
#     return bestMove