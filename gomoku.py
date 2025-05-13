
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
                        if self.count_balls(x, y, dx, dy, player) >= 5:
                            return True
        return False

    def count_balls(self, x, y, dx, dy, player):
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
        player_score = self.evaluate_player(player)
        opponent_score = self.evaluate_player(opponent)
        return player_score - opponent_score

    def evaluate_player(self, player):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (-1, -1)]

        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] != player:
                    continue
                for dx, dy in directions:
                    length, open_ends = self.count_seq(x, y, dx, dy, player)
                    if length >= 5:
                        score += 100000  # Win
                    elif length == 4 and open_ends == 2:
                        score += 10000  # Open four
                    elif length == 4 and open_ends == 1:
                        score += 5000  # Closed four
                    elif length == 3 and open_ends == 2:
                        score += 2500  # Open three
                    elif length == 3 and open_ends == 1:
                        score += 1250
                    elif length == 2 and open_ends == 2:
                        score += 625
                    elif length == 2 and open_ends == 1:
                        score += 300
                    elif length == 1 and open_ends == 2:
                        score += 150
                    elif length == 1 and open_ends == 1:
                        score += 100
        return score

    def count_seq(self, x, y, dx, dy, player):
        len = 0
        open_ends = 0

        # Move backward to the beginning of the sequence
        nx, ny = x, y
        while self.isValid(nx - dx, ny - dy) and self.board[ny - dy][nx - dx] == player:
            nx -= dx
            ny -= dy

        # Count the sequence
        cur_x, cur_y = nx, ny
        while self.isValid(cur_x, cur_y) and self.board[cur_y][cur_x] == player:
            len += 1
            cur_x += dx
            cur_y += dy

        # Check open ends
        if self.isValid(nx - dx, ny - dy) and self.board[ny - dy][nx - dx] == 0:
            open_ends += 1
        if self.isValid(cur_x, cur_y) and self.board[cur_y][cur_x] == 0:
            open_ends += 1

        return len, open_ends

    def isValid(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

