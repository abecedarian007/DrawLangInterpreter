# 目前只写了FOR-DRAW
from src import Token
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]

    def parse(self):
        return self.parse_for_draw_statement()

    def parse_for_draw_statement(self):
        self.match(Token.ReservedWord.FOR)
        self.match(TokenType.T)
        self.match(TokenType.FROM)
        start_expr = self.parse_expression()
        self.match(TokenType.TO)
        end_expr = self.parse_expression()
        self.match(TokenType.STRE)
        step_expr = self.parse_expression()
        self.match("DRAW")
        self.match("(")
        x_expr = self.parse_expression()
        self.match(",")
        y_expr = self.parse_expression()
        self.match(")")

#   简单逻辑
        return {
            "type": "FOR-DRAW",
            "start": start_expr,
            "end": end_expr,
            "step": step_expr,
            "draw": {"x": x_expr, "y": y_expr}
        }

    def parse_expression(self):
        expr = self.parse_term()
        while self.current_token.type in ["+", "-"]:
            operator = self.current_token.type
            self.advance_token()
            right = self.parse_term()
            expr = {"type": "binary-op", "operator": operator, "left": expr, "right": right}
        return expr

    def parse_term(self):
        term = self.parse_factor()
        while self.current_token.type in ["*", "/"]:
            operator = self.current_token.type
            self.advance_token()
            right = self.parse_factor()
            term = {"type": "binary-op", "operator": operator, "left": term, "right": right}
        return term

    def parse_factor(self):
        if self.current_token.type == "NUMBER":
            value = self.current_token.value
            self.advance_token()
            return {"type": "number", "value": value}
        elif self.current_token.type == "(":
            self.advance_token()
            expr = self.parse_expression()
            self.match(")")
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.type}")

    def match(self, expected_type):
        if self.current_token.type == expected_type:
            self.advance_token()
        else:
            raise SyntaxError(f"Expected token {expected_type}, found {self.current_token.type}")

    def advance_token(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None




