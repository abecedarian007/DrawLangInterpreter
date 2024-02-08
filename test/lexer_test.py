import re
import math
# 定义记号规格 元组
import enum

# class TokenType(enum.Enum):
#     NUMBER = r'\d+(\.\d*)?'
#     ASSIGN = r'IS'
#     END = r';'
#     FOR = r'FOR'
#     ROT = r'ROT'
#     SCALE = r'SCALE'
#     ORIGIN = r'ORIGIN'
#     DRAW = r'DRAW'
#     TO = r'TO'
#     STEP = r'STEP'
#     OPEN = r'\('
#     CLOSE = r'\)'
#     COMMA = r','
#     OP = r'[+\-*/]'
#     VAR = r'[a-zA-Z_]\w*'
#     SKIP = r'[ \t]+'
#     NEWLINE = r'\n'
#     MISMATCH = r'.'

class Token:
    def __init__(self,tokentype,lexeme,value=0.0):
        self.tokentype = tokentype
        self.lexeme= lexeme
        self.value = value

TOKEN_SPECIFICATION = [
    ('NUMBER',    r'\d+(\.\d*)?'),   # 整数或者小数
    ('IS',        r'IS'),
    ('END',       r';'),
    ('FROM',      r'FROM'),
    ('FOR',       r'FOR'),
    ('ROT',       r'ROT'),
    ('SCALE',     r'SCALE'),
    ('ORIGIN',    r'ORIGIN'),
    ('DRAW',      r'DRAW'),
    ('TO',        r'TO'),
    ('T',         r'T'),
    ('STEP',      r'STEP'),
    ('OPEN',      r'\('),
    ('CLOSE',     r'\)'),
    ('COMMA',     r','),
    ('OP',        r'[+\-*/]'),       #运算符
    ('SKIP',      r'[ \t]+'),
    ('MISMATCH',  r'.'),
    ('NEWLINE',   r'\n'),
    ('PI',        r'PI'),
    ('e',         r'e'),
    ('FUNC',      r'[a-zA-Z_]\w*')
]

TokenDict = dict(

)
# 编译正则表达式
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
get_token = re.compile(tok_regex).match

# 词法分析器
def tokenize(code):
    line_number = 1
    current_position = line_number_start = 0
    mo = get_token(code)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NUMBER':
            value = float(value)
            yield kind, value
        elif kind == 'NEWLINE':
            line_number += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'PI':
            yield kind, math.pi
        elif kind == 'e':
            yield kind, math.e
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r} at line {line_number}')
        else:
             yield kind, value
        current_position = mo.end()
        mo = get_token(code, current_position)
    if current_position != len(code):
        raise RuntimeError('Unexpected end of input')

#测试
code = """FOR T FROM 0 TO 2*PI STEP PI/50 DRAW (cos(T), sin(T));
SCALE IS (100, 100);
ORIGIN IS (360, 240);
ROT IS PI/2;"""
for token in tokenize(code):
    print(token)