class AIPlayer:
    def __init__(self , player , algo = "minimax" , depth = 2):
        self.player = player
        self.algo = algo
        self.depth = depth

    def minmax(self , game , depth , maximizingPlayer):
        if depth == 0 or game.check_win():
            return game.evaluate(self.player), None

        validMoves = game.get_valid_moves()
        if not validMoves:
            return 0 , None

        bestMove = None

        if maximizingPlayer:
            maxVal = -float('inf')
            for move in validMoves:
                x , y = move
                game.make_move(x, y)
                eval , _ = self.minmax(game , depth - 1 , False)
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
                eval , _ = self.minmax(game , depth - 1 , True)
                game.undo_move(x,y)

                if eval < minVal:
                    minVal = eval
                    bestMove = move

            return minVal , bestMove

    def alphabeta(self , game, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or game.check_win():
            return game.evaluate(self.player), None

        validMoves = game.get_valid_moves()
        if not validMoves:
            return 0, None

        bestMove = None

        if maximizingPlayer:
            maxVal = -float('inf')
            for move in validMoves:
                x, y = move
                game.make_move(x, y)
                eval, _ = self.alphabeta(game, depth - 1, alpha, beta, False)
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
                eval, _ = self.alphabeta(game, depth - 1, alpha, beta, True)
                game.undo_move(x, y)

                if eval < minVal:
                    minVal = eval
                    bestMove = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minVal, bestMove

def get_best_move_minimax(game , depth):
    ai = AIPlayer(game.current_player , "minimax" , depth)
    _ , move = ai.minmax(game , depth , True)
    return move

def get_best_move_alphabeta(game , depth):
    ai = AIPlayer(game.current_player , "alpha-beta" , depth)
    _ , move = ai.alphabeta(game , depth , -float('inf'), float('inf'), True)
    return move
