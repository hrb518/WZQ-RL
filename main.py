from flask import Flask,Response, render_template, request, jsonify, session,stream_with_context
import os
import chat
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个密钥用于session加密

class Gomoku:
    def __init__(self, size=15):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.history = []

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == '.'

    def prev(self):
        x,y,player= self.history.pop()
        self.board[x][y]= '.'
        self.current_player = player



    def make_move(self, x, y):
        if self.is_valid_move(x, y):
            self.history.append((x, y,self.current_player))
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

    def make_random_move(self):
        empty_cells = [(x, y) for x in range(self.size) for y in range(self.size) if self.is_valid_move(x, y)]
        if empty_cells:
            x, y = random.choice(empty_cells)
            result = self.make_move(x, y)
            return result
        return None
    
 

    def chat_wzq(self,model):
        error_pos=''
        for i in range(5):
            msg= '\n'.join([' '.join(row) for row in self.board])
            msg += error_pos
            json_result_str= chat.chat_wzq(msg,model)    
            json_result=json.loads(json_result_str)

            coordinate_str=json_result['coordinate']
            x, y = map(int, coordinate_str.split(','))
            if self.is_valid_move(x, y):
                result = self.make_move(x, y)
                return result,json_result
            else:
                error_pos="\n 不要再下这个位置 "+coordinate_str+" 这个地方已经有棋子了啊"
                print("Invalid move. Try again.")
        return None,json.loads('{"reason":"Invalid move. Try again."}')

def get_game_from_session():
    if 'game' in session:
        game_data = session['game']
        game = Gomoku()
        game.board = game_data['board']
        game.current_player = game_data['current_player']
        if 'history' in game_data:
            game.history = game_data['history']
        else: 
            game.history=[]
        return game
    else:
        game = Gomoku()
        session['game'] = {'board': game.board, 'current_player': game.current_player,'history': game.history}
        return game

def save_game_to_session(game):

    session['game'] = {'board': game.board, 'current_player': game.current_player,'history': game.history}

@app.route('/')
def index():
    game = get_game_from_session()
    current_file_path = os.path.abspath(__file__)
    return render_template('wzq.html', board=game.board, 
                           history=game.history, 
                           current_player=game.current_player, current_file_path=current_file_path)

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    x, y = data['x'], data['y']
    game = get_game_from_session()
    result = game.make_move(x, y)
    save_game_to_session(game)
    if result:
        return jsonify({'board': game.board, 'current_player': game.current_player, 'result': result,'history':game.history})
    return jsonify({'board': game.board, 'current_player': game.current_player, 'result': result,'history':game.history})


@app.route('/systemMove', methods=['POST'])
def system_move():
    data = request.get_json()
    model = data['model']
    game = get_game_from_session()
    try:
        system_result,json_result = game.chat_wzq(model)
        if system_result:
            return jsonify({'board': game.board, 'current_player': game.current_player, 'result': system_result,"json_result":json_result,'history':game.history})
        else:
            save_game_to_session(game)
            return jsonify({'board': game.board, 'current_player': game.current_player, 'result': '',"json_result":json_result,'history':game.history})

    except Exception as e:
        print(f"Error : {e}")
        system_result = None
        return jsonify({'board': game.board, 'current_player': game.current_player, 'result': system_result,"json_result":"e",'history':game.history})
    

@app.route('/reset', methods=['POST'])
def reset():
    game = Gomoku()
    save_game_to_session(game)
    return jsonify({'board': game.board, 'current_player': game.current_player})

@app.route('/prev', methods=['POST'])
def prev():
    game = get_game_from_session()
    game.prev()
    save_game_to_session(game)
    return jsonify({'board': game.board, 'current_player': game.current_player,'history':game.history})

 

import time
# 路由到SSE服务端点
@app.route('/stream_response')
def stream():
    return Response(stream_with_context(chat.notify_move()), content_type='text/event-stream')



if __name__ == "__main__":
    app.run(debug=True, threaded=True)