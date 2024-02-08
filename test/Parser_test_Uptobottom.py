from src.lexer import tokenize
from src.Token import *
import math


class Parser:
    def __init__(self, token_list):
        self.tokens = token_list
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = next(self.tokens, None)

    def parse(self):
        while self.current_token:
            if self.current_token.token_name == ReservedWord.SCALE:
                self.parse_scale_statement()
            elif self.current_token.token_name == ReservedWord.FOR:
                self.parse_for_draw_statement()
            elif self.current_token.token_name == ReservedWord.ORIGIN:
                self.parse_origin_statement()
            elif self.current_token.token_name == ReservedWord.ROT:
                self.parse_rot_statement()
            else:
                # 跳过未识别的，错误处理
                self.next_token()

    def parse_origin_statement(self):
        # Syntax: ORIGIN IS (横坐标, 纵坐标);
        self.next_token()
        if self.current_token.token_name != ReservedWord.IS:
            raise SyntaxError("Expected 'IS' after 'ORIGIN'")
        self.next_token()

        # Expecting a '('
        if self.current_token.token_name != Seperator.LEFT_BRACKET:
            raise SyntaxError("Expected '(' after 'IS'")
        self.next_token()

        x_origin = self.parse_expression()
        if self.current_token.token_name != Seperator.COMMA:
            raise SyntaxError("Expected ',' after x origin coordinate")
        self.next_token()

        y_origin = self.parse_expression()

        # Expecting a ')'
        if self.current_token.token_name != Seperator.RIGHT_BRACKET:
            raise SyntaxError("Expected ')' after y origin coordinate")
        self.next_token()

        # Expecting a ';'
        if self.current_token.token_name != Seperator.SEMICOLON:
            raise SyntaxError("Expected ';' at the end of ORIGIN statement")
        self.next_token()

        print(f"ORIGIN statement parsed with x coordinate: {x_origin} and y coordinate: {y_origin}")

    def parse_for_draw_statement(self):
        # Syntax: FOR T FROM 起点 TO 终点 STEP 步长 DRAW(横坐标, 纵坐标);
        self.next_token()

        # Expecting a 'T'
        if self.current_token.token_name != Parameter.T:
            raise SyntaxError("Expected 'T' after 'FOR'")
        self.next_token()

        # Expecting a 'FROM'
        if self.current_token.token_name != ReservedWord.FROM:
            raise SyntaxError("Expected 'FROM' after 'T'")
        self.next_token()

        start_point = self.parse_expression()

        # Expecting a 'TO'
        if self.current_token.token_name != ReservedWord.TO:
            raise SyntaxError("Expected 'TO' after start point")
        self.next_token()

        # Parsing the end point
        end_point = self.parse_expression()

        # Expecting a 'STEP'
        if self.current_token.token_name != ReservedWord.STEP:
            raise SyntaxError("Expected 'STEP' after end point")
        self.next_token()

        # Parsing the step value
        step_value = self.parse_expression()

        # Expecting a 'DRAW'
        if self.current_token.token_name != ReservedWord.DRAW:
            raise SyntaxError("Expected 'DRAW' after step value")
        self.next_token()

        # Expecting a '('
        if self.current_token.token_name != Seperator.LEFT_BRACKET:
            raise SyntaxError("Expected '(' after 'DRAW'")
        self.next_token()

        x_draw = self.parse_expression()
        if self.current_token.token_name != Seperator.COMMA:
            raise SyntaxError("Expected ',' after x draw coordinate")
        self.next_token()

        y_draw = self.parse_expression()

        # Expecting a ')'
        if self.current_token.token_name != Seperator.RIGHT_BRACKET:
            raise SyntaxError("Expected ')' after y draw coordinate")
        self.next_token()

        # Expecting a ';'
        if self.current_token.token_name != Seperator.SEMICOLON:
            raise SyntaxError("Expected ';' at the end of FOR-DRAW statement")
        self.next_token()

        print(f"FOR-DRAW statement parsed with start point: {start_point}, end point: {end_point}, step value: {step_value}, x draw: {x_draw}, y draw: {y_draw}")

    def parse_scale_statement(self):
        # Syntax: SCALE IS (横坐标比例因子, 纵坐标比例因子);
        self.next_token()
        if self.current_token.token_name != ReservedWord.IS:
            raise SyntaxError("Expected 'IS' after 'SCALE'")
        self.next_token()

        # Expecting a '('
        if self.current_token.token_name != Seperator.LEFT_BRACKET:
            raise SyntaxError("Expected '(' after 'IS'")
        self.next_token()

        x_scale = self.parse_expression()
        if self.current_token.token_name != Seperator.COMMA:
            raise SyntaxError("Expected ',' after x scale factor")
        self.next_token()

        y_scale = self.parse_expression()

        # Expecting a ')'
        if self.current_token.token_name != Seperator.RIGHT_BRACKET:
            raise SyntaxError("Expected ')' after y scale factor")
        self.next_token()

        # Expecting a ';'
        if self.current_token.token_name != Seperator.SEMICOLON:
            raise SyntaxError("Expected ';' at the end of SCALE statement")
        self.next_token()

        print(f"SCALE statement parsed with x scale factor: {x_scale} and y scale factor: {y_scale}")

    def parse_rot_statement(self):
        # Syntax: ROT IS 弧度值;
        self.next_token()
        if self.current_token.token_name != ReservedWord.IS:
            raise SyntaxError("Expected 'IS' after 'ROT'")
        self.next_token()

        radian_value = self.parse_expression()

        if self.current_token.token_name != Seperator.SEMICOLON:
            raise SyntaxError("Expected ';' at the end of ROT statement")
        self.next_token()
        print(f"ROT statement parsed with radian value: {radian_value}")

    def parse_expression(self):
        # 这里要实现表达式的解析，包括数字和运算，现在我只实现了单独数字标记
        if self.current_token.token_name != Constant.NUMBER and self.current_token.token_name != Constant.PI:
            raise SyntaxError("Expected a number")
        value = self.current_token.value
        self.next_token()  # Move past the number token_name
        return value
        # if self.current_token.token_name == ConstantEnum.PI:
            # 准备通过eval函数直接极端表达式的值


code = """FOR T FROM 0 TO 2 STEP PI DRAW (1, 2);
// this is a comment
SCALE IS (100, 100);
ORIGIN IS (360, 240);
"""

tokens = tokenize(code)
parser = Parser(iter(tokens))
parser.parse()

