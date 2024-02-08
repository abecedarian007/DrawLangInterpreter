#  语义分析器，绘图程序

from syntax_tree import ExpressionNode
import matplotlib.pyplot as plt
import math
import numpy as np
import re
from threading import Timer


class Painter:
    def __init__(self):
        self.orx = 0.0
        self.ory = 0.0
        self.scx = 1.0
        self.scy = 1.0
        self.ang = 0.0
        self.Draw_color = (0, 0, 0)
        self.Points=dict(X=[], Y=[])

    # 语义分析和绘图

    def RotStatementpainter(self, expressions):
        z = Painter.convert_to_float(expressions)
        self.ang = z[0]

    def ScaleStatementpainter(self, expressions):
        z = Painter.convert_to_float(expressions)
        self.scx, self.scy = z[0], z[1]

    def OriginStatementpainter(self, expressions):
        z = Painter.convert_to_float(expressions)
        self.orx, self.ory = z[0], z[1]

    def ColorStatementpainter(self, expressions):
        z = Painter.convert_to_float(expressions)
        standard_red = z[0]
        standard_green = z[1]
        standard_blue = z[2]
        matplotlib_red = standard_red / 255.0
        matplotlib_green = standard_green / 255.0
        matplotlib_blue = standard_blue / 255.0
        self.Draw_color = (matplotlib_red, matplotlib_green, matplotlib_blue)
    def Set_circle_Statement(self, expressions):

        z = Painter.convert_to_float(expressions)
        self.orx, self.ory = z[0], z[1]
        self.scx, self.scy = z[2], z[3]
        self.ang = 0
        n = np.array([-3.141592653589793, 3.141592653589793, 0.06283185307179586, "COS(T)", "SIN(T)"])
        Painter.ForDrawStatementpainter(self, n)

    def ForDrawStatementpainter(self, expressions):
        z = Painter.convert_to_float(expressions)
        T_start, T_end = z[0], z[1]
        T_step = z[2]

        Point_x, Point_y = expressions[3], expressions[4]
        # if expressions[5]:
        #     # print(statement[5])
        #     self.Draw_color = expressions[5]
        self.paint(T_start, T_end, T_step, Point_x, Point_y)

    def paint(self, T_start, T_end, T_step, Point_x, Point_y):
        T_value = T_start
        # 绘制的点坐标
        while T_value <= T_end:
            x = Painter.count(T_value, Point_x)
            y = Painter.count(T_value, Point_y)
            # 比例变换
            # x, y = x * 1.0, y * 1.0
            x, y = x * self.scx, y * self.scy
            # 旋转变换
            x, y = x * math.cos(self.ang) + y * math.sin(self.ang), y * math.cos(self.ang) - x * math.sin(self.ang)
            # 平移变换
            x, y = x + self.orx, y + self.ory

            self.Points['X'].append(x)
            self.Points['Y'].append(y)
            T_value += T_step
        plt.plot(self.Points['X'], self.Points['Y'], '.', color=self.Draw_color)
        # canvas = plt.gcf().canvas
        # timer = canvas.new_timer(interval=2000)
        # timer.add_callback(lambda: plt.close())
        # timer.start()
        plt.pause(0.8)
        plt.axis('equal')
        #plt.show()


    def count(T_value, expressions):

        # 替换字符串中的T为T_value
        # 使用一个函数来动态替换T为T_value的值
        def replace_T(match):
            return str(T_value)

        replaced_expression = re.sub(r'T', replace_T, expressions)

        # 使用eval函数求值
        # result = eval(replaced_expression)
        result = Painter.calculate_expression(replaced_expression)
        return result

    def convert_to_float(expressions):
        # 将传入的字符串数字转化为float类型
        float_values = []
        for expr in expressions:
            try:
                float_value = float(expr)
                float_values.append(float_value)
            except ValueError:

                float_values.append(expr)
        return float_values

    def calculate_expression(expression):
        # 将字符串表达式中的函数名转换为小写，以便与Python内置函数匹配
        expression = expression.replace('SIN', 'math.sin')
        expression = expression.replace('COS', 'math.cos')

        # 使用eval函数计算表达式的值
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return f"Error: {e}"

