import enum
import math
from typing import Union
from sympy import pi, E


class Constant(enum.Enum):
    NUMBER = r'\d+(\.\d*)?'
    PI = "pi"
    E = "e"


class Parameter(enum.Enum):
    T = "T"
    T_EXPRESSION = "op_func(T)"


class Function(enum.Enum):
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    LN = "ln"
    SQRT = "sqrt"
    EXP = "exp"


class ReservedWord(enum.Enum):
    ORIGIN = "ORIGIN"
    SCALE = "SCALE"
    ROT = "ROT"
    IS = "IS"
    FOR = "FOR"
    FROM = "FROM"
    TO = "TO"
    STEP = "STEP"
    DRAW = "DRAW"
    COLOR = "COLOR"
    SET_CIRCLE = "SET CIRCLE"
    RADIUS = "RADIUS"


class Operator(enum.Enum):
    POSITIVE = "+_"
    NEGATIVE = "-_"
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "**"


class Seperator(enum.Enum):
    COMMA = ","
    SEMICOLON = ";"
    LEFT_BRACKET = "("
    RIGHT_BRACKET = ")"
    NEWLINE = "\n"
    RETURN = "\r"


class Color(enum.Enum):
    RED = "RED"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    WHITE = "WHITE"
    BLACK = "BLACK"


class OtherToken(enum.Enum):
    COMMENT = "//"
    NONE_TOKEN = ""


TokenNameType = Union[Constant, Parameter, Function, ReservedWord, Operator, Seperator, Color, OtherToken]


class TokenType(enum.Enum):
    NONE = 0            # None token_name
    CONSTANT = 1        # 常量：数字、pi、e
    PARAMETER = 2       # 参数：T
    FUNCTION = 3        # 函数：sin、cos、tan、ln、sqrt、exp
    RESERVED_WORD = 4   # 保留字：ORIGIN, SCALE, ROT, IS, FOR, FROM, TO, STEP, DRAW
    OPERATOR = 5        # 运算符：+ - * / **
    SEPERATOR = 6       # 分隔符：; ( )
    COLOR = 7           # 颜色
    COMMENT = 8         # 注释


class Tokenization:
    def __init__(self, raw, token_name: TokenNameType, token_type: TokenType, value=0.0, func_ptr=None):
        self.raw = raw
        self.token_name = token_name
        self.token_type = token_type
        self.value = value
        self.func_ptr = func_ptr

    def show(self):
        # print(self.raw, self.token_name.name, self.token_type.name, self.value, self.func_ptr)
        print(f"{self.raw:<10} {self.token_name.name:<15} {self.token_type.name:<15}")


def mark_token(token_type, raw):
    token_type = token_type.upper()
    if token_type == "NUMBER":
        return Tokenization(raw, Constant.NUMBER, TokenType.CONSTANT, raw)
    elif token_type == "PI":
        return Tokenization(raw, Constant.PI, TokenType.CONSTANT, pi)
    elif token_type == "E":
        return Tokenization(raw, Constant.E, TokenType.CONSTANT, E)
    elif token_type == "T":
        return Tokenization(raw, Parameter.T, TokenType.PARAMETER)
    elif token_type == "SIN":
        return Tokenization(raw, Function.SIN, TokenType.FUNCTION, 0, math.sin)
    elif token_type == "COS":
        return Tokenization(raw, Function.COS, TokenType.FUNCTION, 0, math.cos)
    elif token_type == "TAN":
        return Tokenization(raw, Function.TAN, TokenType.FUNCTION, 0, math.tan)
    elif token_type == "LN":
        return Tokenization(raw, Function.LN, TokenType.FUNCTION, 0, math.log)
    elif token_type == "SQRT":
        return Tokenization(raw, Function.SQRT, TokenType.FUNCTION, 0, math.sqrt)
    elif token_type == "EXP":
        return Tokenization(raw, Function.EXP, TokenType.FUNCTION, 0, math.exp)
    elif token_type == "ORIGIN":
        return Tokenization(raw, ReservedWord.ORIGIN, TokenType.RESERVED_WORD)
    elif token_type == "SCALE":
        return Tokenization(raw, ReservedWord.SCALE, TokenType.RESERVED_WORD)
    elif token_type == "ROT":
        return Tokenization(raw, ReservedWord.ROT, TokenType.RESERVED_WORD)
    elif token_type == "IS":
        return Tokenization(raw, ReservedWord.IS, TokenType.RESERVED_WORD)
    elif token_type == "FOR":
        return Tokenization(raw, ReservedWord.FOR, TokenType.RESERVED_WORD)
    elif token_type == "FROM":
        return Tokenization(raw, ReservedWord.FROM, TokenType.RESERVED_WORD)
    elif token_type == "TO":
        return Tokenization(raw, ReservedWord.TO, TokenType.RESERVED_WORD)
    elif token_type == "STEP":
        return Tokenization(raw, ReservedWord.STEP, TokenType.RESERVED_WORD)
    elif token_type == "DRAW":
        return Tokenization(raw, ReservedWord.DRAW, TokenType.RESERVED_WORD)
    elif token_type == "COLOR":
        return Tokenization(raw, ReservedWord.COLOR, TokenType.RESERVED_WORD)
    elif token_type == "SET_CIRCLE":
        return Tokenization(raw, ReservedWord.SET_CIRCLE, TokenType.RESERVED_WORD)
    elif token_type == "RADIUS":
        return Tokenization(raw, ReservedWord.RADIUS, TokenType.RESERVED_WORD)
    elif token_type == "POSITIVE":
        return Tokenization(raw, Operator.POSITIVE, TokenType.OPERATOR, 0)
    elif token_type == "NEGATIVE":
        return Tokenization(raw, Operator.NEGATIVE, TokenType.OPERATOR, 0)
    elif token_type == "PLUS":
        return Tokenization(raw, Operator.PLUS, TokenType.OPERATOR, 0)
    elif token_type == "MINUS":
        return Tokenization(raw, Operator.MINUS, TokenType.OPERATOR, 0)
    elif token_type == "MULTIPLY":
        return Tokenization(raw, Operator.MULTIPLY, TokenType.OPERATOR, 0)
    elif token_type == "DIVIDE":
        return Tokenization(raw, Operator.DIVIDE, TokenType.OPERATOR, 0)
    elif token_type == "POWER":
        return Tokenization(raw, Operator.POWER, TokenType.OPERATOR, 0, math.pow)
    elif token_type == "COMMA":
        return Tokenization(raw, Seperator.COMMA, TokenType.SEPERATOR)
    elif token_type == "SEMICOLON":
        return Tokenization(raw, Seperator.SEMICOLON, TokenType.SEPERATOR)
    elif token_type == "LEFT_BRACKET":
        return Tokenization(raw, Seperator.LEFT_BRACKET, TokenType.SEPERATOR)
    elif token_type == "RIGHT_BRACKET":
        return Tokenization(raw, Seperator.RIGHT_BRACKET, TokenType.SEPERATOR)
    elif token_type == "NEWLINE":
        return Tokenization(raw, Seperator.NEWLINE, TokenType.SEPERATOR)
    elif token_type == "RETURN":
        return Tokenization(raw, Seperator.RETURN, TokenType.SEPERATOR)
    elif token_type == "COMMENT":
        return Tokenization(raw, OtherToken.COMMENT, TokenType.COMMENT)
    elif token_type == "RED":
        return Tokenization(raw, Color.RED, TokenType.COLOR)
    elif token_type == "BLUE":
        return Tokenization(raw, Color.BLUE, TokenType.COLOR)
    elif token_type == "YELLOW":
        return Tokenization(raw, Color.YELLOW, TokenType.COLOR)
    elif token_type == "GREEN":
        return Tokenization(raw, Color.GREEN, TokenType.COLOR)
    elif token_type == "WHITE":
        return Tokenization(raw, Color.WHITE, TokenType.COLOR)
    elif token_type == "BLACK":
        return Tokenization(raw, Color.BLACK, TokenType.COLOR)
    elif token_type == "MISMATCH":
        return Tokenization(raw, OtherToken.NONE_TOKEN, TokenType.NONE)
    else:
        raise ValueError("TokenType ERROR!")
