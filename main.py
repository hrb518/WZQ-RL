from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

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
                return f"Player {self.current_player} wins!"
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            return "Invalid move. Try again."
        return None

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

@app.route('/')
def index():
    game = Gomoku()
    current_file_path = os.path.abspath(__file__)
    return render_template('wzq.html', board=game.board, current_player=game.current_player,current_file_path=current_file_path)

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    x, y = data['x'], data['y']
    game = Gomoku()
    result = game.make_move(x, y)
    return jsonify({'board': game.board, 'current_player': game.current_player, 'result': result})

if __name__ == "__main__":
    app.run(debug=True)