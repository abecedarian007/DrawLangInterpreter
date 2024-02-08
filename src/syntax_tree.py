from src.Token import *
from sympy import symbols, sympify, sin, cos, tan, pi, E, log, exp, sqrt


# 添加一个字典来映射大写函数到 SymPy 对应的函数
FUNCTION_MAP = {
    'SIN': sin,
    'COS': cos,
    'TAN': tan,
    'PI': pi,
    'E': E,
    'LN': log,
    'EXP': exp,
    'SQRT': sqrt
}


def make_expr_node(token: Tokenization, val1=None, val2=None):
    """
    创建一个表达式节点
    """
    token_type = token.token_type
    node = ExpressionNode(token)
    if token_type == TokenType.CONSTANT:
        node.set_constant(token.value)
    elif token_type == TokenType.PARAMETER:
        node.set_parameter(token.raw)
    elif token_type == TokenType.COLOR:
        node.set_color(token.token_name)
    elif token_type == TokenType.FUNCTION:
        node.set_function(val1)
    elif token_type == TokenType.OPERATOR:
        node.set_operator(val1, val2)
    return node


class ExpressionNode:
    def __init__(self, op_token: Tokenization):
        self.OpToken = op_token
        self.Content = None

    def set_operator(self, left, right):
        assert self.OpToken.token_type == TokenType.OPERATOR
        self.Content = {'Left': left, 'Right': right}  # 二元运算符有两个孩子节点

    def set_function(self, child):
        assert self.OpToken.token_type == TokenType.FUNCTION
        self.Content = {'Child': child, 'MathFuncPtr': self.OpToken.func_ptr}  # 函数有一个孩子节点

    def set_color(self, color):
        assert self.OpToken.token_type == TokenType.COLOR
        self.Content = color

    def set_constant(self, const):
        assert self.OpToken.token_type == TokenType.CONSTANT
        self.Content = const

    def set_parameter(self, parm_ptr):
        assert self.OpToken.token_type == TokenType.PARAMETER
        self.Content = parm_ptr

    def to_string(self) -> str:
        # 检查节点类型并相应地处理
        if self.OpToken.token_type == TokenType.OPERATOR:
            left_expr = self.Content['Left'].to_string()
            right_expr = self.Content['Right'].to_string()
            return f"({left_expr} {self.OpToken.raw} {right_expr})"
        elif self.OpToken.token_type == TokenType.FUNCTION:
            child_expr = self.Content['Child'].to_string()
            # 在这里，确保所有函数名称都转换为SymPy可识别的函数
            func_name = FUNCTION_MAP.get(self.OpToken.raw.upper(), None)
            if not func_name:
                raise ValueError(f"Function {self.OpToken.raw} is not recognized.")
            return f"{func_name}({child_expr})"
        elif self.OpToken.token_type == TokenType.COLOR:
            # 对于颜色节点，返回颜色的名称或者其他字符串表示
            return f"Color-{self.Content}"
        elif self.OpToken.token_type == TokenType.CONSTANT:
            return str(self.Content)
        elif self.OpToken.token_type == TokenType.PARAMETER:
            return self.Content
        else:
            raise ValueError("Unknown node type")

    def contains_parameter(self):
        """
        检查当前节点或其任何子节点是否包含参数。
        """
        if self.OpToken.token_type == TokenType.PARAMETER:
            return True
        if self.OpToken.token_type in [TokenType.FUNCTION, TokenType.OPERATOR]:
            if 'Child' in self.Content and self.Content['Child'].contains_parameter():
                return True
            if 'Left' in self.Content and self.Content['Left'].contains_parameter():
                return True
            if 'Right' in self.Content and self.Content['Right'].contains_parameter():
                return True
        return False

    def simplify(self):
        """
        简化当前树结构，对可计算的子树化简，对于不可计算的子树保留（例如含参数的子树）
        :return: 简化后的树
        """
        # 对于常量、参数、颜色，直接返回当前节点的副本
        if self.OpToken.token_type == TokenType.CONSTANT:
            res = ExpressionNode(self.OpToken)
            res.set_constant(self.Content)
            return res
        elif self.OpToken.token_type == TokenType.PARAMETER:
            res = ExpressionNode(self.OpToken)
            res.set_parameter(self.Content)
            return res
        elif self.OpToken.token_type == TokenType.COLOR:
            res = ExpressionNode(self.OpToken)
            res.set_color(self.Content)
            return res
        # 对于函数，递归处理子节点
        elif self.OpToken.token_type == TokenType.FUNCTION:
            child_node = self.Content['Child'].simplify()
            if not child_node.contains_parameter():
                # 尝试计算函数节点的值
                try:
                    func_name = FUNCTION_MAP.get(self.OpToken.raw.upper(), None)
                    if func_name is None:
                        raise ValueError(f"Function {self.OpToken.raw} is not recognized.")
                    # 生成 SymPy 表达式
                    func_expr = func_name(sympify(child_node.to_string(), locals=FUNCTION_MAP))
                    # 计算表达式的数值，将 pi 和 E 转换为浮点数
                    evaluated_value = func_expr.evalf()
                    # 创建一个新的常量节点
                    new_const_node = ExpressionNode(
                        Tokenization(str(evaluated_value), Constant.NUMBER, TokenType.CONSTANT, evaluated_value)
                    )
                    new_const_node.set_constant(evaluated_value)
                    return new_const_node
                except Exception as e:
                    print(f"Unable to evaluate function {self.OpToken.raw}: {e}")
            # 如果含有参数或无法计算，返回原函数节点
            new_node = ExpressionNode(self.OpToken)
            new_node.set_function(child_node)
            return new_node
        # 对于二元运算符，递归处理左右子节点
        elif self.OpToken.token_type == TokenType.OPERATOR:
            left_node = self.Content['Left'].simplify()
            right_node = self.Content['Right'].simplify()

            try:
                # 将节点转换为 SymPy 表达式
                if not left_node.contains_parameter() and not right_node.contains_parameter():
                    left_expr = sympify(left_node.to_string(), locals=FUNCTION_MAP)
                    right_expr = sympify(right_node.to_string(), locals=FUNCTION_MAP)
                    combined_expr = f"{left_expr} {self.OpToken.raw} {right_expr}"
                    simplified_expr = float(sympify(combined_expr, locals=FUNCTION_MAP).evalf())
                    new_const_node = ExpressionNode(
                        Tokenization(str(simplified_expr), Constant.NUMBER, TokenType.CONSTANT, simplified_expr)
                    )
                    new_const_node.set_constant(simplified_expr)
                    return new_const_node
                elif not left_node.contains_parameter() and right_node.contains_parameter():
                    # 对单边为0的表达式处理
                    if float(left_node.Content) == 0.0:
                        right_expr = sympify(right_node.to_string(), locals=FUNCTION_MAP)
                        combined_expr = f"0 {self.OpToken.raw} {right_expr}"
                        simplified_expr = sympify(combined_expr, locals=FUNCTION_MAP)
                        new_const_node = ExpressionNode(
                            Tokenization(str(simplified_expr), Parameter.T_EXPRESSION, TokenType.PARAMETER,
                                         simplified_expr)
                        )
                        new_const_node.set_parameter(simplified_expr)
                        return new_const_node
                    # 单边不为0
                    left_expr = sympify(left_node.to_string(), locals=FUNCTION_MAP)
                    left_expr_simplified = float(left_expr.evalf())
                    new_left_node = ExpressionNode(
                        Tokenization(str(left_expr_simplified), Constant.NUMBER, TokenType.CONSTANT,
                                     left_expr_simplified)
                    )
                    new_left_node.set_constant(left_expr_simplified)
                    new_op_node = ExpressionNode(self.OpToken)
                    new_op_node.set_operator(new_left_node, right_node)
                    return new_op_node
                elif left_node.contains_parameter() and not right_node.contains_parameter():
                    # 对单边含为0的表达式处理
                    if float(right_node.Content) == 0.0:
                        left_expr = sympify(left_node.to_string(), locals=FUNCTION_MAP)
                        combined_expr = f"{left_expr} {self.OpToken.raw} 0"
                        simplified_expr = sympify(combined_expr, locals=FUNCTION_MAP)
                        new_const_node = ExpressionNode(
                            Tokenization(str(simplified_expr), Parameter.T_EXPRESSION, TokenType.PARAMETER,
                                         simplified_expr)
                        )
                        new_const_node.set_parameter(simplified_expr)
                        return new_const_node
                    # 单边不为0
                    right_expr = sympify(right_node.to_string(), locals=FUNCTION_MAP)
                    right_expr_simplified = float(right_expr.evalf())
                    new_right_node = ExpressionNode(
                        Tokenization(str(right_expr_simplified), Constant.NUMBER, TokenType.CONSTANT,
                                     right_expr_simplified)
                    )
                    new_right_node.set_constant(right_expr_simplified)
                    new_op_node = ExpressionNode(self.OpToken)
                    new_op_node.set_operator(left_node, new_right_node)
                    return new_op_node
                else:
                    left_expr = sympify(left_node.to_string(), locals=FUNCTION_MAP)
                    right_expr = sympify(right_node.to_string(), locals=FUNCTION_MAP)
                    combined_expr = f"{left_expr} {self.OpToken.raw} {right_expr}"
                    simplified_expr = sympify(combined_expr, locals=FUNCTION_MAP)
                    new_const_node = ExpressionNode(
                        Tokenization(str(simplified_expr), Parameter.T_EXPRESSION, TokenType.PARAMETER, simplified_expr)
                    )
                    new_const_node.set_parameter(simplified_expr)
                    return new_const_node

            except Exception as e:
                print(f"Error simplifying expression: {e}")
                # 如果无法简化，返回包含原操作符和简化子节点的新节点
                new_op_node = ExpressionNode(self.OpToken)
                new_op_node.set_operator(left_node, right_node)
                return new_op_node
        else:
            raise ValueError("Unknown node type")

    def evaluate(self) -> str:
        """
        用于生成可评估的字符串表达式
        :return: 表达式的字符串
        """
        if self.OpToken.token_type == TokenType.CONSTANT:
            return str(sympify(self.Content).evalf())
        elif self.OpToken.token_type == TokenType.PARAMETER:
            return str(self.Content)
        elif self.OpToken.token_type == TokenType.COLOR:
            return str(self.Content.name)
        elif self.OpToken.token_type == TokenType.FUNCTION:
            return f"{self.OpToken.raw}({self.Content['Child'].evaluate()})"
        elif self.OpToken.token_type == TokenType.OPERATOR:
            return f"({self.Content['Left'].evaluate()} {self.OpToken.raw} {self.Content['Right'].evaluate()})"
        else:
            raise ValueError("Unknown node type")

    def getValue(self):
        # 叶子节点，直接返回他自己
        if self.lson == None and self.rson == None:
            if self.OpToken.token_type == TokenType.CONSTANT:
                return self.OpToken.value
            elif self.OpToken.token_type == TokenType.PARAMETER:
                return ExpressionNode.T_value
            else:
                print("Expression Error")
                exit(-1)

        # 只有左子树	函数节点	or +5 or -5
        elif self.rson == None:
            if self.OpToken.token_name == Operator.PLUS:
                return self.lson.getValue()
            elif self.OpToken.token_name == Operator.MINUS:
                return -self.lson.getValue()
            elif self.OpToken.token_type == TokenType.FUNCTION:
                return self.OpToken.func_ptr(self.lson.getValue())
            else:
                print("Expression Error")
                exit(-1)
        # 只有右子树
        elif self.lson == None:
            if self.OpToken.token_name == Operator.PLUS:
                return self.rson.getValue()
            elif self.OpToken.token_name == Operator.MINUS:
                return -self.rson.getValue()
            elif self.OpToken.token_type == TokenType.FUNCTION:
                return self.OpToken.func_ptr(self.rson.getValue())
            else:
                print("Expression Error")
        # 左右子树都有的时候计算+ — * / **的值
        else:
            if self.OpToken.token_name == Operator.PLUS:
                return self.lson.getValue() + self.rson.getValue()
            elif self.OpToken.token_name == Operator.MINUS:
                return self.lson.getValue() - self.rson.getValue()
            elif self.OpToken.token_name == Operator.MULTIPLY:
                return self.lson.getValue() * self.rson.getValue()
            elif self.OpToken.token_name == Operator.DIVIDE:
                return self.lson.getValue() / self.rson.getValue()
            elif self.OpToken.token_name == Operator.POWER:
                return self.lson.getValue() ** self.rson.getValue()
            else:
                print("Expression Error")
                exit(-1)
