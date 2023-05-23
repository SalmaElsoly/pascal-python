from .Util import Position


class CustomError(Exception):
    def __init__(self, pos, error_name, details):
        self.pos: Position = pos
        self.error_name = error_name
        self.details = details
        super().__init__(self.as_string())

    def as_string(self):
        result = f"Error {self.error_name}, given: {self.details}\n"
        result += f"Line {self.pos.ln + 1}, column {self.pos.col + 1}"
        return result


class UnknownToken(CustomError):
    def __init__(self, pos, given):
        super().__init__(pos, "UnknownToken", given)


class InvalidConstant(CustomError):
    def __init__(self, pos, given):
        super().__init__(pos, "InvalidConstant", given)


class IncompleteString(CustomError):
    def __init__(self, pos, given):
        super().__init__(pos, "IncompleteString", given)

class IncompleteComment(CustomError):
    def __init__(self, pos, given):
        super().__init__(pos, "IncompleteComment", given)
