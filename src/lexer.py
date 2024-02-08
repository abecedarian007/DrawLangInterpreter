import re
from src.Token import mark_token

TOKEN_SPECIFICATION = [
    ('BLANK', r'[ \t]+'),
    ('COMMENT', r'//.*'),
    ('NUMBER', r'\d+(\.\d*)?'),  # 整数或者小数
    ('PI', r'\bPI\b'),
    ('E', r'\bE\b'),
    ('TO', r'\bTO\b'),
    ('T', r'\bT\b'),
    ('SIN', r'\bSIN\b'),
    ('COS', r'\bCOS\b'),
    ('TAN', r'\bTAN\b'),
    ('LN', r'\bLN\b'),
    ('SQRT', r'\bSQRT\b'),
    ('EXP', r'\bEXP\b'),
    ('ORIGIN', r'\bORIGIN\b'),
    ('SCALE', r'\bSCALE\b'),
    ('ROT', r'\bROT\b'),
    ('IS', r'\bIS\b'),
    ('FOR', r'\bFOR\b'),
    ('FROM', r'\bFROM\b'),
    ('STEP', r'\bSTEP\b'),
    ('DRAW', r'\bDRAW\b'),
    ('COLOR', r'\bCOLOR\b'),
    ('SET_CIRCLE', r'\bSET_CIRCLE\b'),
    ('RADIUS', r'\bRADIUS\b'),
    ('RED', r'\bRED\b'),
    ('BLUE', r'\bBLUE\b'),
    ('YELLOW', r'\bYELLOW\b'),
    ('GREEN', r'\bGREEN\b'),
    ('WHITE', r'\bWHITE\b'),
    ('BLACK', r'\bBLACK\b'),
    ('POSITIVE', r'(?<![0-9PIET])\s*\+\s*(?=[0-9PIET])'),
    ('NEGATIVE', r'(?<![0-9PIET])\s*-\s*(?=[0-9PIET])'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MULTIPLY', r'(?<!\*)\*(?!\*)'),
    ('DIVIDE', r'/'),
    ('POWER', r'\*\*'),
    ('LEFT_BRACKET', r'\('),
    ('RIGHT_BRACKET', r'\)'),
    ('COMMA', r','),
    ('SEMICOLON', r';'),
    ('NEWLINE', r'\n'),
    ('RETURN', r'\r'),
    ('MISMATCH', r'\S+')  # 匹配非空白字符的序列
]

tk_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
get_token = re.compile(tk_regex).match


def tokenize(code_input):
    upper_code = code_input.upper()  # 将代码转化为大写
    token_list = []
    current_position = 0

    while current_position < len(upper_code):
        mo = get_token(upper_code, current_position)
        if mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind != "BLANK" and kind != "NEWLINE" and kind != "RETURN" and kind != "COMMENT":  # 忽略空白、回车、换行、注释
                token_list.append(mark_token(kind, value))
            current_position = mo.end()
        else:
            # 当前位置未找到匹配，查找下一个空白字符或字符串末尾
            next_space = upper_code.find(' ', current_position)
            if next_space == -1:
                next_space = len(upper_code)
            value = upper_code[current_position:next_space]
            token_list.append(mark_token('MISMATCH', value))
            current_position = next_space

    return token_list


# # 测试
# code = """SET_CIRCLE (10,10) RADIUS (2, 4);
# FOR T FROM 0 TO 2 STEP PI DRAW ((2*2+100)*cos(T), sin(T));
# FOR T FROM 0 TO 2 STEP PI DRAW (T+T, sin(T));
# // this is a comment
# SCALE IS (100+1, (100-5)*2);
# ORIGIN IS (+360, -240);
# ROT IS -PI/2;
# COLOR RED;
# """

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
#
# code = """for t from 0 to 2*pi step pi/200 draw(16*(sin(t)**3),13*cos(t) - 5*cos(2*t) - 2*cos(3*t)-cos(4*t));
# """
#
# for token_name in tokenize(code):
#     # print(token_name.raw, token_name.token_type, token_name.token_name)
#     token_name.show()
