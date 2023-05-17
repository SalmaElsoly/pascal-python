import re
from modules.Tokenizer import Tokenizer
from modules.Tokens import Token_type, Operators, ReservedWords
from modules.Errors import CustomError, IncompleteString, InvalidConstant, UnknownToken
from modules.Util import Position


class Lexer:
    def __init__(self, text) -> None:
        self.text: str = text
        self.pos: Position = Position(-1)
        self.current_char: str = None
        self.next_char: str = None
        self.tokens: list[Tokenizer] = []
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if int(self.pos.idx) < len(self.text) else None
        )
        self.next_char = (
            self.text[self.pos.idx + 1] if self.pos.idx + 1 < len(self.text) else None
        )

    def make_tokens(self):
        try:
            while self.current_char is not None:
                if self.current_char in " \t\n":
                    self.advance()
                elif re.fullmatch(r"\.|[0-9]", self.current_char) or (
                    self.next_char is not None
                    and self.current_char in "+-"
                    and re.fullmatch(r"\.|[0-9]", self.next_char)
                ):
                    self.make_constant()
                elif self.current_char in Operators or (
                    self.next_char is not None
                    and (self.current_char + self.next_char) in Operators
                ):
                    self.make_operator()
                elif re.fullmatch(r"[a-zA-z]", self.current_char):
                    self.make_reserved_word_or_identifier()
                elif self.current_char is "'":
                    self.make_string()
                else:
                    raise UnknownToken(self.pos, self.current_char)
        except CustomError as e:
            return [], e.as_string()
        return self.tokens, None

    def make_operator(self):
        op_str = self.current_char
        self.advance()
        if self.current_char is not None and (op_str + self.current_char) in Operators:
            op_str += self.next_char
            self.advance()
            self.tokens.append(Tokenizer(op_str, Operators[op_str]))
        else:
            self.tokens.append(Tokenizer(op_str, Operators[op_str]))

    def make_constant(self):
        num_str = ""
        dot_count = 0
        if self.current_char in "+-":
            num_str += self.current_char
            self.advance()
        if self.current_char is ".":
            num_str += self.current_char
            dot_count += 1
            self.advance()

        while self.current_char is not None and (
            self.current_char.isnumeric() or self.current_char is "."
        ):
            if self.current_char == ".":
                dot_count += 1
            num_str += self.current_char
            self.advance()
        if num_str == ".":
            self.tokens.append(Tokenizer(num_str, Token_type.Dot))
            return
        if (
            dot_count > 1
            or (len(num_str) <= 2 and re.fullmatch(r"[+-]|([+-]\.)", num_str))
            or not re.fullmatch(r"^(?=.)(([+-]?[0-9]*)(\.[0-9]*)?)$", num_str)
        ):
            raise InvalidConstant(self.pos, self.current_char)
        self.tokens.append(Tokenizer(num_str, Token_type.Constant))

    def make_reserved_word_or_identifier(self):
        rwid_str = ""
        while self.current_char is not None and re.fullmatch(
            r"^(^[a-zA-z][a-zA-z0-9]*$)$", rwid_str + self.current_char
        ):
            rwid_str += self.current_char
            self.advance()
        if rwid_str in ReservedWords:
            self.tokens.append(Tokenizer(rwid_str, ReservedWords[rwid_str]))
        else:
            self.tokens.append(Tokenizer(rwid_str, Token_type.Identifier))

    def make_string(self):
        str_str = ""
        self.advance()
        while self.current_char != "'":
            if self.current_char == "\\":
                self.advance()
            if self.current_char is None:
                raise IncompleteString(
                    self.pos,
                    "EOF",
                )
            str_str += self.current_char
            self.advance()
        self.advance()
        self.tokens.append(Tokenizer(str_str, Token_type.String))
