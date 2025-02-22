# chat.py
from openai import OpenAI
import configparser
import os
# 读取 key.ini 文件
config = configparser.ConfigParser()
 
current_file_path = os.path.join( os.path.dirname(__file__), "key.ini")
config.read(current_file_path)

api_key = config['DEFAULT']['api_key']
base_url = "https://api.deepseek.com"

client = OpenAI(api_key=api_key, base_url=base_url)

def board_to_string(board):
    return '\n'.join([' '.join(row) for row in board])

def chat_wzq(board):
    user_message = board_to_string(board)
    prompt ="""
    你是一个五子棋的专家，请根据棋盘信息给出下一步棋的坐标，你是下O的选手
    坐标格式为：x,y，x和y均为整数，x代表横坐标，y代表纵坐标，坐标从0开始，
    例如：0,0代表左上角，14,14代表右下角，请给出坐标， 还有思考理由，
    用json输出，格式如下, 
    {
    "coordinate": "5,5",
    "reason": "当前棋盘上，X在(4,3)和(6,5)有两个棋子，形成了一个潜在的三连线。为了防止X在下一步形成四连线，O应该在(5,5)落子，这样可以同时阻止X在水平和垂直方向上的进攻。此外，这个位置也为O自己创造了一个潜在的三连线机会。"
    }

    结果为json格式，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，
    结果{ 开头哦，不要```json
    """ 
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_message},
    ]
    response = get_chat_response(messages)
    return response

def get_chat_response(messages):
    print("start req###################################################")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )
    print(response)
    return response.choices[0].message.content

def main():
    # 定义一个特定的棋盘状态
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'X', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', 'X', 'O', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    # 调用 chat_wzq 函数
    response = chat_wzq(board)
    
    # 打印结果
    print(f"System's move: {response}")

if __name__ == "__main__":
    main()