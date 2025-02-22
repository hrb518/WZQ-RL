# chat.py
from openai import OpenAI
import configparser
import os
# 读取 key.ini 文件
config = configparser.ConfigParser()
 
current_file_path = os.path.join( os.path.dirname(__file__), "key.ini")
config.read(current_file_path)

api_key = config['DEFAULT']['api_key']

#走deepseek模型
model="deepseek-chat"
base_url = "https://api.deepseek.com"


# 走通义千问模型
base_url =  "https://dashscope.aliyuncs.com/compatible-mode/v1"
model="qwen-plus"


client = OpenAI(api_key=api_key, base_url=base_url)

def chat_wzq(msg):
    user_message = msg
    prompt ="""
    你是一个五子棋的专家，请根据棋盘信息给出下一步棋的坐标，你是下O"""  """的选手
    坐标格式为：x,y，x和y均为整数，x代表横坐标，y代表纵坐标，坐标从0开始，
    例如：0,0代表左上角，14,14代表右下角，请给出坐标， 还有思考理由，
    用json输出，格式如下, 
    {
    "coordinate": "",
    "reason": " "
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
    print(messages)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
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