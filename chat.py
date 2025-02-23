# chat.py
from openai import OpenAI
import configparser
import os
# 读取 key.ini 文件
config = configparser.ConfigParser()
 
current_file_path = os.path.join( os.path.dirname(__file__), "key.ini")
config.read(current_file_path)

api_key = config['DEFAULT']['api_key']
base_url = config['DEFAULT']['base_url']
model = config['DEFAULT']['model']

#走deepseek模型
# base_url = "https://api.deepseek.com"
# model="deepseek-chat"
# model="deepseek-reasoner"

# 走通义千问模型
# base_url =  "https://dashscope.aliyuncs.com/compatible-mode/v1"
# model="qwen-plus"
# model="deepseek-r1"

client = OpenAI(api_key=api_key, base_url=base_url)
def parse_board(board_str):
    return [list(row.split()) for row in board_str.strip().split('\n')]

def chat_wzq(msg,model):
    user_message = msg
    board = parse_board(msg)
    
    # 获取 X 和 O 的坐标位置
    x_positions = [(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == 'X']
    o_positions = [(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == 'O']
    
    # 将坐标位置格式化为字符串
    x_positions_str = ', '.join([f"({x},{y})" for x, y in x_positions])
    o_positions_str = ', '.join([f"({x},{y})" for x, y in o_positions])
    
#     prompt ="""
#     你是一个五子棋的专家，请根据棋盘信息给出下一步棋的坐标，O代表你的棋子，X代表你的对手的棋子
#     棋盘大小为15x15，棋子只能放在棋盘上，不能超出棋盘，棋子只能放在空位上，
#     请先分析一下当前棋局的局势！！！如果三颗棋子连在一起的时候，要确保先有一个棋子拦截
#     棋子只能放在一个位置上，不能重复，棋子只能放在一个位置上，不能重复，
#     棋子只能放在一个位置上，不能重复，棋子只能放在一个位置上，不能重复，
#     出答案前先看看你要下的位置上面到底有没棋子知道不
#             对方有四个棋子连在一起的时候，请先堵住知道不！！！！不要傻b去下别的地方，
#     坐标格式为：x,y，x和y均为整数，x代表横坐标，y代表纵坐标，坐标从0开始，
#     例如：0,0代表左上角，14,14代表右下角，请给出坐标， 还有思考理由，
#     用json输出，格式如下, 
#     {
#     "coordinate": "",
#     "reason": " "
#     }

#     结果为json格式，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，不要用其他格式输出，请用json格式输出，
#     结果{ 开头哦，不要```json
#     """ 



#     prompt = """
# 你是一位五子棋专家，请根据提供的15x15棋盘信息给出下一步棋的最佳坐标。
# - 先完整的说明对手棋子的坐标位置
# - 根据提供的棋盘信息，给出下一步棋的最佳坐标。
# - O代表你的棋子，X代表对手的棋子。
# - 先回想下五子棋里的最佳实践攻略
# - 分析当前棋局局势，优先考虑防守与进攻策略。
# - 当发现三颗连续的棋子时（无论是自己的还是对方的），应采取措施阻止对方形成四连或自己尝试完成四连。
# - 若对方有四个棋子连在一起，请务必首先堵住这一威胁点。
# - 棋子只能放置在空位上，并且每个位置仅能放置一个棋子。
# - 坐标格式为"x,y"，其中x和y均为整数，从1开始计数。例如：0,0表示左上角，14,14表示右下角。
# 请以如下JSON格式输出你的选择及理由：
# {
#     "reason": "说明选择该坐标的原因",
#     "coordinate": "x,y"
   
# }
# 请严格按照上述JSON格式输出结果，以"{"开头，"}"结尾。
#     """

    prompt = f"""
    你是一位五子棋专家，请根据提供的15x15棋盘信息给出下一步棋的最佳坐标。
- 对手棋子(X)的坐标位置: {x_positions_str}
- 你的棋子(O)的坐标位置: {o_positions_str}
- 根据提供的棋盘信息，给出下一步棋的最佳坐标。
- O代表你的棋子，X代表对手的棋子。
- 先回想下五子棋里的最佳实践攻略
- 分析当前棋局局势，优先考虑防守与进攻策略。
- 当发现三颗连续的棋子时（无论是自己的还是对方的），应采取措施阻止对方形成四连或自己尝试完成四连。例如对手在(5,6)、(5,7)和(6,7)形成了一个潜在的三连威胁，我方需要在(7,8)或者(3,4)位置下手，消除隐患
- 若对方有四个棋子连在一起，请务必首先堵住这一威胁点。例如对手的棋子(X)在(3,3)、(4,4)、(5,5)、(6,6)形成了一条斜向四连，我方需要在(7,7)和(2,2)位置同时有棋子下手，消除隐患
- 坐标格式为"x,y"，其中x和y均为整数，从1开始计数。例如：0,0表示左上角，14,14表示右下角。
请以如下JSON格式输出你的选择及理由：
{{
    "reason": "说明选择该坐标的原因",
    "coordinate": "x,y"
}}
请严格按照上述JSON格式输出结果，以"{{"开头，"}}"结尾。
    """


    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_message},
    ]
    print(model)
    response = get_chat_response(messages,model)
    response=response.strip().replace('```json\n', '').replace('\n```', '') 
    return response

def get_chat_response(messages,model):
    print("start req###################################################")
    print(messages)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1.4,
        presence_penalty=2.0,
        stream=True,
        stream_options={"include_usage": True}
    )
    responseStr=''
    for chunk in response:
        print(chunk.model_dump_json())
        if chunk.choices and chunk.choices[0] :
            msg=chunk.choices[0].delta.content
            reasoning_content=None
            if hasattr(chunk.choices[0].delta,'reasoning_content'):
                reasoning_content=chunk.choices[0].delta.reasoning_content
            if q.full():
                print("队列已满，生产者等待...")
            if(reasoning_content):
                q.put(reasoning_content)
            
            if(msg):
                q.put(msg)
                print("msg:"+msg)
                responseStr+=msg
    print(responseStr)
    return responseStr
    # return response.choices[0].message.content

import time
import threading
import queue
# 创建一个队列对象
q = queue.Queue(maxsize=30)
# 创建一个事件对象
event = threading.Event()
def notify_move():
    while True:
        try:
            if q.empty():
                print("队列为空，消费者等待...")
            item = q.get(timeout=3000)  # 设置超时，避免无限期阻塞
            print(f"消费者消费了 {item}")            
            yield 'data: {} \n\n'.format(item)
            q.task_done()
        except queue.Empty:
            print("等待超时")
    # for i in range(100):
    #     event.wait()
    #     event.clear()
    #     time.sleep(1)
    #     msg ='data: 当前时间是 {}\n\n'.format(time.time())
    #     print("start notify_move:"+str(i)+": "+msg)
    #     yield 'data: {}'.format(msg)

def main():
    # 定义一个特定的棋盘状态
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'X', 'O', '.', 'O', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'X', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
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
    boardstr= '\n'.join([' '.join(row) for row in board])

    response = chat_wzq(boardstr,model=model)
    
    # 打印结果
    print(f"System's move: {response}")

if __name__ == "__main__":
    main()