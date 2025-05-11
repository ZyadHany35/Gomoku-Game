# gomoku_solver/gomoku.py
class GomokuGame:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.current_player = 1

    def reset(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 1

    def make_move(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size and self.board[y][x] == 0:
            self.board[y][x] = self.current_player
            self.current_player = 3 - self.current_player
            return True
        return False

    def undo_move(self, x, y):
        self.board[y][x] = 0
        self.current_player = 3 - self.current_player

    def get_valid_moves(self):
        moves = []
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == 0:
                    moves.append((x, y))
        return moves

    def check_win(self):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] != 0:
                    player = self.board[y][x]
                    for dx, dy in directions:
                        if self.count_stones(x, y, dx, dy, player) >= 5:
                            return True
        return False

    def count_stones(self, x, y, dx, dy, player):
        count = 0
        for i in range(5):
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == player:
                count += 1
            else:
                break
        return count

    def evaluate(self, player):
        opponent = 3 - player
        player_score = self.count_sequences(player)
        opponent_score = self.count_sequences(opponent)
        return player_score - opponent_score

    def count_sequences(self, player):
        count = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == player:
                    for dx, dy in directions:
                        if self.check_sequence(x, y, dx, dy, player):
                            count += 1
        return count

    def check_sequence(self, x, y, dx, dy, player):
        length = 0
        for i in range(4):
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == player:
                length += 1
            else:
                break
        return length >= 4
