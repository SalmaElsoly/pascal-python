class Position:
    def __init__(self, idx):
        self.idx = idx
        self.ln = 0
        self.col = -1

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self
