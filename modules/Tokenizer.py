class Tokenizer:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {"Lex": self.lex, "token_type": self.token_type}
