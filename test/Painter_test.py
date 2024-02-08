import re
import math
from matplotlib import pyplot as plt
from src.lexer import tokenize
from Parser_test_Uptobottom import Parser
from src.Token import *

class Interpreter:
    def __init__(self):
        # 初始化绘图参数
        self.origin_x = 0
        self.origin_y = 0
        self.scale_x = 1
        self.scale_y = 1
        self.rot_angle = 0
        self.commands = []

    def set_origin(self, x, y):
        self.origin_x = x
        self.origin_y = y

    def set_scale(self, sx, sy):
        self.scale_x = sx
        self.scale_y = sy

    def set_rotation(self, angle):
        self.rot_angle = angle

    def transform(self, x, y):
        # 比例变换
        x_scaled = x * self.scale_x
        y_scaled = y * self.scale_y
        # 旋转变换
        x_rot = x_scaled * math.cos(self.rot_angle) - y_scaled * math.sin(self.rot_angle)
        y_rot = x_scaled * math.sin(self.rot_angle) + y_scaled * math.cos(self.rot_angle)
        # 平移变换
        x_trans = x_rot + self.origin_x
        y_trans = y_rot + self.origin_y

        return x_trans, y_trans

    def execute_command(self, cmd_type, cmd_value):
        if cmd_type == ReservedWord.ORIGIN:
            self.set_origin(*cmd_value)
        elif cmd_type == ReservedWord.SCALE:
            self.set_scale(*cmd_value)
        elif cmd_type == ReservedWord.ROT:
            self.set_rotation(cmd_value)
        elif cmd_type == ReservedWord.FOR:
            self.commands.append(cmd_value)

    def draw(self):
        plt.figure(figsize=(6, 6))
        for command in self.commands:
            # 假设命令是一系列点
            transformed_points = [self.transform(x, y) for x, y in command]
            xs, ys = zip(*transformed_points)
            plt.plot(xs, ys)

        plt.show()
    def interpret(self, code):
        # 词法分析
        tokens = tokenize(code)
        # 语法分析
        parser = Parser(iter(tokens))
        parsed_data = parser.parse()
        print(parsed_data)
        # 执行命令
        for cmd_type, cmd_value in parsed_data:
            self.execute_command(cmd_type, cmd_value)

        # 绘图
        self.draw()

# 示例代码
code = """ORIGIN IS (300, 300);
SCALE IS (1, 1);
"""

interpreter = Interpreter()
interpreter.interpret(code)  # 解释并绘制图形

