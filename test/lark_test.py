from lark import Lark, Transformer, v_args, Token, Tree
import math
import matplotlib.pyplot as plt

# 定义语法
grammar = """
    start: statement+

    statement: for_statement
             | scale_statement
             | origin_statement
             | rotation_statement

    for_statement: "FOR" "T" "FROM" expr "TO" expr "STEP" expr "DRAW" "(" expr "," expr ")" ";"
    scale_statement: "SCALE" "IS" "(" expr "," expr ")" ";"
    origin_statement: "ORIGIN" "IS" "(" expr "," expr ")" ";"
    rotation_statement: "ROT" "IS" expr ";"

    expr: term ((PLUS | MINUS) term)*
    term: factor ((MUL | DIV) factor)*
    factor: NUMBER | "(" expr ")" | func | PI | T | SEMICOLON
    func: FUNC "(" expr ")"

    FUNC: "sin" | "cos" | "tan" | "sqrt"
    PLUS: "+"
    MINUS: "-"
    MUL: "*"
    DIV: "/"
    PI: "PI"
    T: "T"
    NUMBER: /-?\d+(\.\d+)?/
    SEMICOLON:";"

    %import common.WS
    %ignore WS
"""

# 创建解析器
parser = Lark(grammar, start='start')


# 定义 Transformer
class CalculateTree(Transformer):
    def __init__(self):
        self.origin = (0, 0)
        self.scale = (1, 1)
        self.rotation = 0
        self.x_values = []
        self.y_values = []

    def start(self, items):
        # 绘图逻辑
        plt.plot(self.x_values, self.y_values)
        plt.show()
        return items

    def for_statement(self, items):
        # 解析 FOR 语句，执行绘图逻辑
        start, end, step, x_expr, y_expr = items
        t = start
        while t <= end:
            x = self.evaluate_expression(x_expr, t)
            y = self.evaluate_expression(y_expr, t)
            self.x_values.append(x)
            self.y_values.append(y)
            t += step
        return 'For-Loop Executed'

    def scale_statement(self, items):
        # 设置缩放
        self.scale = (items[0], items[1])
        return f'Scale set to {self.scale}'

    def origin_statement(self, items):
        # 设置原点
        self.origin = (items[0], items[1])
        return f'Origin set to {self.origin}'

    def rotation_statement(self, items):
        # 设置旋转
        self.rotation = items[0]
        return f'Rotation set to {self.rotation} degrees'

    def expr(self, items):
        if len(items) == 1:
            return items[0]
        op = items[1]
        if op == '+':
            return items[0] + items[2]
        elif op == '-':
            return items[0] - items[2]

    def term(self, items):
        # if len(items) == 1:
        #     return items[0]
        # op = items[1]
        # if op == '*':
        #     return items[0] * items[2]
        # elif op == '/':
        #     return items[0] / items[2]
        if len(items) == 1:
            return self.evaluate_expression(items[0])
        left = self.evaluate_expression(items[0])
        right = self.evaluate_expression(items[2])
        op = items[1]
        if op == '*':
            return left * right
        elif op == '/':
            return left / right

    def factor(self, items):
        if len(items) == 1:
            if isinstance(items[0], Token) and items[0].type == 'PI':
                return math.pi
            return items[0]
        return self.evaluate_expression(items[1])

    def func(self, items):
        # func, value = items
        # if func == 'sin':
        #     return math.sin(value)
        # elif func == 'cos':
        #     return math.cos(value)
        # elif func == 'tan':
        #     return math.tan(value)
        # elif func == 'sqrt':
        #     return math.sqrt(value)

        # func_name, expr = items
        # value = self.evaluate_expression(expr)  # 计算表达式的值
        #
        # # 确保 value 是一个数值
        # if value is None:
        #     raise ValueError(f"Invalid value for function {func_name}: {value}")
        #
        # # 根据函数名调用相应的数学函数
        # if func_name == 'sin':
        #     return math.sin(value)
        # elif func_name == 'cos':
        #     return math.cos(value)
        # 添加对其他数学函数的处理

        #
        # func_name, expr = items
        # value = self.evaluate_expression(expr[0])  # 确保正确地计算表达式的值
        #
        # if value is None:
        #     raise ValueError(f"Invalid value for function {func_name}: {value}")
        #
        # # 根据函数名调用相应的数学函数
        # if func_name.value == 'sin':
        #     return math.sin(value)
        # elif func_name.value == 'cos':
        #     return math.cos(value)

        func_name, expr = items

        # 确保 expr 不是 None 且可下标访问
        if expr is None or not isinstance(expr, (list, Tree)):
            raise ValueError(f"Invalid expression for function {func_name.value}: {expr}")

        value = self.evaluate_expression(expr[0])  # 计算 expr 的第一个元素

        if value is None:
            raise ValueError(f"Invalid value for function {func_name.value}: {value}")

        # 根据函数名调用相应的数学函数
        if func_name.value == 'sin':
            return math.sin(value)
        elif func_name.value == 'cos':
            return math.cos(value)

    def evaluate_expression(self, expr, t=None):
        # 根据表达式树计算结果
        # if isinstance(tree, float):
        #     return tree
        # if tree.data == 'expr':
        #     return self.expr(tree.children)
        # elif tree.data == 'term':
        #     return self.term(tree.children)
        # elif tree.data == 'factor':
        #     return self.factor(tree.children)
        # elif tree.data == 'func':
        #     func = tree.children[0].value
        #     value = self.evaluate_expression(tree.children[1].children[0], t)
        #     return self.func([func, value])
        # elif tree.data == 'NUMBER':
        #     return float(tree.children[0])

        # if isinstance(expr, float):
        #     return expr
        #
        #     # 如果 expr 是一个 Token，根据其类型返回相应的值
        # if isinstance(expr, Token):
        #     if expr.type == 'NUMBER':
        #         return float(expr.value)
        #     elif expr.type == 'PI':
        #         return math.pi
        #
        #     # 如果 expr 是一个表达式节点，根据其类型递归计算
        # data = expr.data
        # children = expr.children
        #
        # if data == 'expr':
        #     return self.expr(children, t)
        # elif data == 'term':
        #     return self.term(children, t)
        # elif data == 'factor':
        #     return self.factor(children, t)
        # elif data == 'func':
        #     return self.func(children, t)

        # def evaluate_expression(self, expr, t=None):
        #     # 如果 expr 是一个 Token 对象，根据其类型返回相应的值
        #     if isinstance(expr, Token):
        #         if expr.type == 'NUMBER':
        #             return float(expr.value)
        #         elif expr.type == 'PI':
        #             return math.pi
        #
        #     # 如果 expr 是一个 Tree 对象，根据其类型递归计算
        #     elif isinstance(expr, Tree):
        #         data = expr.data
        #         children = expr.children
        #
        #         if data == 'expr':
        #             return self.expr(children, t)
        #         elif data == 'term':
        #             return self.term(children, t)
        #         elif data == 'factor':
        #             return self.factor(children, t)
        #         elif data == 'func':
        #             return self.func(children, t)
        #         # 添加其他必要的逻辑以处理不同类型的表达式
        #
        #     # 如果 expr 是基本数值类型，直接返回
        #     elif isinstance(expr, (int, float)):
        #         return expr

        # if isinstance(expr, Token):
        #     if expr.type == 'NUMBER':
        #         return float(expr.value)
        #     elif expr.type == 'PI':
        #         return math.pi
        #
        # elif isinstance(expr, Tree):
        #     data = expr.data
        #     children = expr.children
        #
        #     if data == 'expr':
        #         return self.expr(children, t)
        #     elif data == 'term':
        #         return self.term(children, t)
        #     elif data == 'factor':
        #         return self.factor(children, t)
        #     elif data == 'func':
        #         return self.func(children, t)
        #     # 其他情况的处理
        # elif isinstance(expr, (int, float)):
        #     return expr
        #
        #     # 如果没有匹配的情况，返回 None 或抛出异常
        # return None  # 或抛出异常
        if expr is None:
            return None

        if isinstance(expr, Token):
            if expr.type == 'NUMBER':
                return float(expr.value)
            elif expr.type == 'PI':
                return math.pi

        elif isinstance(expr, Tree):
            data = expr.data
            children = expr.children

            if data == 'expr':
                return self.expr(children, t)
            elif data == 'term':
                return self.term(children, t)
            elif data == 'factor':
                return self.factor(children, t)
            elif data == 'func':
                return self.func(children, t)

            # 如果 expr 是一个基本数值类型
        elif isinstance(expr, (int, float)):
            return expr

            # 如果没有匹配的情况，返回 None 或抛出异常
        return None


# 测试代码
source_code = """
FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (cos(T), sin(T));
SCALE IS (100, 100);
ORIGIN IS (360, 240);
ROT IS PI/2;
"""


def analyze_code(code):
    tree = parser.parse(code)
    print("语法树：")
    print(tree.pretty())
    print("\n词法记号：")
    for token in tree.scan_values(lambda v: isinstance(v, Token)):
        print(token)


analyze_code(source_code)
tree = parser.parse(source_code)
calculate = CalculateTree()
result = calculate.transform(tree)
print(result)
