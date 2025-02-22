# 五子棋游戏实现

class Gomoku:
    def __init__(self, size=15):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == '.'

    def make_move(self, x, y):
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            if self.check_winner(x, y):
                self.print_board()
                print(f"Player {self.current_player} wins!")
                return True
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            print("Invalid move. Try again.")
        return False

    def check_winner(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 5):
                nx, ny = x + dx * i, y + dy * i
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                nx, ny = x - dx * i, y - dy * i
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def play(self):
        while True:
            self.print_board()
            try:
                x, y = map(int, input(f"Player {self.current_player}, enter your move (row col): ").split())
                if self.make_move(x, y):
                    break
            except ValueError:
                print("Invalid input. Please enter two integers separated by a space.")

if __name__ == "__main__":
    game = Gomoku()
    game.play()