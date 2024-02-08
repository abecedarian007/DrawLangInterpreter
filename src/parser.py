from typing import Optional, Iterator
import numpy as np

from src.Token import *
import src.lexer as lex
from src.syntax_tree import ExpressionNode, make_expr_node
from src.painter import Painter

TokenNameType = Union[Constant, Parameter, Function, ReservedWord, Operator, Seperator, Color, OtherToken]


class Parser:

    def __init__(self):
        self.token_list: Optional[Iterator[Tokenization]] = None  # 初始化为空列表，用于存储token
        self.current_token: Optional[Tokenization] = None  # 初始化为None，表示当前没有token
        self.pen = None  # 画笔

    def init_token_list(self, input_code: str):
        token_list = iter(lex.tokenize(input_code))  # 调用词法分析，返回输入代码分析后的token列表，并转换为一个可迭代的对象
        if token_list is None:
            raise ValueError("Invalid token_name list.")
        self.token_list = token_list  # 确保token_list是一个列表
        self.next_token()  # 载入第一个token

    def match_token(self, token_name: TokenNameType):
        if self.current_token is not None and self.current_token.token_name != token_name:
            print(f"[SyntaxError] Expected token {token_name.name.upper()}, "
                  f"found {self.current_token.raw.upper()}")
            raise SyntaxError(f"Expected token_name type: {token_name.name}.")
        elif self.current_token is None:
            print(f"[SyntaxError] Expected {token_name.name.upper()}")
            raise SyntaxError(f"[SyntaxError] Expected {token_name.name.upper()}")
        self.next_token()  # 当前匹配成功，解析下一个token

    def next_token(self):
        if self.token_list is None:
            raise RuntimeError("Token iterator is not initialized.")
        self.current_token = next(self.token_list, None)

    def parse(self, input_code: str, draw=False) -> None:
        """
        从语法层面解析输入的代码
        :param draw: 是否进行绘图
        :param input_code: 输入的代码
        :return: None
        """
        self.init_token_list(input_code)
        if draw:
            self.pen = Painter()
            self.pen.__init__()
        self.program(draw)

    def program(self, draw=False) -> None:
        """
        Grammar-EBNF:
            Program → { Statement SEMICOLON }
        :return: None
        """
        print("Entering Program")

        while self.current_token is not None and self.current_token.token_type != TokenType.NONE:
            self.statement(draw)
            self.match_token(Seperator.SEMICOLON)

        if self.current_token is not None and self.current_token.token_type == TokenType.NONE:
            print(f"[SyntaxError] Unknown word: {self.current_token.raw.upper()}")
            raise SyntaxError(f"Unknown word: {self.current_token.raw.upper()}")

        print("Exiting Program")

    def statement(self, draw=False) -> None:
        """
        Grammar-EBNF:
            Statement → OriginStatement
                        | ScaleStatement
                        | RotStatement
                        | ForStatement
                        | ColorStatement
        :return: None
        """
        print("Entering Statement")

        if self.current_token.token_name == ReservedWord.ORIGIN:
            self.origin_statement(draw)
        elif self.current_token.token_name == ReservedWord.SCALE:
            self.scale_statement(draw)
        elif self.current_token.token_name == ReservedWord.ROT:
            self.rot_statement(draw)
        elif self.current_token.token_name == ReservedWord.FOR:
            self.for_draw_statement(draw)
        elif self.current_token.token_name == ReservedWord.COLOR:
            self.color_statement(draw)
        elif self.current_token.token_name == ReservedWord.SET_CIRCLE:
            self.set_circle_statement(draw)
        else:
            print("[SyntaxError] Invalid statement.")
            raise SyntaxError("Invalid statement.")

        print("Exiting Statement")

    def origin_statement(self, draw=False) -> None:
        """
        Syntax:
            ORIGIN IS (横坐标, 纵坐标);
        Grammar-EBNF:
            OriginStatement → ORIGIN IS LEFT_BRACKET Expression COMMA Expression RIGHT_BRACKET
        :return: None
        """
        print("Entering OriginStatement")

        self.match_token(ReservedWord.ORIGIN)
        self.match_token(ReservedWord.IS)
        self.match_token(Seperator.LEFT_BRACKET)
        x_exp = self.expression()
        self.match_token(Seperator.COMMA)
        y_exp = self.expression()
        self.match_token(Seperator.RIGHT_BRACKET)

        # x_str = x_exp.to_string()
        # y_str = y_exp.to_string()
        x_val = x_exp.simplify().evaluate().upper()
        y_val = y_exp.simplify().evaluate().upper()

        # print(f"OriginStatement: ORIGIN IS ({x_str}, {y_str})")
        print(f"OriginStatement: ORIGIN IS ({x_val}, {y_val})")
        print("Exiting OriginStatement")

        if draw:
            z = np.array([x_val, y_val])
            Painter.OriginStatementpainter(self.pen, z)

    def scale_statement(self, draw=False) -> None:
        """
        Syntax:
            SCALE IS (横坐标比例因子, 纵坐标比例因子);
        Grammar-EBNF:
            ScaleStatement → SCALE IS LEFT_BRACKET Expression COMMA Expression RIGHT_BRACKET
        :return: None
        """
        print("Entering ScaleStatement")

        self.match_token(ReservedWord.SCALE)
        self.match_token(ReservedWord.IS)
        self.match_token(Seperator.LEFT_BRACKET)
        abscissa_scale_exp = self.expression()
        self.match_token(Seperator.COMMA)
        ordinate_scale_exp = self.expression()
        self.match_token(Seperator.RIGHT_BRACKET)

        # abscissa_scale_str = abscissa_scale_exp.to_string()
        # ordinate_scale_str = ordinate_scale_exp.to_string()
        abscissa_scale_val = abscissa_scale_exp.simplify().evaluate().upper()
        ordinate_scale_val = ordinate_scale_exp.simplify().evaluate().upper()

        # print(f"ScaleStatement: SCALE IS ({abscissa_scale_str}, {ordinate_scale_str})")
        print(f"ScaleStatement: SCALE IS ({abscissa_scale_val}, {ordinate_scale_val})")
        print("Exiting ScaleStatement")

        if draw:
            z = np.array([abscissa_scale_val, ordinate_scale_val])
            Painter.ScaleStatementpainter(self.pen, z)

    def rot_statement(self, draw=False) -> None:
        """
        Syntax:
            ROT IS 弧度值;
        Grammar-EBNF:
            RotStatement → ROT IS Expression
        :return: None
        """
        print("Entering RotStatement")

        self.match_token(ReservedWord.ROT)
        self.match_token(ReservedWord.IS)
        radian_exp = self.expression()

        # radian_str = radian_exp.to_string()
        radian_val = radian_exp.simplify().evaluate().upper()

        # print(f"RotStatement: ROT IS {radian_str}")
        print(f"RotStatement: ROT IS {radian_val}")
        print("Exiting RotStatement")

        if draw:
            z = np.array([radian_val])
            Painter.RotStatementpainter(self.pen, z)

    def for_draw_statement(self, draw=False) -> None:
        """
        Syntax:
            FOR T FROM 起点 TO 终点 STEP 步长 DRAW(横坐标, 纵坐标);
        Grammar-EBNF:
            ForDrawStatement → FOR T FROM Expression TO  Expression STEP Expression
            DRAW LEFT_BRACKET Expression COMMA Expression RIGHT_BRACKET
        :return: None
        """
        print("Entering ForDrawStatement")

        self.match_token(ReservedWord.FOR)
        self.match_token(Parameter.T)
        self.match_token(ReservedWord.FROM)
        start_exp = self.expression()
        self.match_token(ReservedWord.TO)
        end_exp = self.expression()
        self.match_token(ReservedWord.STEP)
        step_exp = self.expression()
        self.match_token(ReservedWord.DRAW)
        self.match_token(Seperator.LEFT_BRACKET)
        x_exp = self.expression()
        self.match_token(Seperator.COMMA)
        y_exp = self.expression()
        self.match_token(Seperator.RIGHT_BRACKET)

        # start_str = start_exp.to_string()
        # end_str = end_exp.to_string()
        # step_str = step_exp.to_string()
        # x_str = x_exp.to_string()
        # y_str = y_exp.to_string()
        start_val = start_exp.simplify().evaluate().upper()
        end_val = end_exp.simplify().evaluate().upper()
        step_val = step_exp.simplify().evaluate().upper()
        x_val = x_exp.simplify().evaluate().upper()
        y_val = y_exp.simplify().evaluate().upper()

        # print(f"ForDrawStatement: FOR T FROM {start_str} TO {end_str} STEP {step_str} DRAW({x_str}, {y_str})")
        print(f"ForDrawStatement: FOR T FROM {start_val} TO {end_val} STEP {step_val} DRAW({x_val}, {y_val})")
        print("Exiting ForDrawStatement")

        if draw:
            z = np.array([start_val, end_val, step_val, x_val, y_val])
            Painter.ForDrawStatementpainter(self.pen, z)

    def color_statement(self, draw=False) -> None:
        """
        Syntax:
            COLOR IS 颜色;
            | COLOR IS (R, G, B);
        Grammar-EBNF:
            ColorStatement → COLOR IS Expression
                            | COLOR IS LEFT_BRACKET Expression COMMA Expression COMMA Expression RIGHT_BRACKET
        :return: None
        """
        print("Entering ColorStatement")

        self.match_token(ReservedWord.COLOR)
        self.match_token(ReservedWord.IS)
        if self.current_token is not None and self.current_token.token_name == Seperator.LEFT_BRACKET:
            self.match_token(Seperator.LEFT_BRACKET)
            r_exp = self.expression()
            self.match_token(Seperator.COMMA)
            g_exp = self.expression()
            self.match_token(Seperator.COMMA)
            b_exp = self.expression()
            self.match_token(Seperator.RIGHT_BRACKET)

            r_val = r_exp.simplify().evaluate().upper()
            g_val = g_exp.simplify().evaluate().upper()
            b_val = b_exp.simplify().evaluate().upper()

            print(f"ColorStatement: COLOR IS ({r_val}, {g_val}, {b_val})")

            if draw:
                z = np.array([r_val, g_val, b_val])
                Painter.ColorStatementpainter(self.pen, z)

        elif self.current_token is not None and self.current_token.token_type == TokenType.COLOR:
            color_exp = self.expression()

            # color_str = color_exp.to_string()
            color_val = color_exp.simplify().evaluate().upper()

            # print(f"ColorStatement: COLOR {color_str}")
            print(f"ColorStatement: COLOR IS {color_val}")

            if draw:
                z = str(color_val)
                Painter.ColorStatementpainter(self.pen, z)
        else:
            print("[SyntaxError] Expected a valid color expression.")
            raise SyntaxError("Expected a valid color expression.")

        print("Exiting ColorStatement")

    def set_circle_statement(self, draw=False) -> None:
        """
        Syntax:
            SET_CIRCLE (横坐标, 纵坐标) RADIUS (x半径, y半径);
        Grammar-EBNF:
            SetCircleStatement → SET_CIRCLE LEFT_BRACKET Expression COMMA Expression RIGHT_BRACKET
                                    RADIUS LEFT_BRACKET Expression COMMA Expression RIGHT_BRACKET;
        :return: None
        """
        print("Entering SetCircleStatement")

        self.match_token(ReservedWord.SET_CIRCLE)
        self.match_token(Seperator.LEFT_BRACKET)
        x_exp = self.expression()
        self.match_token(Seperator.COMMA)
        y_exp = self.expression()
        self.match_token(Seperator.RIGHT_BRACKET)
        self.match_token(ReservedWord.RADIUS)
        self.match_token(Seperator.LEFT_BRACKET)
        x_radius_exp = self.expression()
        self.match_token(Seperator.COMMA)
        y_radius_exp = self.expression()
        self.match_token(Seperator.RIGHT_BRACKET)

        # x_str = x_exp.to_string()
        # y_str = y_exp.to_string()
        # x_radius_str = x_radius_exp.to_string()
        # y_radius_str = y_radius_exp.to_string()
        x_val = x_exp.simplify().evaluate().upper()
        y_val = y_exp.simplify().evaluate().upper()
        x_radius_val = x_radius_exp.simplify().evaluate().upper()
        y_radius_val = y_radius_exp.simplify().evaluate().upper()

        # print(f"SetCircleStatement: SET_CIRCLE ({x_str}, {y_str}) RADIUS ({x_radius_val}, {y_radius_val})")
        print(f"SetCircleStatement: SET_CIRCLE ({x_val}, {y_val}) RADIUS ({x_radius_val}, {y_radius_val})")
        print("Exiting SetCircleStatement")

        if draw:

            z = np.array([x_val, y_val, x_radius_val, y_radius_val])
            print(z)
            Painter.Set_circle_Statement(self.pen, z)

    def expression(self) -> ExpressionNode:
        """
        Grammar-EBNF:
            Expression → Color
                        | Term { ( PLUS | MINUS ) Term }
        :return: ExpressionNode
        """
        if self.current_token is not None:
            if self.current_token.token_type == TokenType.COLOR:
                curr_token = self.current_token
                self.next_token()
                return make_expr_node(curr_token)
            else:
                left_node = self.term()

                while (self.current_token is not None
                       and self.current_token.token_name in
                       (Operator.PLUS, Operator.MINUS, Operator.NEGATIVE, Operator.NEGATIVE)):
                    operator_token = self.current_token
                    self.match_token(operator_token.token_name)
                    right_node = self.term()
                    # 根据操作符创建表达式节点
                    left_node = make_expr_node(operator_token, left_node, right_node)
                return left_node
        else:
            print("[SyntaxError] Expected a valid expression.")
            raise SyntaxError("Expected a valid expression.")

    def term(self) -> ExpressionNode:
        """
        Grammar-EBNF:
            Term → Factor { ( MUL | DIV ) Factor }
        :return: ExpressionNode
        """
        left_node = self.factor()
        while self.current_token is not None and self.current_token.token_name in (Operator.MULTIPLY, Operator.DIVIDE):
            operator_token = self.current_token
            self.match_token(operator_token.token_name)
            right_node = self.factor()
            # 根据操作符创建表达式节点
            left_node = make_expr_node(operator_token, left_node, right_node)
        return left_node

    def factor(self) -> ExpressionNode:
        """
        Grammar-EBNF:
            Factor → ( PLUS | MINUS ) Factor
                    | Component
        :return: ExpressionNode
        """
        # 检查是否存在一元操作符 PLUS 或 MINUS
        if self.current_token.token_name == Operator.POSITIVE:
            # 对于正号，我们可以忽略它，因为正号不改变数值的符号
            self.next_token()  # 移动到下一个令牌
            return self.factor()  # 递归调用 factor 方法
        elif self.current_token.token_name == Operator.NEGATIVE:
            # 对于负号，我们可以创建一个从0减去该数值的表达式节点来表示负数
            operator_token = self.current_token
            self.next_token()  # 移动到下一个令牌
            node = self.factor()  # 递归调用 factor 方法来获取负号右边的表达式
            # 创建一个代表0 - node的表达式节点
            zero_node = make_expr_node(Tokenization(0, Constant.NUMBER, TokenType.CONSTANT, 0))
            return make_expr_node(operator_token, val1=zero_node, val2=node)
        else:
            # 如果没有一元操作符，直接处理组件
            return self.component()

    def component(self) -> ExpressionNode:
        """
        Grammar-EBNF:
            Component → Atom [ POWER Component ]
        :return: ExpressionNode
        """
        left_node = self.atom()
        if self.current_token is not None and self.current_token.token_name == Operator.POWER:
            operator_token = self.current_token
            self.next_token()
            exponent_node = self.component()
            left_node = make_expr_node(operator_token, left_node, exponent_node)
        return left_node

    def atom(self) -> ExpressionNode:
        """
        Grammar-EBNF:
            Atom → CONSTANT
                  | T
                  | FUNCTION LEFT_BRACKET Expression RIGHT_BRACKET
                  | LEFT_BRACKET Expression RIGHT_BRACKET
        :return: ExpressionNode
        """
        curr_token = self.current_token
        if curr_token.token_type == TokenType.CONSTANT:
            self.next_token()
            return make_expr_node(curr_token)
        elif curr_token.token_type == TokenType.PARAMETER:
            self.next_token()
            return make_expr_node(curr_token)
        elif curr_token.token_type == TokenType.FUNCTION:
            self.next_token()
            self.match_token(Seperator.LEFT_BRACKET)
            node = self.expression()
            self.match_token(Seperator.RIGHT_BRACKET)
            return make_expr_node(curr_token, val1=node)
        elif curr_token.token_name == Seperator.LEFT_BRACKET:
            self.next_token()
            node = self.expression()
            self.match_token(Seperator.RIGHT_BRACKET)
            return node
        else:
            print("[SyntaxError] Unexpected token in atom.")
            raise SyntaxError("Unexpected token_name in atom.")


# 测试

# code = """ROT IS -pi/2;
# for t from 0 to pi step 0.001 draw (t*cos(t), t*sin(t));
# for t from 0 to pi step 0.001 draw (t*cos(t), -t*sin(t));
#
# ROT IS -pi/2+pi/12;
# for t from 0 to pi step 0.001 draw (t*cos(t), t*sin(t));
# for t from 0 to pi step 0.001 draw (t*cos(t), -t*sin(t));
#
# ROT IS -pi/2-pi/12;
# for t from 0 to pi step 0.001 draw (t*cos(t), t*sin(t));
# for t from 0 to pi step 0.001 draw (t*cos(t), -t*sin(t));
# """

# code = """ORIGIN IS (+50*sin(pi/2), -50*sqrt(4)/2);
# ROT IS pi;
# SCALE IS (20*2**2+20, (-100+200)*2);
# COLOR BLUE;
# // this is a comment
# FOR T FROM 0 TO 2 STEP 0.001 DRAW ((2*2-3)*cos(T), pi+T);
# SET_CIRCLE (10,10) RADIUS (2, 6);
# """

# code = """for t from 0 to 2*pi step pi/200 draw(16*(sin(t)**3), 13*cos(t) - 5*cos(2*t) - 2*cos(3*t)-cos(4*t));
# """

# code = """COLOR IS red;
# """
#
# parser = Parser()
# parser.parse(code, draw=False)
